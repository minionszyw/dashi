/**
 * 八字相关API
 */
import { get, post, del } from './request'
import type { BaziProfile } from '@/types'

/**
 * 计算八字
 */
export function calculateBazi(data: {
  name: string
  gender: string
  calendar: string
  year: number
  month: number
  day: number
  hour: number
  minute: number
  birth_city: string
  current_city?: string
}) {
  return post<BaziProfile>('/api/v1/bazi/calculate', data)
}

/**
 * 获取八字档案列表
 */
export function getBaziProfiles() {
  return get<BaziProfile[]>('/api/v1/bazi/profiles')
}

/**
 * 获取八字档案详情
 */
export function getBaziProfile(id: string) {
  return get<BaziProfile>(`/api/v1/bazi/profiles/${id}`)
}

/**
 * 删除八字档案
 */
export function deleteBaziProfile(id: string) {
  return del(`/api/v1/bazi/profiles/${id}`)
}

