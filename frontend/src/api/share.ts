/**
 * 分享相关API
 */
import { request } from './request'

/**
 * 生成小程序码
 */
export function generateMiniProgramCode(conversationId: string) {
  return request<{ image_base64: string; conversation_id: string }>({
    url: '/api/v1/share/miniprogram-code',
    method: 'POST',
    data: {
      conversation_id: conversationId,
      page: 'pages/session/index'  // 使用TabBar页面，扫码后可以看到会话列表
    }
  })
}

