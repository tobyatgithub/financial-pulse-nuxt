<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

interface DataPoint {
  date: string
  value: number
}

interface VolumeData {
  index: string
  data: DataPoint[]
}

interface VolumeResponse {
  lastUpdate: string
  volumes: VolumeData[]
}

const volumeData = ref<VolumeResponse | null>(null)
const isLoading = ref(true)
const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null
const selectedIndex = ref('沪深300')

onMounted(async () => {
  try {
    const response = await fetch('/data/volume.json')
    volumeData.value = await response.json()
  } catch (e) {
    console.error('Failed to load volume data:', e)
  }
  isLoading.value = false
})

watch([isLoading, chartRef, selectedIndex], () => {
  if (!isLoading.value && chartRef.value && volumeData.value) {
    initChart()
  }
})

function initChart() {
  if (!chartRef.value || !volumeData.value) return

  if (chart) {
    chart.dispose()
  }

  chart = echarts.init(chartRef.value, 'dark')

  const currentData = volumeData.value.volumes.find(v => v.index === selectedIndex.value)
  if (!currentData) return

  const option = {
    backgroundColor: 'transparent',
    grid: {
      top: 20,
      right: 20,
      bottom: 30,
      left: 50
    },
    xAxis: {
      type: 'category',
      data: currentData.data.map(d => d.date.slice(5)), // 只显示月-日
      axisLine: { lineStyle: { color: '#3f3f46' } },
      axisLabel: { color: '#71717a', fontSize: 10, rotate: 45 },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: {
        color: '#71717a',
        fontSize: 10,
        formatter: (value: number) => (value / 1000).toFixed(0) + 'k'
      },
      splitLine: { lineStyle: { color: '#27272a' } }
    },
    series: [{
      data: currentData.data.map(d => d.value),
      type: 'bar',
      barWidth: '60%',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#8b5cf6' },
          { offset: 1, color: '#6366f1' }
        ]),
        borderRadius: [4, 4, 0, 0]
      }
    }],
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#18181b',
      borderColor: '#3f3f46',
      textStyle: { color: '#f4f4f5' },
      formatter: (params: any) => {
        const idx = params[0].dataIndex
        const data = currentData.data[idx]
        return `${data.date}<br/>成交额: <strong>${data.value.toLocaleString()}亿</strong>`
      }
    }
  }

  chart.setOption(option)

  // Resize handler
  window.addEventListener('resize', () => chart?.resize())
}

const indexOptions = ['沪深300', '中证500', '中证1000', '中证2000', '微盘股']
</script>

<template>
  <div class="card">
    <div class="card-header">
      <svg class="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
      </svg>
      成交金额 (亿元)
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
    </div>

    <div v-else-if="volumeData" class="space-y-4">
      <!-- 指数选择 -->
      <div class="flex flex-wrap gap-2">
        <button
          v-for="index in indexOptions"
          :key="index"
          @click="selectedIndex = index"
          :class="selectedIndex === index ? 'bg-indigo-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'"
          class="px-3 py-1 text-xs rounded-lg transition-colors"
        >
          {{ index }}
        </button>
      </div>

      <!-- 图表 -->
      <div ref="chartRef" class="h-48 w-full"></div>

      <div class="text-xs text-zinc-500">
        更新时间: {{ volumeData.lastUpdate }}
      </div>
    </div>
  </div>
</template>
