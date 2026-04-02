/**
 * Configuration Module
 * 
 * Gerencia configurações do Agent View com validação
 */

import type { AgentViewConfig } from './monitor.js';

export interface PerformanceConfig {
  cleanupTimeout: number;
  adaptiveRefresh: boolean;
  minRefreshInterval: number;
  maxRefreshInterval: number;
  refreshPerAgent: number;
}

export interface PersistenceConfig {
  enabled: boolean;
  presetsPath: string;
  autoSaveInterval: number;
}

export interface LoggingConfig {
  level: 'debug' | 'info' | 'warn' | 'error' | 'none';
  console: boolean;
  file: boolean;
  logPath: string;
}

export interface CompleteAgentViewConfig extends AgentViewConfig {
  performance: PerformanceConfig;
  persistence: PersistenceConfig;
  logging: LoggingConfig;
}

export const DEFAULT_CONFIG: CompleteAgentViewConfig = {
  layout: '1x4',
  font: 'medium',
  sortMode: 'default',
  headerStyle: 'detailed',
  showBorders: true,
  showColors: true,
  showProgress: true,
  autoRefresh: true,
  refreshInterval: 500,
  performance: {
    cleanupTimeout: 5 * 60 * 1000,
    adaptiveRefresh: true,
    minRefreshInterval: 500,
    maxRefreshInterval: 5000,
    refreshPerAgent: 50,
  },
  persistence: {
    enabled: true,
    presetsPath: '.pi/agent-view-presets.json',
    autoSaveInterval: 30 * 1000,
  },
  logging: {
    level: 'info',
    console: true,
    file: false,
    logPath: '.pi/agent-view.log',
  },
};

export class ConfigValidator {
  static validateLayout(value: unknown): '1x1' | '1x2' | '1x4' | '1x8' | 'list' {
    const valid = ['1x1', '1x2', '1x4', '1x8', 'list'];
    if (typeof value === 'string' && valid.includes(value)) return value as any;
    return DEFAULT_CONFIG.layout;
  }

  static validateFont(value: unknown): 'small' | 'medium' | 'large' {
    const valid = ['small', 'medium', 'large'];
    if (typeof value === 'string' && valid.includes(value)) return value as any;
    return DEFAULT_CONFIG.font;
  }

  static validateSortMode(value: unknown): 'default' | 'active' {
    const valid = ['default', 'active'];
    if (typeof value === 'string' && valid.includes(value)) return value as any;
    return DEFAULT_CONFIG.sortMode;
  }

  static validateHeaderStyle(value: unknown): 'minimal' | 'detailed' | 'compact' {
    const valid = ['minimal', 'detailed', 'compact'];
    if (typeof value === 'string' && valid.includes(value)) return value as any;
    return DEFAULT_CONFIG.headerStyle;
  }

  static validateBoolean(value: unknown, defaultValue: boolean): boolean {
    if (typeof value === 'boolean') return value;
    if (typeof value === 'string') {
      const lower = value.toLowerCase();
      if (lower === 'true' || lower === '1' || lower === 'yes') return true;
      if (lower === 'false' || lower === '0' || lower === 'no') return false;
    }
    if (typeof value === 'number') return value !== 0;
    return defaultValue;
  }

  static validatePositiveNumber(value: unknown, defaultValue: number, min?: number, max?: number): number {
    if (typeof value === 'number' && !isNaN(value) && value >= 0) {
      if (min !== undefined && value < min) return min;
      if (max !== undefined && value > max) return max;
      return value;
    }
    if (typeof value === 'string') {
      const parsed = parseInt(value, 10);
      if (!isNaN(parsed) && parsed >= 0) {
        if (min !== undefined && parsed < min) return min;
        if (max !== undefined && parsed > max) return max;
        return parsed;
      }
    }
    return defaultValue;
  }

  static validateLogLevel(value: unknown): LoggingConfig['level'] {
    const valid = ['debug', 'info', 'warn', 'error', 'none'];
    if (typeof value === 'string' && valid.includes(value)) return value as any;
    return DEFAULT_CONFIG.logging.level;
  }

  static validate(partial: Partial<CompleteAgentViewConfig>): CompleteAgentViewConfig {
    const config: CompleteAgentViewConfig = { ...DEFAULT_CONFIG };

    if (partial.layout !== undefined) config.layout = this.validateLayout(partial.layout);
    if (partial.font !== undefined) config.font = this.validateFont(partial.font);
    if (partial.sortMode !== undefined) config.sortMode = this.validateSortMode(partial.sortMode);
    if (partial.headerStyle !== undefined) config.headerStyle = this.validateHeaderStyle(partial.headerStyle);
    if (partial.showBorders !== undefined) config.showBorders = this.validateBoolean(partial.showBorders, DEFAULT_CONFIG.showBorders);
    if (partial.showColors !== undefined) config.showColors = this.validateBoolean(partial.showColors, DEFAULT_CONFIG.showColors);
    if (partial.showProgress !== undefined) config.showProgress = this.validateBoolean(partial.showProgress, DEFAULT_CONFIG.showProgress);
    if (partial.autoRefresh !== undefined) config.autoRefresh = this.validateBoolean(partial.autoRefresh, DEFAULT_CONFIG.autoRefresh);
    if (partial.refreshInterval !== undefined) config.refreshInterval = this.validatePositiveNumber(partial.refreshInterval, DEFAULT_CONFIG.refreshInterval, 100, 60000);

    if (partial.performance) {
      config.performance = {
        cleanupTimeout: this.validatePositiveNumber(partial.performance.cleanupTimeout, DEFAULT_CONFIG.performance.cleanupTimeout, 1000),
        adaptiveRefresh: this.validateBoolean(partial.performance.adaptiveRefresh, DEFAULT_CONFIG.performance.adaptiveRefresh),
        minRefreshInterval: this.validatePositiveNumber(partial.performance.minRefreshInterval, DEFAULT_CONFIG.performance.minRefreshInterval, 100),
        maxRefreshInterval: this.validatePositiveNumber(partial.performance.maxRefreshInterval, DEFAULT_CONFIG.performance.maxRefreshInterval, 100),
        refreshPerAgent: this.validatePositiveNumber(partial.performance.refreshPerAgent, DEFAULT_CONFIG.performance.refreshPerAgent, 0),
      };
    }

    if (partial.persistence) {
      config.persistence = {
        enabled: this.validateBoolean(partial.persistence.enabled, DEFAULT_CONFIG.persistence.enabled),
        presetsPath: typeof partial.persistence.presetsPath === 'string' ? partial.persistence.presetsPath : DEFAULT_CONFIG.persistence.presetsPath,
        autoSaveInterval: this.validatePositiveNumber(partial.persistence.autoSaveInterval, DEFAULT_CONFIG.persistence.autoSaveInterval, 1000),
      };
    }

    if (partial.logging) {
      config.logging = {
        level: partial.logging.level !== undefined ? this.validateLogLevel(partial.logging.level) : DEFAULT_CONFIG.logging.level,
        console: this.validateBoolean(partial.logging.console ?? DEFAULT_CONFIG.logging.console, DEFAULT_CONFIG.logging.console),
        file: this.validateBoolean(partial.logging.file ?? DEFAULT_CONFIG.logging.file, DEFAULT_CONFIG.logging.file),
        logPath: typeof partial.logging.logPath === 'string' ? partial.logging.logPath : DEFAULT_CONFIG.logging.logPath,
      };
    }

    return config;
  }

  static calculateAdaptiveInterval(config: CompleteAgentViewConfig, activeAgentCount: number): number {
    if (!config.performance.adaptiveRefresh) return config.refreshInterval;
    const { minRefreshInterval, maxRefreshInterval, refreshPerAgent } = config.performance;
    const calculated = config.refreshInterval + (activeAgentCount * refreshPerAgent);
    return Math.max(minRefreshInterval, Math.min(maxRefreshInterval, calculated));
  }
}

export interface AgentViewPreset {
  name: string;
  config: AgentViewConfig;
  createdAt: number;
  updatedAt: number;
}

export interface AgentViewPresets {
  version: string;
  presets: Record<string, AgentViewPreset>;
  lastPreset?: string;
}

export class ConfigManager {
  private config: CompleteAgentViewConfig;
  private listeners: Array<(config: CompleteAgentViewConfig) => void> = [];

  constructor(initialConfig?: Partial<CompleteAgentViewConfig>) {
    this.config = ConfigValidator.validate(initialConfig || {});
  }

  getConfig(): CompleteAgentViewConfig {
    return { ...this.config };
  }

  getUIConfig(): AgentViewConfig {
    return {
      layout: this.config.layout,
      font: this.config.font,
      sortMode: thi
