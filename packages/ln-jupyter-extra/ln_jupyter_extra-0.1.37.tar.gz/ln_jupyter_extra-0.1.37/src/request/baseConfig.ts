/**
 * axios 基础配置
 */
import type { AxiosRequestConfig } from 'axios';

// 基础配置
export const baseConfig: AxiosRequestConfig = {
  baseURL: window.location.origin,
  timeout: 1000 * 60 * 5
};
