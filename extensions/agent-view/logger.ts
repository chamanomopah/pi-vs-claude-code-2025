/**
 * Logger Module
 * 
 * Sistema de logging para debug, warning e error
 */

export type LogLevel = 'debug' | 'info' | 'warn' | 'error' | 'none';

const LOG_LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
  none: 4,
};

const LOG_COLORS: Record<LogLevel, string> = {
  debug: '\x1b[36m', // cyan
  info: '\x1b[32m',  // green
  warn: '\x1b[33m',  // yellow
  error: '\x1b[31m', // red
  none: '\x1b[0m',
};

const RESET = '\x1b[0m';

export interface LoggerConfig {
  level: LogLevel;
  console: boolean;
  file: boolean;
  logPath: string;
}

export class Logger {
  private config: LoggerConfig;
  private buffer: string[] = [];

  constructor(config: LoggerConfig) {
    this.config = config;
  }

  setConfig(config: Partial<LoggerConfig>): void {
    this.config = { ...this.config, ...config };
  }

  shouldLog(level: LogLevel): boolean {
    return LOG_LEVELS[level] >= LOG_LEVELS[this.config.level];
  }

  debug(message: string, ...args: any[]): void {
    this.log('debug', message, ...args);
  }

  info(message: string, ...args: any[]): void {
    this.log('info', message, ...args);
  }

  warn(message: string, ...args: any[]): void {
    this.log('warn', message, ...args);
  }

  error(message: string, error?: Error | unknown, ...args: any[]): void {
    this.log('error', message, error, ...args);
  }

  private log(level: LogLevel, message: string, ...args: any[]): void {
    if (!this.shouldLog(level) || level === 'none') return;

    const timestamp = new Date().toISOString();
    const prefix = `${LOG_COLORS[level]}[${timestamp}] [${level.toUpperCase()}]${RESET}`;
    const fullMessage = `${prefix} ${message}`;

    if (this.config.console) {
      console.log(fullMessage, ...args);
    }

    if (this.config.file) {
      this.buffer.push(`[${timestamp}] [${level.toUpperCase()}] ${message}`);
      if (args.length > 0) {
        this.buffer.push(JSON.stringify(args));
      }
    }
  }

  async flush(): Promise<void> {
    if (!this.config.file || this.buffer.length === 0) return;

    try {
      const fs = await import('fs');
      await fs.promises.mkdir('.pi', { recursive: true });
      await fs.promises.appendFile(this.config.logPath, this.buffer.join('\n') + '\n');
      this.buffer = [];
    } catch (err) {
      console.error('[Logger] Failed to write log file:', err);
    }
  }

  clearBuffer(): void {
    this.buffer = [];
  }
}

export const logger = new Logger({
  level: 'info',
  console: true,
  file: false,
  logPath: '.pi/agent-view.log',
});
