<script setup lang="ts">
import { ref, onMounted } from 'vue'

const lastUpdate = ref<string>('')
const isLoading = ref(true)

onMounted(async () => {
  // Load last update time
  try {
    const response = await fetch('/data/indices.json')
    const data = await response.json()
    lastUpdate.value = data.lastUpdate
  } catch (e) {
    lastUpdate.value = '加载中...'
  }
  isLoading.value = false
})
</script>

<template>
  <div class="min-h-screen bg-zinc-950 text-zinc-100">
    <!-- Header -->
    <header class="border-b border-zinc-800 bg-zinc-900/50 backdrop-blur-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
          </div>
          <h1 class="text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            Financial Pulse
          </h1>
        </div>
        <div class="flex items-center gap-4 text-sm text-zinc-400">
          <span class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            {{ lastUpdate }}
          </span>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- Panel 1: A股/港股指数 -->
        <IndexPanel />

        <!-- Panel 2: 全球市场 -->
        <GlobalMarketPanel />

        <!-- Panel 3: 汇率中间价 -->
        <ExchangeRatePanel />

        <!-- Panel 4: 金融新闻 -->
        <NewsPanel class="md:col-span-2 lg:col-span-1" />

        <!-- Panel 5: VIX恐慌指数 -->
        <VixPanel />

        <!-- Panel 6: 期货基差 -->
        <FuturesBasisPanel class="md:col-span-2" />

        <!-- Panel 7: 成交金额 -->
        <VolumePanel class="lg:col-span-2" />

        <!-- Panel 8: 宏观数据 -->
        <MacroDataPanel />

        <!-- Panel 9: 每日金融词汇 -->
        <DailyTermPanel />
      </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-zinc-800 mt-8 py-4">
      <div class="max-w-7xl mx-auto px-4 text-center text-sm text-zinc-500">
        <p>数据仅供参考，不构成投资建议 | 数据来源：AKShare, yfinance</p>
      </div>
    </footer>
  </div>
</template>
