/**
 * 八字状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { BaziProfile } from '@/types'
import {
  getBaziProfiles,
  getBaziProfile,
  calculateBazi,
  deleteBaziProfile
} from '@/api'

export const useBaziStore = defineStore('bazi', () => {
  // 状态
  const profiles = ref<BaziProfile[]>([])
  const currentProfile = ref<BaziProfile | null>(null)
  const loading = ref(false)

  /**
   * 加载档案列表
   */
  async function loadProfiles() {
    try {
      loading.value = true
      profiles.value = await getBaziProfiles()
    } catch (error) {
      console.error('加载档案列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取档案详情
   */
  async function loadProfile(id: string) {
    try {
      loading.value = true
      currentProfile.value = await getBaziProfile(id)
      return currentProfile.value
    } catch (error) {
      console.error('获取档案详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 计算并保存八字
   */
  async function calculate(data: {
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
    try {
      loading.value = true
      const profile = await calculateBazi(data)
      profiles.value.unshift(profile)
      currentProfile.value = profile
      return profile
    } catch (error) {
      console.error('计算八字失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 删除档案
   */
  async function removeProfile(id: string) {
    try {
      await deleteBaziProfile(id)
      profiles.value = profiles.value.filter(p => p.id !== id)
      if (currentProfile.value?.id === id) {
        currentProfile.value = null
      }
    } catch (error) {
      console.error('删除档案失败:', error)
      throw error
    }
  }

  return {
    profiles,
    currentProfile,
    loading,
    loadProfiles,
    loadProfile,
    calculate,
    removeProfile
  }
})

