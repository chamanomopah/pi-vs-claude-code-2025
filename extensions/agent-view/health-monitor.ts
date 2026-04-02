/**
 * Health Monitor Module
 * 
 * Monitora o estado da extensão e detecta problemas
 */

import { EventEmitter } from 'events';
import { logger } from './logger.js';
import { errorHandler, ErrorSeverity } from './error-handler.js';

export type HealthStatus = 'healthy' | 'degraded' | 'unhealthy';

export interface HealthCheck {
  name: string;
  check: () => boolean | Promise<boolean>;
  critical: boolean;
}

export interface HealthReport {
  status: HealthStatus;
  checks: Record<string, boolean>;
  timestamp: number;
  issues: string[];
}

export class HealthMonitor extends EventEmitter {
  private checks: Map<string, HealthCheck> = new Map();
  private status: HealthStatus = 'healthy';
  private monitorTimer?: NodeJS.Timeout;
  private lastReport?: HealthReport;

  constructor(private interval: number = 30000) {
    super();
  }

  registerCheck(check: HealthCheck): void {
    this.checks.set(check.name, check);
    logger.debug(`Registered health check: ${check.name}`);
  }

  unregisterCheck(name: string): void {
    this.checks.delete(name);
  }

  async check(): Promise<HealthReport> {
    const results: Record<string, boolean> = {};
    const issues: string[] = [];
    let failedCritical = 0;
    let failedTotal = 0;

    for (const [name, check] of this.checks) {
      try {
        const passed = await check.check();
        results[name] = passed;
        
        if (!passed) {
          failedTotal++;
          issues.push(`${name} failed`);
          if (check.critical) {
            failedCritical++;
          }
        }
      } catch (error) {
        results[name] = false;
        failedTotal++;
        issues.push(`${name} error: ${error}`);
        if (check.critical) failedCritical++;
      }
    }

    const previousStatus = this.status;

    if (failedCritical > 0) {
      this.status = 'unhealthy';
    } else if (failedTotal > 0) {
      this.status = 'degraded';
    } else {
      this.status = 'healthy';
    }

    this.lastReport = {
      status: this.status,
      checks: results,
      timestamp: Date.now(),
      issues,
    };

    if (previousStatus !== this.status) {
      logger.info(`Health status changed: ${previousStatus} -> ${this.status}`);
      this.emit('status-change', this.status, previousStatus);
    }

    if (this.status !== 'healthy') {
      this.emit('issues', issues);
    }

    return this.lastReport;
  }

  getStatus(): HealthStatus {
    return this.status;
  }

  getLastReport(): HealthReport | undefined {
    return this.lastReport;
  }

  start(): void {
    if (this.monitorTimer) return;

    this.monitorTimer = setInterval(async () => {
      await this.check();
    }, this.interval);

    logger.info('Health monitor started');
  }

  stop(): void {
    if (this.monitorTimer) {
      clearInterval(this.monitorTimer);
      this.monitorTimer = undefined;
    }
    logger.info('Health monitor stopped');
  }

  dispose(): void {
    this.stop();
    this.removeAllListeners();
  }
}

export function createDefaultHealthMonitor(): HealthMonitor {
  const monitor = new HealthMonitor();

  monitor.registerCheck({
    name: 'memory',
    critical: false,
    check: () => {
      const usage = process.memoryUsage();
      const heapUsedMB = usage.heapUsed / 1024 / 1024;
      const heapTotalMB = usage.heapTotal / 1024 / 1024;
      const usagePercent = (heapUsedMB / heapTotalMB) * 100;
      return usagePercent < 90;
    },
  });

  monitor.registerCheck({
    name: 'error-rate',
    critical: false,
    check: () => {
      const stats = errorHandler.getErrorStats();
      const recent = stats.bySeverity[ErrorSeverity.HIGH] + stats.bySeverity[ErrorSeverity.CRITICAL];
      return recent < 10;
    },
  });

  monitor.registerCheck({
    name: 'event-loop',
    critical: true,
    check: () => {
      return new Promise<boolean>((resolve) => {
        const start = Date.now();
        setImmediate(() => {
          const elapsed = Date.now() - start;
          resolve(elapsed < 100);
        });
      });
    },
  });

  return monitor;
}
