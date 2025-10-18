/**
 * 格式化工具函数
 */

/**
 * 格式化时间戳
 */
export function formatTime(timestamp: string): string {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour

  if (diff < minute) {
    return '刚刚'
  } else if (diff < hour) {
    return `${Math.floor(diff / minute)}分钟前`
  } else if (diff < day) {
    return `${Math.floor(diff / hour)}小时前`
  } else if (diff < 2 * day) {
    return '昨天 ' + formatDateTime(timestamp, 'HH:mm')
  } else if (diff < 7 * day) {
    return `${Math.floor(diff / day)}天前`
  } else {
    return formatDateTime(timestamp, 'MM-DD HH:mm')
  }
}

/**
 * 格式化日期时间
 */
export function formatDateTime(timestamp: string, format: string = 'YYYY-MM-DD HH:mm:ss'): string {
  const date = new Date(timestamp)
  
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')
  const second = String(date.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', String(year))
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hour)
    .replace('mm', minute)
    .replace('ss', second)
}

/**
 * 格式化Token数量
 */
export function formatTokenBalance(balance: number): string {
  if (balance >= 10000) {
    return `${(balance / 10000).toFixed(1)}万`
  }
  return String(balance)
}

/**
 * 格式化金额
 */
export function formatAmount(amount: number): string {
  return `¥${amount.toFixed(2)}`
}

