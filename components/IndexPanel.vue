<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

interface IndexItem {
  symbol: string
  name: string
  value: number
  change: number
  changePercent: number
}

const indices = ref<IndexItem[]>([])
const lastUpdate = ref('')
const isLoading = ref(true)

const mainIndices = computed(() => indices.value.slice(0, 4))
const otherIndices = computed(() => indices.value.slice(4))

onMounted(async () => {
  try {
    const response = await fetch('/data/indices.json')
    const data = await response.json()
    indices.value = data.indices
    lastUpdate.value = data.lastUpdate
  } catch (e) {
    console.error('Failed to load indices data:', e)
  }
  isLoading.value = false
})

function formatValue(value: number): string {
  return value.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function getChangeClass(change: number): string {
  if (change > 0) return 'text-emerald-400'
  if (change < 0) return 'text-red-400'
  return 'text-zinc-400'
}

function getChangeSymbol(change: number): string {
  if (change > 0) return '+'
  return ''
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
      </svg>
      A股/港股指数
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-32">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
    </div>

    <div v-else class="space-y-3">
      <!-- 主要指数 -->
      <div class="space-y-2">
        <div v-for="index in mainIndices" :key="index.symbol" class="flex items-center justify-between py-1">
          <span class="text-sm text-zinc-300">{{ index.name }}</span>
          <div class="text-right">
            <div class="font-mono text-sm font-medium">{{ formatValue(index.value) }}</div>
            <div :class="getChangeClass(index.change)" class="text-xs font-mono">
              {{ getChangeSymbol(index.change) }}{{ formatValue(index.change) }} ({{ getChangeSymbol(index.changePercent) }}{{ index.changePercent.toFixed(2) }}%)
            </div>
          </div>
        </div>
      </div>

      <!-- 其他指数 - 折叠显示 -->
      <div class="border-t border-zinc-800 pt-2 mt-2">
        <div class="grid grid-cols-2 gap-2 text-xs">
          <div v-for="index in otherIndices" :key="index.symbol" class="flex items-center justify-between">
            <span class="text-zinc-400">{{ index.name }}</span>
            <span :class="getChangeClass(index.changePercent)" class="font-mono">
              {{ getChangeSymbol(index.changePercent) }}{{ index.changePercent.toFixed(2) }}%
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
