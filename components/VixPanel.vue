<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import * as echarts from 'echarts'

interface DataPoint {
  date: string
  value: number
}

interface VixData {
  value: number
  change: number
  changePercent: number
  level: string
  history: DataPoint[]
  lastUpdate: string
}

const vixData = ref<VixData | null>(null)
const isLoading = ref(true)
const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

const levelClass = computed(() => {
  if (!vixData.value) return 'text-zinc-400'
  const v = vixData.value.value
  if (v < 15) return 'text-emerald-400'
  if (v < 20) return 'text-yellow-400'
  if (v < 30) return 'text-orange-400'
  return 'text-red-400'
})

const levelBg = computed(() => {
  if (!vixData.value) return 'bg-zinc-800'
  const v = vixData.value.value
  if (v < 15) return 'bg-emerald-500/20'
  if (v < 20) return 'bg-yellow-500/20'
  if (v < 30) return 'bg-orange-500/20'
  return 'bg-red-500/20'
})

onMounted(async () => {
  try {
    const response = await fetch('/data/vix.json')
    vixData.value = await response.json()
  } catch (e) {
    console.error('Failed to load VIX data:', e)
  }
  isLoading.value = false
})

watch([isLoading, chartRef], () => {
  if (!isLoading.value && chartRef.value && vixData.value) {
    initChart()
  }
})

function initChart() {
  if (!chartRef.value || !vixData.value) return

  chart = echarts.init(chartRef.value, 'dark')

  const option = {
    backgroundColor: 'transparent',
    grid: {
      top: 10,
      right: 10,
      bottom: 20,
      left: 35
    },
    xAxis: {
      type: 'category',
      data: vixData.value.history.map(d => d.date.slice(5)), // 只显示月-日
      axisLine: { lineStyle: { color: '#3f3f46' } },
      axisLabel: { color: '#71717a', fontSize: 10 },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: '#71717a', fontSize: 10 },
      splitLine: { lineStyle: { color: '#27272a' } }
    },
    series: [{
      data: vixData.value.history.map(d => d.value),
      type: 'line',
      smooth: true,
      symbol: 'none',
      lineStyle: { color: '#8b5cf6', width: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(139, 92, 246, 0.3)' },
          { offset: 1, color: 'rgba(139, 92, 246, 0)' }
        ])
      }
    }],
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#18181b',
      borderColor: '#3f3f46',
      textStyle: { color: '#f4f4f5' },
      formatter: (params: any) => {
        const idx = params[0].dataIndex
        const data = vixData.value!.history[idx]
        return `${data.date}<br/>VIX: <strong>${data.value.toFixed(2)}</strong>`
      }
    }
  }

  chart.setOption(option)

  // Resize handler
  window.addEventListener('resize', () => chart?.resize())
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
      </svg>
      VIX恐慌指数
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-48">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
    </div>

    <div v-else-if="vixData" class="space-y-4">
      <!-- 当前值 -->
      <div class="flex items-center justify-between">
        <div>
          <div class="text-3xl font-mono font-bold" :class="levelClass">
            {{ vixData.value.toFixed(2) }}
          </div>
          <div :class="['text-sm', vixData.change >= 0 ? 'text-red-400' : 'text-emerald-400']">
            {{ vixData.change >= 0 ? '+' : '' }}{{ vixData.change.toFixed(2) }} ({{ vixData.changePercent >= 0 ? '+' : '' }}{{ vixData.changePercent.toFixed(2) }}%)
          </div>
        </div>
        <div :class="[levelBg, 'px-3 py-1.5 rounded-lg']">
          <span :class="levelClass" class="text-sm font-medium">{{ vixData.level }}</span>
        </div>
      </div>

      <!-- 图表 -->
      <div ref="chartRef" class="h-32 w-full"></div>

      <!-- VIX等级说明 -->
      <div class="flex items-center justify-between text-xs text-zinc-500">
        <span>平静 &lt;15</span>
        <span>正常 15-20</span>
        <span>担忧 20-30</span>
        <span>恐慌 &gt;30</span>
      </div>
    </div>
  </div>
</template>
