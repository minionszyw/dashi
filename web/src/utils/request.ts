/**
 * 网络请求封装
 */

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: any
}

interface ResponseData<T = any> {
  code: number
  message: string
  data: T
  timestamp: number
}

// API基础URL
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * 统一请求方法
 */
export function request<T = any>(options: RequestOptions): Promise<ResponseData<T>> {
  const { url, method = 'GET', data, header = {} } = options

  // 获取token
  const token = uni.getStorageSync('token')
  if (token) {
    header.Authorization = `Bearer ${token}`
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        ...header
      },
      success: (res: any) => {
        const response = res.data as ResponseData<T>
        
        if (response.code === 0) {
          resolve(response)
        } else if (res.statusCode === 401) {
          // 未授权，跳转登录
          uni.removeStorageSync('token')
          uni.removeStorageSync('userInfo')
          uni.reLaunch({
            url: '/pages/login/login'
          })
          reject(new Error('未授权，请重新登录'))
        } else {
          uni.showToast({
            title: response.message || '请求失败',
            icon: 'none'
          })
          reject(new Error(response.message))
        }
      },
      fail: (err) => {
        uni.showToast({
          title: '网络请求失败',
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
export function get<T = any>(url: string, data?: any): Promise<ResponseData<T>> {
  return request<T>({ url, method: 'GET', data })
}

/**
 * POST请求
 */
export function post<T = any>(url: string, data?: any): Promise<ResponseData<T>> {
  return request<T>({ url, method: 'POST', data })
}

/**
 * PUT请求
 */
export function put<T = any>(url: string, data?: any): Promise<ResponseData<T>> {
  return request<T>({ url, method: 'PUT', data })
}

/**
 * DELETE请求
 */
export function del<T = any>(url: string, data?: any): Promise<ResponseData<T>> {
  return request<T>({ url, method: 'DELETE', data })
}

