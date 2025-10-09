/**
 * 对话相关API
 */
import { get, post, del } from '@/utils/request'

export interface ChatSession {
  id: number
  user_id: number
  title?: string
  status: string
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: number
  session_id: number
  role: string
  content: string
  tokens_used: number
  model?: string
  created_at: string
}

export interface ChatHistory {
  session: ChatSession
  messages: ChatMessage[]
}

/**
 * 创建会话
 */
export function createSession(title?: string) {
  return post<ChatSession>('/api/v1/chat/sessions', { title })
}

/**
 * 获取会话列表
 */
export function getSessions() {
  return get<ChatSession[]>('/api/v1/chat/sessions')
}

/**
 * 获取会话详情
 */
export function getSession(sessionId: number) {
  return get<ChatHistory>(`/api/v1/chat/sessions/${sessionId}`)
}

/**
 * 删除会话
 */
export function deleteSession(sessionId: number) {
  return del(`/api/v1/chat/sessions/${sessionId}`)
}

/**
 * 发送消息
 */
export function sendMessage(sessionId: number, content: string) {
  return post<ChatMessage>('/api/v1/chat/messages', {
    session_id: sessionId,
    content
  })
}

