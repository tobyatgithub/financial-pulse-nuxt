<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface RateItem {
  pair: string
  name: string
  rate: number
  change: number
  changePercent: number
}

const rates = ref<RateItem[]>([])
const lastUpdate = ref('')
const isLoading = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('/data/exchange.json')
    const data = await response.json()
    rates.value = data.rates
    lastUpdate.value = data.lastUpdate
  } catch (e) {
    console.error('Failed to load exchange rate data:', e)
  }
  isLoading.value = false
})

function formatRate(rate: number): string {
  return rate.toFixed(4)
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
      <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      人民币汇率中间价
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-32">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500"></div>
    </div>

    <div v-else class="space-y-3">
      <div v-for="rate in rates" :key="rate.pair" class="flex items-center justify-between py-2 border-b border-zinc-800/50 last:border-0">
        <div>
          <div class="text-sm font-medium text-zinc-200">{{ rate.name }}</div>
          <div class="text-xs text-zinc-500">{{ rate.pair }}</div>
        </div>
        <div class="text-right">
          <div class="font-mono text-lg font-bold text-zinc-100">{{ formatRate(rate.rate) }}</div>
          <div :class="getChangeClass(rate.change)" class="text-xs font-mono">
            {{ rate.change >= 0 ? '+' : '' }}{{ rate.change.toFixed(4) }} ({{ rate.changePercent >= 0 ? '+' : '' }}{{ rate.changePercent.toFixed(2) }}%)
          </div>
        </div>
      </div>

      <div class="text-xs text-zinc-500 pt-2">
        更新时间: {{ lastUpdate }}
      </div>
    </div>
  </div>
</template>
