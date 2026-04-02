/**
 * Storage Module
 * 
 * Sistema de persistência de presets de configuração
 */

import type { AgentViewPreset, AgentViewPresets } from './config.js';
import { logger } from './logger.js';

const PRESETS_VERSION = '1.0.0';
const DEFAULT_PRESETS_PATH = '.pi/agent-view-presets.json';

export class PresetStorage {
  private presets: AgentViewPresets;
  private dirty: boolean = false;
  private autoSaveTimer?: NodeJS.Timeout;

  constructor(
    private presetsPath: string = DEFAULT_PRESETS_PATH,
    private autoSaveInterval: number = 30000
  ) {
    this.presets = { version: PRESETS_VERSION, presets: {} };
  }

  async load(): Promise<void> {
    try {
      const fs = await import('fs');
      const exists = await fs.promises.access(this.presetsPath).then(() => true).catch(() => false);

      if (!exists) {
        logger.debug('Presets file does not exist, starting fresh');
        this.presets = { version: PRESETS_VERSION, presets: {} };
        return;
      }

      const content = await fs.promises.readFile(this.presetsPath, 'utf-8');
      const data = JSON.parse(content) as AgentViewPresets;

      if (data.version !== PRESETS_VERSION) {
        logger.warn(`Presets version mismatch: ${data.version} vs ${PRESETS_VERSION}, migrating`);
        await this.migrate(data);
      } else {
        this.presets = data;
      }

      logger.info(`Loaded ${Object.keys(this.presets.presets).length} presets`);
    } catch (error) {
      logger.error('Failed to load presets', error);
      this.presets = { version: PRESETS_VERSION, presets: {} };
    }
  }

  async save(force: boolean = false): Promise<void> {
    if (!force && !this.dirty) {
      logger.debug('No changes to save');
      return;
    }

    try {
      const fs = await import('fs');
      await fs.promises.mkdir('.pi', { recursive: true });
      const content = JSON.stringify(this.presets, null, 2);
      await fs.promises.writeFile(this.presetsPath, content, 'utf-8');
      
      this.dirty = false;
      logger.debug('Presets saved successfully');
    } catch (error) {
      logger.error('Failed to save presets', error);
      throw error;
    }
  }

  async savePreset(name: string, preset: AgentViewPreset): Promise<void> {
    this.presets.presets[name] = { ...preset, name, updatedAt: Date.now() };
    this.presets.lastPreset = name;
    this.dirty = true;
    logger.info(`Preset saved: ${name}`);
    await this.scheduleAutoSave();
  }

  async loadPreset(name: string): Promise<AgentViewPreset | null> {
    const preset = this.presets.presets[name];
    if (!preset) {
      logger.warn(`Preset not found: ${name}`);
      return null;
    }
    this.presets.lastPreset = name;
    logger.info(`Preset loaded: ${name}`);
    return preset;
  }

  async deletePreset(name: string): Promise<boolean> {
    if (!this.presets.presets[name]) {
      logger.warn(`Cannot delete non-existent preset: ${name}`);
      return false;
    }

    delete this.presets.presets[name];
    if (this.presets.lastPreset === name) {
      this.presets.lastPreset = undefined;
    }
    this.dirty = true;
    logger.info(`Preset deleted: ${name}`);
    await this.scheduleAutoSave();
    return true;
  }

  listPresets(): AgentViewPreset[] {
    return Object.values(this.presets.presets).sort((a, b) => b.updatedAt - a.updatedAt);
  }

  getPresetNames(): string[] {
    return Object.keys(this.presets.presets);
  }

  getLastPreset(): string | undefined {
    return this.presets.lastPreset;
  }

  hasPreset(name: string): boolean {
    return name in this.presets.presets;
  }

  private async scheduleAutoSave(): Promise<void> {
    if (this.autoSaveTimer) {
      clearTimeout(this.autoSaveTimer);
    }

    this.autoSaveTimer = setTimeout(() => {
      this.save().catch(err => logger.error('Auto-save failed', err));
    }, this.autoSaveInterval);
  }

  private async migrate(data: AgentViewPresets): Promise<void> {
    logger.info('Migrating presets to latest version');
    this.presets = {
      version: PRESETS_VERSION,
      presets: data.presets,
      lastPreset: data.lastPreset,
    };
    this.dirty = true;
  }

  dispose(): void {
    if (this.autoSaveTimer) {
      clearTimeout(this.autoSaveTimer);
    }
  }
}
