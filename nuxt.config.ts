// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  modules: ['@nuxtjs/tailwindcss'],

  css: ['~/assets/css/main.css'],

  app: {
    head: {
      title: 'Financial Pulse - 金融看板',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: '实时金融数据看板 - A股、港股、全球市场、汇率、VIX等' }
      ]
    }
  },

  // Serve static files from /static directory
  nitro: {
    prerender: {
      routes: ['/']
    },
    publicAssets: [
      {
        dir: '../static',
        maxAge: 60 * 5 // 5 minutes cache
      }
    ]
  },

  // Enable static generation for Cloudflare Pages
  ssr: true
})
