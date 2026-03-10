# Financial Pulse - 金融看板

实时金融数据看板，包含A股、港股、全球市场、汇率、VIX等9个数据板块。

## 功能特性

### 9个数据板块

1. **A股/港股指数** - 上证、深证、创业板、恒生、沪深300、中证500/1000/2000、南华商品
2. **全球市场** - 日经225、韩国综合、道琼斯、纳斯达克、富时100、德国DAX
3. **人民币汇率中间价** - 美元/人民币、英镑/人民币、100日元/人民币、欧元/人民币
4. **金融新闻** - 聚合财新网、新浪财经、华尔街见闻 RSS 源
5. **VIX恐慌指数** - 实时数值 + 近3个月历史图表
6. **期货基差** - IH/IF/IC/IM 近远月合约基差对比
7. **成交金额** - 各指数近3周成交额图表
8. **宏观数据** - GDP、PMI、CPI、PPI、M1、M2 等宏观指标
9. **每日金融词汇** - 每日2个金融术语学习

## 技术栈

- **框架**: Nuxt 3.21.1 + Vue 3 + TypeScript
- **样式**: Tailwind CSS
- **图表**: ECharts (vue-echarts)
- **数据源**: AKShare (Python) + yfinance
- **部署**: Cloudflare Pages

## 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 静态生成
npm run generate
```

## 部署到 Cloudflare Pages

### 构建配置

| 设置项 | 值 |
|--------|-----|
| Build command | `npm run generate` |
| Build output directory | `dist` |
| Node version | 20.19.0 (通过 `.node-version` 文件指定) |

### 部署步骤

1. Fork 本仓库
2. 在 Cloudflare Dashboard → **Pages** → **Create a project**
3. 连接 GitHub 仓库 `financial-pulse-nuxt`
4. 填写上述构建配置

---

## 数据更新方案

### 方案对比

| 方案 | 成本 | 实时性 | 复杂度 | 推荐场景 |
|------|------|--------|--------|----------|
| **A. GitHub Actions 定时更新** | 免费 | 1小时延迟 | ⭐ 低 | ✅ 推荐 |
| **B. 本地脚本 + Cron** | 免费 | 可控 | ⭐⭐ 中 | 有自有服务器 |
| **C. Cloudflare Workers + KV** | 免费额度 | 近实时 | ⭐⭐⭐ 高 | 需要实时数据 |

---

### 方案 A: GitHub Actions 定时更新 (推荐)

**原理**: GitHub Actions 每小时运行 Python 脚本，获取数据后提交到仓库，触发 Cloudflare Pages 重新部署。

**配置步骤**:

1. **获取 Cloudflare Deploy Hook URL**:
   - 进入 Cloudflare Dashboard → 你的 Pages 项目
   - **Settings** → **Builds & deployments**
   - 滚动到底部找到 **Deploy hooks**
   - 点击 **Create deploy hook**，命名为 "GitHub Actions"
   - 复制生成的 URL (格式类似 `https://api.cloudflare.com/client/v4/pages/webhooks/xxx`)

2. **配置 GitHub Secret**:
   - 进入 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions**
   - 点击 **New repository secret**
   - Name: `CF_DEPLOY_HOOK_URL`
   - Value: 粘贴上一步复制的 Deploy Hook URL
   - 点击 **Add secret**

3. **启用 Workflow**:
   - 仓库中的 `.github/workflows/update-data.yml` 已配置好
   - 默认每小时整点运行
   - 也可以在 Actions 页面手动触发

**优点**: 完全免费、配置简单、无需服务器
**缺点**: 数据延迟最多1小时

---

### 方案 B: 本地脚本 + Cron

**原理**: 在本地或服务器上使用 cron 定时任务运行 Python 脚本，手动或自动同步数据。

**配置步骤**:

```bash
# 1. 编辑 crontab
crontab -e

# 2. 添加定时任务 (每小时运行)
0 * * * * cd /path/to/financial-pulse-nuxt && python scripts/fetch_data.py && git add static/data/*.json && git commit -m "data: update" && git push

# 3. 在 Cloudflare 设置 Deploy Hook (同方案A)
```

**优点**: 完全控制更新频率
**缺点**: 需要本地机器/服务器持续运行

---

### 方案 C: Cloudflare Workers + KV (高级)

**原理**: 使用 Cloudflare Workers 运行时动态获取数据，存储到 KV 缓存。

**配置步骤**:

1. 创建 KV namespace:
   ```
   wrangler kv:namespace create "FINANCIAL_DATA"
   ```

2. 创建 Worker API (需要改造成 SSR 模式)

3. 前端改为从 Worker API 获取数据

**优点**: 近实时数据、无需 GitHub 中转
**缺点**: 配置复杂、有免费额度限制

---

## 目录结构

```
financial-pulse-nuxt/
├── app.vue                 # 主应用组件
├── components/             # Vue 组件
│   ├── IndexPanel.vue      # A股/港股指数
│   ├── GlobalMarketPanel.vue # 全球市场
│   ├── ExchangeRatePanel.vue # 汇率
│   ├── NewsPanel.vue       # 金融新闻
│   ├── VixPanel.vue        # VIX恐慌指数
│   ├── FuturesBasisPanel.vue # 期货基差
│   ├── VolumePanel.vue     # 成交金额
│   ├── MacroDataPanel.vue  # 宏观数据
│   └── DailyTermPanel.vue  # 每日词汇
├── static/data/            # JSON 数据文件
├── scripts/                # Python 数据获取脚本
│   ├── fetch_data.py       # 主脚本
│   └── requirements.txt    # Python 依赖
├── server/api/             # Nuxt API 路由
├── types/                  # TypeScript 类型定义
└── .github/workflows/      # GitHub Actions
```

## 数据源说明

| 板块 | 数据源 | 更新频率 |
|------|--------|----------|
| A股/港股指数 | AKShare | 交易时间5分钟 |
| 全球市场 | yfinance | 1小时 |
| 汇率中间价 | AKShare | 每日09:30后 |
| 金融新闻 | RSS聚合 | 1小时 |
| VIX恐慌指数 | yfinance | 15分钟 |
| 期货基差 | AKShare | 交易时间5分钟 |
| 成交金额 | AKShare | 每日收盘后 |
| 宏观数据 | AKShare | 数据发布后 |
| 每日词汇 | 本地词库 | 每日 |

## 注意事项

- 数据仅供参考，不构成投资建议
- AKShare 接口可能不稳定，脚本包含降级到模拟数据的逻辑
- yfinance 需要稳定的网络连接访问 Yahoo Finance

## License

MIT
