<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

interface FinancialTerm {
  term: string
  definition: string
  example: string
  category: string
}

interface TermsData {
  terms: FinancialTerm[]
}

const termsData = ref<TermsData | null>(null)
const isLoading = ref(true)

// 根据日期选择词汇（同一天显示相同的词汇）
const todayTerms = computed<FinancialTerm[]>(() => {
  if (!termsData.value) return []

  const today = new Date()
  const dayOfYear = Math.floor((today.getTime() - new Date(today.getFullYear(), 0, 0).getTime() / 86400000))

  // 使用日期哈希选择词汇
  const terms = termsData.value.terms
  const index1 = dayOfYear % terms.length
  const index2 = (dayOfYear + terms.length / 2) % terms.length

  return [terms[index1], terms[index2]]
})

onMounted(async () => {
  try {
    const response = await fetch('/data/terms.json')
    termsData.value = await response.json()
  } catch (e) {
    console.error('Failed to load terms data:', e)
  }
  isLoading.value = false
})

const categoryColors: Record<string, string> = {
  '风险管理': 'bg-purple-500/20 text-purple-400',
  '衍生品': 'bg-orange-500/20 text-orange-400',
  '市场指标': 'bg-blue-500/20 text-blue-400',
  '宏观经济': 'bg-green-500/20 text-green-400',
  '量化投资': 'bg-pink-500/20 text-pink-400',
  '交易策略': 'bg-yellow-500/20 text-yellow-400',
  '交易机制': 'bg-cyan-500/20 text-cyan-400'
}

function getCategoryColor(category: string): string {
  return categoryColors[category] || 'bg-zinc-500/20 text-zinc-400'
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <svg class="w-4 h-4 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
      </svg>
      每日金融词汇
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-48">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-500"></div>
    </div>

    <div v-else-if="todayTerms.length > 0" class="space-y-4">
      <div
        v-for="(term, index) in todayTerms"
        :key="index"
        class="p-4 bg-zinc-800/30 rounded-lg border border-zinc-800"
      >
        <div class="flex items-center gap-2 mb-2">
          <h3 class="text-lg font-bold text-white">{{ term.term }}</h3>
          <span :class="getCategoryColor(term.category)" class="text-xs px-2 py-0.5 rounded">
            {{ term.category }}
          </span>
        </div>

        <p class="text-sm text-zinc-300 mb-3">{{ term.definition }}</p>

        <div class="bg-zinc-900/50 rounded p-2">
          <p class="text-xs text-zinc-400">
            <span class="text-zinc-500">示例：</span>
            {{ term.example }}
          </p>
        </div>
      </div>

      <div class="text-xs text-zinc-500 text-center">
        每日更新 · 共 {{ termsData?.terms.length || 0 }} 个词汇
      </div>
    </div>
  </div>
</template>
