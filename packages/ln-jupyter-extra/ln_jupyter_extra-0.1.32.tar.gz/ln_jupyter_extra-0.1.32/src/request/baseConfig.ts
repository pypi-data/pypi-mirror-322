/**
 * axios 基础配置
 */
import type { AxiosRequestConfig } from 'axios';
import { getApiBaseUrl } from '../utils/settings';

// 基础配置
export let baseConfig: AxiosRequestConfig = {
  baseURL: window.location.origin,
  timeout: 1000 * 60 * 5
};

// 初始化基础配置
export async function initializeBaseConfig() {
  const baseUrl = await getApiBaseUrl();
  baseConfig = {
    ...baseConfig,
    baseURL: baseUrl
  };
  return baseConfig;
}
