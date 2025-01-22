import { ISettingRegistry } from '@jupyterlab/settingregistry';

// 插件ID
const PLUGIN_ID = 'ln-jupyter-extra:plugin';

// 设置管理器实例
let settingRegistry: ISettingRegistry | null = null;

export interface IApiConfig {
  baseUrl?: string;
  authToken?: string;
}

/**
 * 初始化设置管理器
 */
export function initializeSettings(registry: ISettingRegistry) {
  settingRegistry = registry;
}

/**
 * 保存API配置
 */
export async function saveApiConfig(config: IApiConfig): Promise<void> {
  if (!settingRegistry) {
    return;
  }

  try {
    const settings = await settingRegistry.load(PLUGIN_ID);
    const currentConfig =
      (settings.get('apiConfig').composite as IApiConfig) || {};

    await settings.set('apiConfig', {
      ...currentConfig,
      ...config
    });
  } catch (error) {
    console.error('Failed to save API config:', error);
  }
}

/**
 * 获取API配置
 */
export async function getApiConfig(): Promise<IApiConfig> {
  if (!settingRegistry) {
    return {};
  }

  try {
    const settings = await settingRegistry.load(PLUGIN_ID);
    return (settings.get('apiConfig').composite as IApiConfig) || {};
  } catch (error) {
    console.error('Failed to get API config:', error);
    return {};
  }
}

/**
 * 获取API基础URL
 */
export async function getApiBaseUrl(): Promise<string> {
  // 优先从URL获取
  const url = new URL(window.location.href);
  const typeFromUrl = url.searchParams.get('type');
  if (typeFromUrl) {
    return typeFromUrl;
  }
  const config = await getApiConfig();
  return config.baseUrl || window.location.origin;
}

/**
 * 获取认证Token
 */
export async function getAuthToken(): Promise<string | undefined> {
  // 优先从URL获取
  const url = new URL(window.location.href);
  const authFromUrl = url.searchParams.get('auth');
  if (authFromUrl) {
    return authFromUrl;
  }
  // 从设置中获取
  const config = await getApiConfig();
  return config.authToken;
}

/**
 * 清除API配置
 */
export async function clearApiConfig(): Promise<void> {
  if (!settingRegistry) {
    return;
  }

  try {
    const settings = await settingRegistry.load(PLUGIN_ID);
    await settings.set('apiConfig', {});
  } catch (error) {
    console.error('Failed to clear API config:', error);
  }
}
