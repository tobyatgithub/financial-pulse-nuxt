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

- **框架**: Nuxt 3.20.2 + Vue 3 + TypeScript
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

# 生产构建
npm run build

# 静态生成
npm run generate
```

## 数据更新

### 手动更新数据

```bash
# 安装 Python 依赖
pip install -r scripts/requirements.txt

# 运行数据获取脚本
python scripts/fetch_data.py
```

### 自动更新

项目使用 GitHub Actions 每小时自动更新数据：
- `.github/workflows/update-data.yml` - 定时任务配置
- 自动提交数据更新并触发 Cloudflare Pages 重新部署

## 部署到 Cloudflare Pages

1. Fork 本仓库
2. 在 Cloudflare Pages 中连接 GitHub 仓库
3. 设置构建配置:
   - 构建命令: `npm run generate`
   - 输出目录: `.output/public`
4. 设置环境变量（可选）:
   - `CF_DEPLOY_HOOK_URL` - Cloudflare Pages Deploy Hook URL

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
