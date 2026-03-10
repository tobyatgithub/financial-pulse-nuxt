<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface MarketItem {
  symbol: string
  name: string
  value: number
  change: number
  changePercent: number
}

const markets = ref<MarketItem[]>([])
const isLoading = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('/data/global.json')
    const data = await response.json()
    markets.value = data.markets
  } catch (e) {
    console.error('Failed to load global market data:', e)
  }
  isLoading.value = false
})

function formatValue(value: number): string {
  return value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function getChangeClass(change: number): string {
  if (change > 0) return 'text-emerald-400'
  if (change < 0) return 'text-red-400'
  return 'text-zinc-400'
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      全球市场
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-32">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div v-else class="space-y-2">
      <div v-for="market in markets" :key="market.symbol" class="flex items-center justify-between py-1.5 border-b border-zinc-800/50 last:border-0">
        <span class="text-sm text-zinc-300">{{ market.name }}</span>
        <div class="text-right">
          <div class="font-mono text-sm font-medium">{{ formatValue(market.value) }}</div>
          <div :class="getChangeClass(market.changePercent)" class="text-xs font-mono">
            {{ market.changePercent >= 0 ? '+' : '' }}{{ market.changePercent.toFixed(2) }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
