/**
 * Error Handler Module
 * 
 * Captura e trata erros da extensão
 */

import { logger } from './logger.js';

export interface ErrorContext {
  operation?: string;
  agentId?: string;
  details?: Record<string, any>;
}

export class ExtensionError extends Error {
  constructor(
    message: string,
    public code: string,
    public context?: ErrorContext,
    public cause?: Error
  ) {
    super(message);
    this.name = 'ExtensionError';
  }
}

export enum ErrorSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical',
}

export interface ErrorReport {
  error: ExtensionError;
  severity: ErrorSeverity;
  timestamp: number;
  handled: boolean;
}

type ErrorStrategy = 'retry' | 'fallback' | 'ignore' | 'abort';

export class ErrorHandler {
  private errors: ErrorReport[] = [];
  private strategies: Map<string, ErrorStrategy> = new Map();
  private retryCounts: Map<string, number> = new Map();
  private maxRetries: number = 3;

  constructor() {
    this.setupGlobalHandlers();
  }

  private setupGlobalHandlers(): void {
    process.on('uncaughtException', (error) => {
      logger.error('Uncaught exception', error);
      this.report(error, ErrorSeverity.HIGH);
    });

    process.on('unhandledRejection', (reason) => {
      logger.error('Unhandled rejection', reason);
      this.report(new Error(String(reason)), ErrorSeverity.HIGH);
    });
  }

  setStrategy(errorCode: string, strategy: ErrorStrategy): void {
    this.strategies.set(errorCode, strategy);
  }

  setMaxRetries(max: number): void {
    this.maxRetries = max;
  }

  report(error: Error | ExtensionError, severity: ErrorSeverity = ErrorSeverity.MEDIUM): ErrorReport {
    const extError = error instanceof ExtensionError
      ? error
      : new ExtensionError(error.message, 'UNKNOWN_ERROR', undefined, error);

    const report: ErrorReport = {
      error: extError,
      severity,
      timestamp: Date.now(),
      handled: false,
    };

    this.errors.push(report);
    logger.error(`[${extError.code}] ${extError.message}`, extError.cause);

    return report;
  }

  async handle(error: ExtensionError): Promise<void> {
    const report = this.errors.find(r => r.error === error);
    if (report) report.handled = true;

    const strategy = this.strategies.get(error.code) || 'fallback';

    switch (strategy) {
      case 'retry':
        await this.handleRetry(error);
        break;
      case 'fallback':
        await this.handleFallback(error);
        break;
      case 'ignore':
        logger.debug(`Ignoring error: ${error.code}`);
        break;
      case 'abort':
        logger.error(`Aborting due to error: ${error.code}`);
        throw error;
    }
  }

  private async handleRetry(error: ExtensionError): Promise<void> {
    const key = `${error.code}_${error.context?.operation || 'default'}`;
    const count = this.retryCounts.get(key) || 0;

    if (count >= this.maxRetries) {
      logger.error(`Max retries exceeded for: ${key}`);
      await this.handleFallback(error);
      return;
    }

    this.retryCounts.set(key, count + 1);
    logger.info(`Retrying operation (${count + 1}/${this.maxRetries}): ${key}`);
  }

  private async handleFallback(error: ExtensionError): void {
    logger.warn(`Using fallback for: ${error.code}`);
  }

  getRecentErrors(limit: number = 10): ErrorReport[] {
    return this.errors
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, limit);
  }

  getErrorsByCode(code: string): ErrorReport[] {
    return this.errors.filter(r => r.error.code === code);
  }

  getErrorsBySeverity(severity: ErrorSeverity): ErrorReport[] {
    return this.errors.filter(r => r.severity === severity);
  }

  clearErrors(): void {
    this.errors = [];
    this.retryCounts.clear();
  }

  getErrorStats(): { total: number; bySeverity: Record<ErrorSeverity, number>; byCode: Record<string, number> } {
    const bySeverity: Record<ErrorSeverity, number> = {
      low: 0,
      medium: 0,
      high: 0,
      critical: 0,
    };
    const byCode: Record<string, number> = {};

    for (const report of this.errors) {
      bySeverity[report.severity]++;
      byCode[report.error.code] = (byCode[report.error.code] || 0) + 1;
    }

    return {
      total: this.errors.length,
      bySeverity,
      byCode,
    };
  }
}

export const errorHandler = new ErrorHandler();

export function createError(code: string, message: string, context?: ErrorContext, cause?: Error): ExtensionError {
  return new ExtensionError(message, code, context, cause);
}
