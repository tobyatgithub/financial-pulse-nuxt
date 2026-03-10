<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface MacroIndicator {
  name: string
  value: number
  unit: string
  period: string
  source: string
  trend: string
  comment: string
}

interface MacroData {
  lastUpdate: string
  indicators: MacroIndicator[]
  summary: string
}

const macroData = ref<MacroData | null>(null)
const isLoading = ref(true)
const hoveredIndicator = ref<MacroIndicator | null>(null)

onMounted(async () => {
  try {
    const response = await fetch('/data/macro.json')
    macroData.value = await response.json()
  } catch (e) {
    console.error('Failed to load macro data:', e)
  }
  isLoading.value = false
})

function getTrendIcon(trend: string): string {
  if (trend === 'up') return '↑'
  if (trend === 'down') return '↓'
  return '→'
}

function getTrendClass(trend: string): string {
  if (trend === 'up') return 'text-emerald-400'
  if (trend === 'down') return 'text-red-400'
  return 'text-zinc-400'
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <svg class="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
      </svg>
      宏观数据
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-48">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500"></div>
    </div>

    <div v-else-if="macroData" class="space-y-4">
      <!-- 指标列表 -->
      <div class="grid grid-cols-2 gap-3">
        <div
          v-for="indicator in macroData.indicators"
          :key="indicator.name"
          class="p-3 bg-zinc-800/50 rounded-lg hover:bg-zinc-800 transition-colors cursor-pointer relative"
          @mouseenter="hoveredIndicator = indicator"
          @mouseleave="hoveredIndicator = null"
        >
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs text-zinc-400">{{ indicator.name }}</span>
            <span :class="getTrendClass(indicator.trend)" class="text-sm">
              {{ getTrendIcon(indicator.trend) }}
            </span>
          </div>
          <div class="text-xl font-mono font-bold text-zinc-100">
            {{ indicator.value }}{{ indicator.unit }}
          </div>
          <div class="text-xs text-zinc-500 mt-1">{{ indicator.period }}</div>

          <!-- 悬浮提示 -->
          <div
            v-if="hoveredIndicator === indicator"
            class="absolute bottom-full left-0 right-0 mb-2 p-2 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl z-10"
          >
            <div class="text-xs text-zinc-400 mb-1">{{ indicator.comment }}</div>
            <div class="text-xs text-zinc-500">来源: {{ indicator.source }}</div>
          </div>
        </div>
      </div>

      <!-- 概括 -->
      <div class="bg-cyan-500/10 border border-cyan-500/30 rounded-lg p-3">
        <p class="text-sm text-cyan-300">{{ macroData.summary }}</p>
      </div>

      <div class="text-xs text-zinc-500">
        更新时间: {{ macroData.lastUpdate }}
      </div>
    </div>
  </div>
</template>
