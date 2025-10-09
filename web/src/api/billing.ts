/**
 * 计费相关API
 */
import { get, post } from '@/utils/request'

export interface BalanceInfo {
  balance: number
  user_id: number
}

export interface Transaction {
  id: number
  user_id: number
  type: string
  amount: number
  balance_after?: number
  description?: string
  reference_id?: string
  created_at: string
}

export interface RechargeResponse {
  order_no: string
  amount: number
  tokens: number
  payment_params?: any
}

/**
 * 查询余额
 */
export function getBalance() {
  return get<BalanceInfo>('/api/v1/billing/balance')
}

/**
 * 获取交易记录
 */
export function getTransactions(limit = 20, offset = 0) {
  return get<Transaction[]>('/api/v1/billing/transactions', { limit, offset })
}

/**
 * 发起充值
 */
export function createRecharge(amount: number, paymentMethod = 'wechat') {
  return post<RechargeResponse>('/api/v1/billing/recharge', {
    amount,
    payment_method: paymentMethod
  })
}

