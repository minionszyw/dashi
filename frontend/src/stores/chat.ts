/**
 * 对话状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Conversation, Message } from '@/types'
import {
  getConversations,
  getConversation,
  createConversation,
  updateConversation,
  deleteConversation,
  getChatHistory
} from '@/api'

export const useChatStore = defineStore('chat', () => {
  // 状态
  const conversations = ref<Conversation[]>([])
  const currentConversation = ref<Conversation | null>(null)
  const messages = ref<Message[]>([])
  const loading = ref(false)

  /**
   * 加载会话列表
   */
  async function loadConversations() {
    try {
      loading.value = true
      conversations.value = await getConversations()
    } catch (error) {
      console.error('加载会话列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 创建新会话
   */
  async function newConversation(data?: {
    title?: string
    bazi_profile_id?: string
  }) {
    try {
      const conversation = await createConversation(data || {})
      conversations.value.unshift(conversation)
      currentConversation.value = conversation
      messages.value = []
      return conversation
    } catch (error) {
      console.error('创建会话失败:', error)
      throw error
    }
  }

  /**
   * 切换当前会话
   */
  async function switchConversation(conversationId: string) {
    try {
      loading.value = true
      const result = await getChatHistory(conversationId)
      currentConversation.value = result.conversation
      messages.value = result.messages
    } catch (error) {
      console.error('切换会话失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新会话标题
   */
  async function updateConversationTitle(conversationId: string, title: string) {
    try {
      const updated = await updateConversation(conversationId, { title })
      const index = conversations.value.findIndex(c => c.id === conversationId)
      if (index !== -1) {
        conversations.value[index] = updated
      }
      if (currentConversation.value?.id === conversationId) {
        currentConversation.value = updated
      }
    } catch (error) {
      console.error('更新会话标题失败:', error)
      throw error
    }
  }

  /**
   * 删除会话
   */
  async function removeConversation(conversationId: string) {
    try {
      await deleteConversation(conversationId)
      conversations.value = conversations.value.filter(c => c.id !== conversationId)
      if (currentConversation.value?.id === conversationId) {
        currentConversation.value = null
        messages.value = []
      }
    } catch (error) {
      console.error('删除会话失败:', error)
      throw error
    }
  }

  /**
   * 添加消息到当前会话
   */
  function addMessage(message: Message) {
    messages.value.push(message)
  }

  /**
   * 添加用户消息
   */
  function addUserMessage(content: string): Message {
    const message: Message = {
      id: `temp_${Date.now()}`,
      conversation_id: currentConversation.value?.id || '',
      role: 'user',
      content,
      token_cost: 0,
      created_at: new Date().toISOString()
    }
    addMessage(message)
    return message
  }

  /**
   * 添加AI消息（流式）
   */
  function addAIMessage(content: string = ''): Message {
    const message: Message = {
      id: `temp_ai_${Date.now()}`,
      conversation_id: currentConversation.value?.id || '',
      role: 'assistant',
      content,
      token_cost: 0,
      created_at: new Date().toISOString()
    }
    addMessage(message)
    return message
  }

  /**
   * 更新AI消息内容（流式追加）
   */
  function appendAIMessageContent(messageId: string, content: string) {
    const message = messages.value.find(m => m.id === messageId)
    if (message) {
      message.content += content
    }
  }

  /**
   * 完成AI消息（更新ID和token消耗）
   */
  function finalizeAIMessage(tempId: string, realId: string, tokenCost: number) {
    const message = messages.value.find(m => m.id === tempId)
    if (message) {
      message.id = realId
      message.token_cost = tokenCost
    }
  }

  /**
   * 清空当前会话
   */
  function clearCurrent() {
    currentConversation.value = null
    messages.value = []
  }

  return {
    conversations,
    currentConversation,
    messages,
    loading,
    loadConversations,
    newConversation,
    switchConversation,
    updateConversationTitle,
    removeConversation,
    addMessage,
    addUserMessage,
    addAIMessage,
    appendAIMessageContent,
    finalizeAIMessage,
    clearCurrent
  }
})

