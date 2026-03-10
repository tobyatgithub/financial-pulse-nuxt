// 通用数据点类型
export interface DataPoint {
  date: string
  value: number
}

// 指数数据
export interface IndexData {
  symbol: string
  name: string
  value: number
  change: number
  changePercent: number
  lastUpdate: string
}

// 汇率数据
export interface ExchangeRate {
  pair: string
  rate: number
  change: number
  lastUpdate: string
}

// VIX数据
export interface VixData {
  value: number
  change: number
  changePercent: number
  history: DataPoint[]
  lastUpdate: string
}

// 新闻数据
export interface NewsItem {
  title: string
  source: string
  url: string
  publishedAt: string
}

// 金融词汇
export interface FinancialTerm {
  term: string
  definition: string
  example: string
  category: string
}

// 期货基差
export interface FuturesBasis {
  contract: string
  futuresPrice: number
  spotPrice: number
  basis: number
  basisPercent: number
  expiry: string
}

// 成交金额
export interface TradingVolume {
  index: string
  volumes: DataPoint[]
  lastUpdate: string
}

// 宏观数据
export interface MacroData {
  indicator: string
  value: number
  unit: string
  period: string
  source: string
  lastUpdate: string
}

// 看板更新状态
export interface UpdateStatus {
  lastUpdate: string
  nextUpdate: string
  status: 'success' | 'error' | 'updating'
}

// API响应包装
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  lastUpdate?: string
}
