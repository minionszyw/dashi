/**
 * 对话相关API
 */
import { get, post, put, del } from './request'
import type { Conversation, Message } from '@/types'

/**
 * 创建会话
 */
export function createConversation(data: {
  title?: string
  bazi_profile_id?: string
  context_size?: number
  ai_style?: string
}) {
  return post<Conversation>('/api/v1/chat/conversations', data)
}

/**
 * 获取会话列表
 */
export function getConversations(params?: { skip?: number; limit?: number }) {
  return get<Conversation[]>('/api/v1/chat/conversations', params)
}

/**
 * 获取会话详情
 */
export function getConversation(id: string) {
  return get<Conversation>(`/api/v1/chat/conversations/${id}`)
}

/**
 * 更新会话
 */
export function updateConversation(id: string, data: Partial<Conversation>) {
  return put<Conversation>(`/api/v1/chat/conversations/${id}`, data)
}

/**
 * 删除会话
 */
export function deleteConversation(id: string) {
  return del(`/api/v1/chat/conversations/${id}`)
}

/**
 * 获取会话历史
 */
export function getChatHistory(conversationId: string, params?: { skip?: number; limit?: number }) {
  return get<{
    conversation: Conversation
    messages: Message[]
    total: number
  }>(`/api/v1/chat/history/${conversationId}`, params)
}

