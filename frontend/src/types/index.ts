/**
 * 全局类型定义
 */

// 用户类型
export interface User {
  id: string
  openid?: string
  nickname?: string
  avatar_url?: string
  gender?: string
  birth_info?: any
  token_balance: number
  created_at: string
}

// 会话类型
export interface Conversation {
  id: string
  user_id: string
  title: string
  bazi_profile_id?: string
  context_size: number
  ai_style: string
  created_at: string
  updated_at?: string
}

// 消息类型
export type MessageRole = 'user' | 'assistant' | 'system'

export interface Message {
  id: string
  conversation_id: string
  role: MessageRole
  content: string
  token_cost: number
  created_at: string
}

// 八字档案类型
export interface BaziProfile {
  id: string
  user_id: string
  name: string
  gender: string
  birth_info: {
    calendar: string
    year: number
    month: number
    day: number
    hour: number
    minute: number
    birth_city: string
    current_city?: string
  }
  bazi_result: {
    bazi: string
    jieqi_info: string
    dayun_info: string
    formatted_output: string
  }
  created_at: string
}

// 订单类型
export interface Order {
  id: string
  user_id: string
  amount: number
  token_amount: number
  status: 'pending' | 'paid' | 'failed' | 'refunded'
  payment_id?: string
  trade_no: string
  created_at: string
  paid_at?: string
}

// API响应类型
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 分页响应类型
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

