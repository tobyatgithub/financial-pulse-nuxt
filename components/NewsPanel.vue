<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface NewsItem {
  title: string
  source: string
  url: string
  publishedAt: string
}

const news = ref<NewsItem[]>([])
const isLoading = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('/data/news.json')
    const data = await response.json()
    news.value = data.news
  } catch (e) {
    console.error('Failed to load news data:', e)
  }
  isLoading.value = false
})

function formatTime(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)

  if (diffMins < 60) return `${diffMins}分钟前`
  if (diffMins < 1440) return `${Math.floor(diffMins / 60)}小时前`
  return date.toLocaleDateString('zh-CN')
}

function getSourceColor(source: string): string {
  const colors: Record<string, string> = {
    '财新网': 'bg-blue-500/20 text-blue-400',
    '新浪财经': 'bg-orange-500/20 text-orange-400',
    '华尔街见闻': 'bg-purple-500/20 text-purple-400'
  }
  return colors[source] || 'bg-zinc-500/20 text-zinc-400'
}
</script>

<template>
  <div class="card h-full">
    <div class="card-header">
      <svg class="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
      </svg>
      金融新闻
    </div>

    <div v-if="isLoading" class="flex items-center justify-center h-32">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-500"></div>
    </div>

    <div v-else class="space-y-3 max-h-80 overflow-y-auto">
      <a
        v-for="(item, index) in news"
        :key="index"
        :href="item.url"
        target="_blank"
        rel="noopener noreferrer"
        class="block group"
      >
        <div class="p-2 rounded-lg hover:bg-zinc-800/50 transition-colors">
          <div class="flex items-start gap-2">
            <span :class="getSourceColor(item.source)" class="text-xs px-1.5 py-0.5 rounded shrink-0">
              {{ item.source }}
            </span>
            <span class="text-xs text-zinc-500 shrink-0">{{ formatTime(item.publishedAt) }}</span>
          </div>
          <p class="text-sm text-zinc-300 mt-1 group-hover:text-white transition-colors line-clamp-2">
            {{ item.title }}
          </p>
        </div>
      </a>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
