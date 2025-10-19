/**
 * API请求封装
 */
import { storage } from '@/utils/storage'
import type { ApiResponse } from '@/types'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: any
  needAuth?: boolean
}

/**
 * 统一请求方法
 */
export async function request<T = any>(options: RequestOptions): Promise<T> {
  const { url, method = 'GET', data, header = {}, needAuth = true } = options

  // 添加认证token
  if (needAuth) {
    const token = storage.getToken()
    if (token) {
      header['Authorization'] = `Bearer ${token}`
    }
  }

  // 开发环境打印请求信息
  console.log('🚀 API请求:', method, url, data)

  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        ...header
      },
      success: (res) => {
        console.log('📥 API响应:', res.statusCode, url, res.data)
        
        if (res.statusCode === 200) {
          resolve(res.data as T)
        } else if (res.statusCode === 401 || res.statusCode === 403) {
          // Token过期或未认证，跳转登录
          storage.clear()
          uni.reLaunch({
            url: '/pages/login/index'
          })
          reject(new Error('登录已过期，请重新登录'))
        } else if (res.statusCode === 402) {
          // Token余额不足
          uni.showModal({
            title: '提示',
            content: 'Token余额不足，请充值',
            confirmText: '去充值',
            success: (res) => {
              if (res.confirm) {
                uni.navigateTo({
                  url: '/pages/recharge/index'
                })
              }
            }
          })
          reject(new Error('Token余额不足'))
        } else {
          // 尝试从响应中提取错误信息
          const errorMsg = (res.data as any)?.detail || (res.data as any)?.message || '请求失败'
          console.error('❌ API错误:', res.statusCode, errorMsg, res.data)
          uni.showToast({
            title: errorMsg,
            icon: 'none',
            duration: 3000
          })
          reject(new Error(errorMsg))
        }
      },
      fail: (err) => {
        console.error('❌ 网络错误:', err)
        uni.showToast({
          title: '网络错误',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

/**
 * GET请求
 */
export function get<T = any>(url: string, data?: any): Promise<T> {
  return request<T>({
    url: data ? `${url}?${new URLSearchParams(data).toString()}` : url,
    method: 'GET'
  })
}

/**
 * POST请求
 */
export function post<T = any>(url: string, data?: any): Promise<T> {
  return request<T>({
    url,
    method: 'POST',
    data
  })
}

/**
 * PUT请求
 */
export function put<T = any>(url: string, data?: any): Promise<T> {
  return request<T>({
    url,
    method: 'PUT',
    data
  })
}

/**
 * DELETE请求
 */
export function del<T = any>(url: string): Promise<T> {
  return request<T>({
    url,
    method: 'DELETE'
  })
}

