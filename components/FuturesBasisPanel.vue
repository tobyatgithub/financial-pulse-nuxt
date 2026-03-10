<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'

interface FuturesContract {
  code: string
  name: string
  futuresPrice: number
  spotPrice: number
  multiplier: number
  basis: number
  basisPercent: number
  expiry: string
  daysToExpiry: number
  annualizedBasis: number
}

interface FuturesData {
  lastUpdate: string
  description: string
  contracts: FuturesContract[]
  strategyNote: string
}

const futuresData = ref<FuturesData | null>(null)
const isLoading = ref(true)
const showNearMonth = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('/data/futures.json')
    futuresData.value = await response.json()
  } catch (e) {
    console.error('Failed to load futures data:', e)
  }
  isLoading.value = false
})

function getBasisClass(basis: number): string {
  if (basis > 0) return 'text-emerald-400' // 升水
  return 'text-red-400' // 贴水
}

function formatBasis(value: number): string {
  return (value >= 0 ? '+' : '') + value.toFixed(2)
}

// 使用 computed 计算近月和远月合约
const nearMonthContracts = computed(() => {
  if (!futuresData.value) return []
  const sorted = [...futuresData.value.contracts].sort((a, b) => a.daysToExpiry - b.daysToExpiry)
  return sorted.slice(0, 4)
})

const farMonthContracts = computed(() => {
  if (!futuresData.value) return []
  const sorted = [...futuresData.value.contracts].sort((a, b) => a.daysToExpiry - b.daysToExpiry)
  return sorted.slice(4)
})
</script>

<template>
  <div class="card">
    <div class="card-header">
      <svg class="w-4 h-4 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
      </svg>
      期货基差 (IH/IF/IC/IM)
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-48">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
    </div>

    <div v-else-if="futuresData" class="space-y-4">
      <!-- 合约切换 -->
      <div class="flex gap-2">
        <button
          @click="showNearMonth = true"
          :class="showNearMonth ? 'bg-zinc-700 text-white' : 'bg-zinc-800 text-zinc-400'"
          class="px-3 py-1 text-xs rounded-lg transition-colors"
        >
          近月合约
        </button>
        <button
          @click="showNearMonth = false"
          :class="!showNearMonth ? 'bg-zinc-700 text-white' : 'bg-zinc-800 text-zinc-400'"
          class="px-3 py-1 text-xs rounded-lg transition-colors"
        >
          远月合约
        </button>
      </div>

      <!-- 基差表格 -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-zinc-500 text-xs border-b border-zinc-800">
              <th class="text-left py-2">合约</th>
              <th class="text-right py-2">期货</th>
              <th class="text-right py-2">现货</th>
              <th class="text-right py-2">基差%</th>
              <th class="text-right py-2">年化%</th>
              <th class="text-right py-2">到期</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="contract in (showNearMonth ? nearMonthContracts : farMonthContracts)"
              :key="contract.code"
              class="border-b border-zinc-800/50"
            >
              <td class="py-2 font-medium">{{ contract.code }}</td>
              <td class="text-right font-mono">{{ contract.futuresPrice.toFixed(1) }}</td>
              <td class="text-right font-mono text-zinc-400">{{ contract.spotPrice.toFixed(1) }}</td>
              <td :class="['text-right font-mono', getBasisClass(contract.basis)]">
                {{ formatBasis(contract.basisPercent) }}%
              </td>
              <td :class="['text-right font-mono', getBasisClass(contract.annualizedBasis)]">
                {{ formatBasis(contract.annualizedBasis) }}%
              </td>
              <td class="text-right text-zinc-500">{{ contract.daysToExpiry }}天</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 策略简评 -->
      <div class="bg-zinc-800/50 rounded-lg p-3">
        <p class="text-xs text-zinc-400">{{ futuresData.strategyNote }}</p>
      </div>

      <div class="text-xs text-zinc-500">
        更新时间: {{ futuresData.lastUpdate }}
      </div>
    </div>
  </div>
</template>
