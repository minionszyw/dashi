/**
 * 文件上传API
 */
import { storage } from '@/utils/storage'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * 上传头像
 */
export function uploadAvatar(filePath: string): Promise<{ avatar_url: string; message: string }> {
  const token = storage.getToken()
  
  return new Promise((resolve, reject) => {
    console.log('🚀 上传头像:', filePath)
    
    uni.uploadFile({
      url: `${BASE_URL}/api/v1/user/upload-avatar`,
      filePath,
      name: 'file',
      header: {
        'Authorization': `Bearer ${token}`
      },
      success: (res) => {
        console.log('📥 上传响应:', res.statusCode, res.data)
        
        if (res.statusCode === 200) {
          const data = JSON.parse(res.data)
          resolve(data)
        } else {
          const errorData = JSON.parse(res.data)
          const errorMsg = errorData.detail || '上传失败'
          uni.showToast({
            title: errorMsg,
            icon: 'none'
          })
          reject(new Error(errorMsg))
        }
      },
      fail: (err) => {
        console.error('❌ 上传失败:', err)
        uni.showToast({
          title: '上传失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

