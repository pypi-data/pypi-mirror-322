/**
 * axios 基础配置
 */
import type { AxiosRequestConfig } from 'axios';
import { getApiBaseUrl } from '../utils/settings';

let baseConfig: AxiosRequestConfig = {
  baseURL: window.location.origin,
  timeout: 60000 // 超时时间
};

// 初始化基础配置
export async function initializeBaseConfig() {
  const apiBaseUrl = await getApiBaseUrl();
  baseConfig = {
    ...baseConfig,
    baseURL: apiBaseUrl
  };
}

// 导出基础配置
export { baseConfig };
