<template>
  <div class="chat-container">
    <el-container class="app-shell">
      <el-aside width="260px" class="sidebar">
        <div class="sidebar-header">
          <div class="brand">
            <div class="brand-logo" aria-label="Cloud Agent mascot">
              <svg class="monster-icon" viewBox="0 0 48 48" role="img" aria-hidden="true">
                <defs>
                  <linearGradient id="monsterBody" x1="10" y1="8" x2="40" y2="42" gradientUnits="userSpaceOnUse">
                    <stop offset="0" stop-color="#7dd3fc" />
                    <stop offset="0.55" stop-color="#38bdf8" />
                    <stop offset="1" stop-color="#2563eb" />
                  </linearGradient>
                  <linearGradient id="monsterHorn" x1="12" y1="6" x2="36" y2="18" gradientUnits="userSpaceOnUse">
                    <stop offset="0" stop-color="#ccfbf1" />
                    <stop offset="1" stop-color="#14b8a6" />
                  </linearGradient>
                </defs>
                <path d="M14.4 17.8 10.6 9.6a1.4 1.4 0 0 1 2-1.76l7.48 4.36Z" fill="url(#monsterHorn)" />
                <path d="M33.6 17.8 37.4 9.6a1.4 1.4 0 0 0-2-1.76l-7.48 4.36Z" fill="url(#monsterHorn)" />
                <rect x="8" y="12" width="32" height="30" rx="12" fill="url(#monsterBody)" />
                <path d="M12 26c0-7.18 4.92-11 12-11s12 3.82 12 11" fill="rgba(255,255,255,0.2)" />
                <circle cx="18.5" cy="27" r="3" fill="#f8fbff" />
                <circle cx="29.5" cy="27" r="3" fill="#f8fbff" />
                <circle cx="19.4" cy="27.4" r="1.1" fill="#075985" />
                <circle cx="28.6" cy="27.4" r="1.1" fill="#075985" />
                <path d="M20 34.2c2.16 1.62 5.84 1.62 8 0" fill="none" stroke="#e0f2fe" stroke-width="2" stroke-linecap="round" />
              </svg>
            </div>
            <h2>Cloud Agent</h2>
          </div>
          <el-button type="primary" :icon="Plus" circle @click="createNewSession" />
        </div>
        <div class="session-list">
          <div 
            v-for="session in sessions" 
            :key="session.id"
            :class="['session-item', { active: currentSessionId === session.id }]"
            @click="switchSession(session.id)"
          >
            <el-icon><ChatDotRound /></el-icon>
            <span class="session-name">{{ session.name }}</span>
          </div>
        </div>
        <div class="user-info">
          <div class="mini-avatar user-avatar">U</div>
          <span class="username">{{ currentUserId }}</span>
        </div>
      </el-aside>

      <el-main class="chat-main">
        <div class="chat-header">
          <div class="header-title">企业云智能客服</div>
          <div class="header-subtitle">Multi-Agent · Billing · Promotion · FinOps</div>
        </div>
        <div class="message-list" ref="messageListRef">
          <div v-if="messages.length === 0" class="empty-state">
            <el-icon size="64" color="#409EFC"><Service /></el-icon>
            <h3 class="welcome-title">欢迎使用云平台智能客服</h3>
            <p class="welcome-desc">我是您的专属 AI 助手，您可以直接向我提问，或者尝试以下典型场景：</p>
            
            <div class="scenario-container">
              <el-row :gutter="20">
                <el-col :span="12">
                  <div class="scenario-card">
                    <div class="card-header">
                      <el-icon><Monitor /></el-icon>
                      <span>产品咨询与推荐</span>
                    </div>
                    <div class="scenario-list">
                      <div class="scenario-item" @click="sendQuery('云服务器ECS有哪些基本属性？')">云服务器ECS有哪些基本属性？</div>
                      <div class="scenario-item" @click="sendQuery('我是Java接口服务+MySQL，8核16G够吗？推荐具体实例型号。')">Java服务+MySQL，推荐具体实例型号</div>
                    </div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="scenario-card">
                    <div class="card-header">
                      <el-icon><List /></el-icon>
                      <span>账单与实例查询</span>
                    </div>
                    <div class="scenario-list">
                      <div class="scenario-item" @click="sendQuery('帮我查一下我最近的订单记录')">帮我查一下我最近的订单记录</div>
                      <div class="scenario-item" @click="sendQuery('查询我名下的所有运行中的实例')">查询我名下的所有运行中的实例</div>
                    </div>
                  </div>
                </el-col>
              </el-row>
              <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :span="12">
                  <div class="scenario-card">
                    <div class="card-header">
                      <el-icon><DataLine /></el-icon>
                      <span>资源优化与降本</span>
                    </div>
                    <div class="scenario-list">
                      <div class="scenario-item primary" @click="loadFinOpsReport">生成结构化成本优化报告</div>
                      <div class="scenario-item" @click="sendQuery('获取近7天CPU/内存/带宽数据并做降本建议')">获取近7天资源监控并做降本建议</div>
                      <div class="scenario-item" @click="sendQuery('服务器利用率低，怎么省钱？')">服务器利用率低，怎么省钱？</div>
                    </div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="scenario-card">
                    <div class="card-header">
                      <el-icon><Share /></el-icon>
                      <span>产品推广活动</span>
                    </div>
                    <div class="scenario-list">
                      <div class="scenario-item" @click="sendQuery('我想推广云服务器ECS，有海报吗？')">我想推广云服务器ECS，有海报吗？</div>
                      <div class="scenario-item" @click="sendQuery('帮我生成一张 c7 计算型的推广海报')">帮我生成一张 c7 计算型的推广海报</div>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>

          <div 
            v-for="(msg, index) in messages" 
            :key="index"
            :class="['message-row', msg.role]"
          >
            <div :class="['msg-avatar', msg.role === 'user' ? 'user-avatar' : 'ai-avatar']">
              {{ msg.role === 'user' ? 'U' : 'AI' }}
            </div>
            <div class="message-bubble" v-html="renderMarkdown(msg.content)"></div>
          </div>

          <FinOpsReport v-if="finOpsReport" :report="finOpsReport" />
          
          <div v-if="isLoading" class="message-row assistant">
             <div class="msg-avatar ai-avatar">AI</div>
             <div class="message-bubble loading">
               <el-icon class="is-loading"><Loading /></el-icon> 正在思考与调用工具中...
             </div>
          </div>
        </div>

        <div class="input-area">
          <el-input
            v-model="inputQuery"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题，Shift + Enter 换行，Enter 发送"
            @keydown.enter.prevent="handleEnter"
            :disabled="isLoading"
          />
          <el-button 
            type="primary" 
            class="send-btn" 
            :icon="Position" 
            :loading="isLoading"
            @click="sendQuery(inputQuery)"
            :disabled="!inputQuery.trim()"
          >
            发送
          </el-button>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { Plus, ChatDotRound, Service, Position, Loading, Monitor, List, DataLine, Share } from '@element-plus/icons-vue'
import { marked } from 'marked'
import FinOpsReport from './components/FinOpsReport.vue'
import type { FinOpsReport as FinOpsReportData, FinOpsReportResponse } from './types/finops'

// 状态定义
const inputQuery = ref('')
const isLoading = ref(false)
const messageListRef = ref<HTMLElement | null>(null)
const currentSessionId = ref('session_default_1')
const finOpsReport = ref<FinOpsReportData | null>(null)
const currentUserId = '芝加哥斯拉'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const messages = ref<Message[]>([])
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5001'

const sessions = ref([
  { id: 'session_default_1', name: '新对话' }
])

// 初始化
onMounted(() => {
  // 可以从 localStorage 恢复数据
})

const createNewSession = () => {
  const newId = `session_${Date.now()}`
  sessions.value.unshift({ id: newId, name: '新对话' })
  currentSessionId.value = newId
  messages.value = []
  finOpsReport.value = null
}

const switchSession = (id: string) => {
  if (currentSessionId.value === id) return
  currentSessionId.value = id
  messages.value = [] // 实际应从本地或后端拉取该 session 的历史
  finOpsReport.value = null
}

const renderMarkdown = (text: string) => {
  return marked(text)
}

const scrollToBottom = async () => {
  await nextTick()
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const handleEnter = (e: KeyboardEvent) => {
  if (e.shiftKey) return
  if (inputQuery.value.trim() && !isLoading.value) {
    sendQuery(inputQuery.value)
  }
}

const sendQuery = async (query: string) => {
  if (!query.trim()) return
  
  const text = query.trim()
  inputQuery.value = ''
  
  // 添加用户消息
  messages.value.push({ role: 'user', content: text })
  scrollToBottom()
  
  isLoading.value = true
  
  // 预先创建一个空的助手消息，用于接收流式数据
  const assistantMessage: Message = { role: 'assistant', content: '' }
  messages.value.push(assistantMessage)
  const currentMsgIndex = messages.value.length - 1
  
  try {
    // 调用 FastAPI 后端接口并使用 fetch 接收 SSE 流
    const response = await fetch(`${apiBaseUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: text,
        user_id: currentUserId,
        session_id: currentSessionId.value
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    const decoder = new TextDecoder('utf-8')
    isLoading.value = false // 开始接收流，关闭 loading 状态

    if (reader) {
      let buffer = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || '' // 将不完整的一行保留到下一次循环

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6).trim()
            if (dataStr === '[DONE]') continue
            if (!dataStr) continue
            
            try {
              const data = JSON.parse(dataStr)
              if (data.content && messages.value[currentMsgIndex]) {
                messages.value[currentMsgIndex].content += data.content
                scrollToBottom()
              }
              if (data.done) {
                // 流传输完成
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e, dataStr)
            }
          }
        }
      }
    }
  } catch (error) {
    console.error('API Error:', error)
    if (messages.value[currentMsgIndex]) {
      messages.value[currentMsgIndex].content = '❌ 请求失败，请检查后端服务是否启动 (FastAPI port 5001)。'
    }
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const loadFinOpsReport = async () => {
  isLoading.value = true
  finOpsReport.value = null
  messages.value.push({ role: 'user', content: '生成一份结构化云资源成本优化报告' })
  scrollToBottom()

  try {
    const response = await fetch(`${apiBaseUrl}/api/finops/report`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: currentUserId,
        billing_month: '2026-05',
        target_instance_type: 'ecs.g8a.xlarge'
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const payload = (await response.json()) as FinOpsReportResponse
    finOpsReport.value = payload.data
    messages.value.push({
      role: 'assistant',
      content: `已生成 ${payload.data.summary.billing_month} 的结构化 FinOps 报告，预计月节省 ${payload.data.summary.currency} ${payload.data.summary.estimated_monthly_savings.toLocaleString('zh-CN')}。`
    })
  } catch (error) {
    console.error('FinOps report error:', error)
    messages.value.push({
      role: 'assistant',
      content: '❌ 成本优化报告生成失败，请确认后端服务是否启动。'
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.chat-container {
  height: 100vh;
  width: 100vw;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.96) 0%, rgba(241, 248, 255, 0.92) 48%, rgba(231, 244, 255, 0.86) 100%);
  overflow: hidden;
  padding: 16px;
  box-sizing: border-box;
}
.app-shell {
  height: 100%;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(191, 219, 254, 0.62);
  box-shadow: 0 24px 70px rgba(30, 64, 175, 0.11);
  background: rgba(255, 255, 255, 0.76);
  backdrop-filter: blur(18px);
}
.sidebar {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.86) 0%, rgba(232, 244, 255, 0.78) 100%);
  border-right: 1px solid rgba(147, 197, 253, 0.28);
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(20px);
}
.sidebar-header {
  padding: 18px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(191, 219, 254, 0.42);
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-logo {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(224, 242, 254, 0.78));
  border: 1px solid rgba(125, 211, 252, 0.58);
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.16);
}
.monster-icon {
  width: 34px;
  height: 34px;
  display: block;
}
.sidebar-header h2 {
  margin: 0;
  font-size: 16px;
  color: #0f172a;
  letter-spacing: 0;
}
.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}
.session-item {
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #475569;
  transition: all 0.3s;
  border: 1px solid rgba(191, 219, 254, 0);
}
.session-item:hover {
  background-color: rgba(239, 246, 255, 0.88);
  border-color: rgba(147, 197, 253, 0.4);
}
.session-item.active {
  background: rgba(219, 234, 254, 0.72);
  color: #1d4ed8;
  font-weight: 500;
  border-color: rgba(96, 165, 250, 0.42);
}
.user-info {
  padding: 16px;
  border-top: 1px solid rgba(191, 219, 254, 0.42);
  display: flex;
  align-items: center;
  gap: 10px;
}
.username {
  font-weight: 600;
  color: #334155;
}

.chat-main {
  display: flex;
  flex-direction: column;
  padding: 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.74) 0%, rgba(244, 250, 255, 0.84) 100%);
}
.chat-header {
  padding: 16px 28px 12px;
  border-bottom: 1px solid rgba(191, 219, 254, 0.48);
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(16px);
}
.header-title {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}
.header-subtitle {
  margin-top: 4px;
  color: #64748b;
  font-size: 13px;
}
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 24px 28px;
  scroll-behavior: smooth;
}
.empty-state {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #64748b;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(191, 219, 254, 0.48);
  border-radius: 10px;
  padding: 40px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(16px);
}
.welcome-title {
  margin-top: 16px;
  margin-bottom: 8px;
  color: #1e293b;
  font-size: 24px;
  font-weight: 600;
}
.welcome-desc {
  margin-bottom: 32px;
  color: #64748b;
  font-size: 15px;
}
.scenario-container {
  width: 100%;
  max-width: 800px;
}
.scenario-card {
  background: rgba(255, 255, 255, 0.66);
  border: 1px solid rgba(191, 219, 254, 0.54);
  border-radius: 8px;
  padding: 20px;
  height: 100%;
  transition: all 0.3s ease;
  box-shadow: 0 10px 28px rgba(37, 99, 235, 0.06);
  backdrop-filter: blur(14px);
}
.scenario-card:hover {
  box-shadow: 0 16px 36px rgba(37, 99, 235, 0.1);
  border-color: rgba(96, 165, 250, 0.58);
}
.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 16px;
}
.card-header .el-icon {
  color: #3b82f6;
  font-size: 20px;
}
.scenario-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.scenario-item {
  background: rgba(255, 255, 255, 0.84);
  border: 1px solid rgba(203, 213, 225, 0.68);
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 14px;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}
.scenario-item:hover {
  background: rgba(239, 246, 255, 0.94);
  border-color: rgba(96, 165, 250, 0.72);
  color: #1d4ed8;
  transform: translateY(-2px);
}
.scenario-item.primary {
  border-color: rgba(56, 189, 248, 0.55);
  background: linear-gradient(135deg, rgba(239, 246, 255, 0.98), rgba(224, 242, 254, 0.82));
  color: #075985;
  font-weight: 700;
}
.scenario-item.primary:hover {
  border-color: rgba(14, 165, 233, 0.72);
  background: linear-gradient(135deg, rgba(224, 242, 254, 0.98), rgba(204, 251, 241, 0.72));
  color: #0f766e;
}

.message-row {
  display: flex;
  gap: 12px;
  margin-bottom: 18px;
  max-width: 86%;
  align-items: flex-start;
}
.message-row.user {
  flex-direction: row-reverse;
  margin-left: auto;
}
.msg-avatar {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}
.user-avatar {
  color: #eff6ff;
  background: linear-gradient(135deg, #60a5fa, #2563eb);
}
.ai-avatar {
  color: #f8fafc;
  background: linear-gradient(135deg, #38bdf8, #14b8a6);
}
.mini-avatar {
  width: 28px;
  height: 28px;
  border-radius: 9px;
  display: grid;
  place-items: center;
  font-size: 11px;
  font-weight: 700;
}
.message-bubble {
  background: rgba(255, 255, 255, 0.9);
  padding: 13px 16px;
  border-radius: 10px;
  border: 1px solid rgba(191, 219, 254, 0.48);
  box-shadow: 0 10px 26px rgba(37, 99, 235, 0.06);
  line-height: 1.6;
  color: #1e293b;
  font-size: 15px;
  backdrop-filter: blur(12px);
}
.message-row.user .message-bubble {
  background: linear-gradient(135deg, #3b82f6, #0ea5e9);
  color: #ffffff;
  border-color: rgba(59, 130, 246, 0.35);
}
.message-row.assistant .message-bubble {
  border-top-left-radius: 0;
}
.message-row.user .message-bubble {
  border-top-right-radius: 0;
}
.message-bubble :deep(p) { margin: 0 0 10px 0; }
.message-bubble :deep(p:last-child) { margin: 0; }
.message-bubble :deep(img) { max-width: 100%; border-radius: 8px; margin-top: 10px; }
.message-bubble :deep(pre) { background: #f4f4f5; padding: 10px; border-radius: 6px; overflow-x: auto; }
.message-bubble :deep(code) { font-family: monospace; }

.input-area {
  padding: 16px 28px 20px;
  background: rgba(255, 255, 255, 0.78);
  border-top: 1px solid rgba(191, 219, 254, 0.48);
  display: flex;
  flex-direction: column;
  gap: 12px;
  backdrop-filter: blur(16px);
}
.send-btn {
  align-self: flex-end;
  width: 110px;
  border-radius: 10px;
}
</style>
