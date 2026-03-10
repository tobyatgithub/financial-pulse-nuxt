#!/usr/bin/env python3
"""
Financial Pulse 数据获取脚本
从 AKShare 和其他数据源获取金融数据并生成 JSON 文件
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 数据输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "static" / "data"

def ensure_output_dir():
    """确保输出目录存在"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def save_json(filename: str, data: dict):
    """保存 JSON 数据到文件"""
    filepath = OUTPUT_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {filename}")

def fetch_indices():
    """
    获取 A股/港股指数数据
    数据源: AKShare (东方财富)
    """
    try:
        import akshare as ak
        from datetime import datetime

        indices = []

        # 主要指数代码 (东方财富格式)
        index_codes = {
            '000001': {'name': '上证指数', 'symbol': 'sh000001'},
            '399001': {'name': '深证成指', 'symbol': 'sz399001'},
            '399006': {'name': '创业板指', 'symbol': 'sz399006'},
            '000016': {'name': '上证50', 'symbol': 'sh000016'},
            '000300': {'name': '沪深300', 'symbol': 'sh000300'},
            '000905': {'name': '中证500', 'symbol': 'sh000905'},
            '000852': {'name': '中证1000', 'symbol': 'sh000852'},
            '932000': {'name': '中证2000', 'symbol': 'sh932000'},
        }

        # 尝试使用东方财富实时行情接口
        try:
            df = ak.stock_zh_a_spot_em()
            print(f"A股实时行情数据: {len(df)} 条")

            for _, row in df.iterrows():
                code = str(row['代码'])
                if code in index_codes:
                    info = index_codes[code]
                    indices.append({
                        'symbol': info['symbol'],
                        'name': info['name'],
                        'value': float(row['最新价']),
                        'change': float(row['涨跌额']),
                        'changePercent': float(row['涨跌幅'])
                    })

        except Exception as e:
            print(f"⚠️ 东方财富接口失败: {e}, 尝试备用接口")

            # 备用: 使用新浪接口
            try:
                df = ak.stock_zh_index_spot_sina()
                print(f"新浪指数数据: {len(df)} 条")

                for _, row in df.iterrows():
                    code = str(row['代码'])
                    if code in index_codes:
                        info = index_codes[code]
                        indices.append({
                            'symbol': info['symbol'],
                            'name': info['name'],
                            'value': float(row['最新价']),
                            'change': float(row['涨跌额']),
                            'changePercent': float(row['涨跌幅'])
                        })
            except Exception as e2:
                print(f"⚠️ 新浪接口也失败: {e2}")
                raise e2

        # 获取港股恒生指数
        try:
            df_hk = ak.stock_hk_spot_em()
            for _, row in df_hk.iterrows():
                if str(row['代码']) == '1' or '恒生' in str(row['名称']):
                    indices.append({
                        'symbol': 'hkHSI',
                        'name': '恒生指数',
                        'value': float(row['最新价']),
                        'change': float(row['涨跌额']),
                        'changePercent': float(row['涨跌幅'])
                    })
                    break
        except Exception as e:
            print(f"⚠️ 港股数据获取失败: {e}")

        # 添加南华商品指数 (静态数据，AKShare暂无此接口)
        indices.append({
            'symbol': 'sh000932',
            'name': '南华商品',
            'value': 2567.89,
            'change': -8.90,
            'changePercent': -0.35
        })

        if indices:
            data = {
                'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'indices': indices
            }
            save_json('indices.json', data)
        else:
            raise Exception("No index data fetched")

    except ImportError:
        print("⚠️ AKShare not installed, using mock data")
        create_mock_indices()
    except Exception as e:
        print(f"❌ 获取指数数据失败: {e}")
        create_mock_indices()

def create_mock_indices():
    """创建模拟指数数据"""
    from datetime import datetime

    data = {
        'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'indices': [
            {'symbol': 'sh000001', 'name': '上证指数', 'value': 3356.83, 'change': 12.45, 'changePercent': 0.37},
            {'symbol': 'sz399001', 'name': '深证成指', 'value': 10789.56, 'change': -23.12, 'changePercent': -0.21},
            {'symbol': 'sz399006', 'name': '创业板指', 'value': 2156.78, 'change': 8.34, 'changePercent': 0.39},
            {'symbol': 'hkHSI', 'name': '恒生指数', 'value': 23456.89, 'change': -123.45, 'changePercent': -0.52},
            {'symbol': 'sh000016', 'name': '上证50', 'value': 2678.90, 'change': 5.67, 'changePercent': 0.21},
            {'symbol': 'sh000300', 'name': '沪深300', 'value': 3912.34, 'change': 8.90, 'changePercent': 0.23},
            {'symbol': 'sh000905', 'name': '中证500', 'value': 5678.90, 'change': -12.34, 'changePercent': -0.22},
            {'symbol': 'sh000852', 'name': '中证1000', 'value': 6234.56, 'change': 23.45, 'changePercent': 0.38},
            {'symbol': 'sh932000', 'name': '中证2000', 'value': 2123.45, 'change': 15.67, 'changePercent': 0.74},
            {'symbol': 'sh000932', 'name': '南华商品', 'value': 2567.89, 'change': -8.90, 'changePercent': -0.35}
        ]
    }
    save_json('indices.json', data)

def fetch_global_markets():
    """
    获取全球市场数据
    数据源: yfinance
    """
    try:
        import yfinance as yf
        from datetime import datetime

        symbols = {
            '^N225': '日经225',
            '^KS11': '韩国综合',
            '^DJI': '道琼斯',
            '^IXIC': '纳斯达克',
            '^FTSE': '富时100',
            '^GDAXI': '德国DAX'
        }

        markets = []
        for symbol, name in symbols.items():
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
                previous_close = info.get('previousClose')

                if current_price and previous_close:
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100

                    markets.append({
                        'symbol': symbol,
                        'name': name,
                        'value': round(current_price, 2),
                        'change': round(change, 2),
                        'changePercent': round(change_percent, 2)
                    })
            except Exception as e:
                print(f"⚠️ {name} 数据获取失败: {e}")

        if markets:
            data = {
                'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'markets': markets
            }
            save_json('global.json', data)
        else:
            raise Exception("No data fetched")

    except ImportError:
        print("⚠️ yfinance not installed, using mock data")
        create_mock_global()
    except Exception as e:
        print(f"❌ 获取全球市场数据失败: {e}")
        create_mock_global()

def create_mock_global():
    """创建模拟全球市场数据"""
    from datetime import datetime

    data = {
        'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'markets': [
            {'symbol': '^N225', 'name': '日经225', 'value': 38456.78, 'change': 234.56, 'changePercent': 0.61},
            {'symbol': '^KS11', 'name': '韩国综合', 'value': 2678.90, 'change': -12.34, 'changePercent': -0.46},
            {'symbol': '^DJI', 'name': '道琼斯', 'value': 42345.67, 'change': 156.78, 'changePercent': 0.37},
            {'symbol': '^IXIC', 'name': '纳斯达克', 'value': 17890.12, 'change': -45.67, 'changePercent': -0.26},
            {'symbol': '^FTSE', 'name': '富时100', 'value': 8123.45, 'change': 23.45, 'changePercent': 0.29},
            {'symbol': '^GDAXI', 'name': '德国DAX', 'value': 18234.56, 'change': -67.89, 'changePercent': -0.37}
        ]
    }
    save_json('global.json', data)

def fetch_vix():
    """
    获取 VIX 恐慌指数数据
    数据源: yfinance
    """
    try:
        import yfinance as yf
        from datetime import datetime, timedelta

        ticker = yf.Ticker("^VIX")
        info = ticker.info

        current_value = info.get('currentPrice') or info.get('regularMarketPrice')
        previous_close = info.get('previousClose')

        # 获取历史数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        hist = ticker.history(start=start_date, end=end_date)

        history = []
        for date, row in hist.iterrows():
            history.append({
                'date': date.strftime('%Y-%m-%d'),
                'value': round(row['Close'], 2)
            })

        # 判断 VIX 水平
        if current_value < 15:
            level = "平静"
        elif current_value < 20:
            level = "正常"
        elif current_value < 30:
            level = "担忧"
        else:
            level = "恐慌"

        change = current_value - previous_close
        change_percent = (change / previous_close) * 100

        data = {
            'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'value': round(current_value, 2),
            'change': round(change, 2),
            'changePercent': round(change_percent, 2),
            'level': level,
            'history': history
        }
        save_json('vix.json', data)

    except Exception as e:
        print(f"❌ 获取 VIX 数据失败: {e}")
        create_mock_vix()

def create_mock_vix():
    """创建模拟 VIX 数据"""
    from datetime import datetime, timedelta

    # 生成近3个月的历史数据
    history = []
    base_value = 16.0
    for i in range(14):
        date = datetime.now() - timedelta(days=(14-i)*7)
        value = base_value + (i % 3) * 1.5 - (i % 5) * 0.8
        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'value': round(16.45 + (i - 7) * 0.5, 2)
        })

    data = {
        'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'value': 16.45,
        'change': -0.78,
        'changePercent': -4.52,
        'level': '正常',
        'history': history
    }
    save_json('vix.json', data)

def fetch_exchange_rates():
    """
    获取人民币汇率中间价
    数据源: AKShare (中国外汇交易中心)
    """
    try:
        import akshare as ak
        from datetime import datetime

        # 尝试获取汇率数据
        try:
            df = ak.fx_spot_quote()
            print(f"汇率数据: {len(df)} 条")
            print(f"汇率数据列: {df.columns.tolist()}")
            print(f"汇率数据前2行:\n{df.head(2)}")

            rates = []
            pairs = {
                'USD/CNY': '美元/人民币',
                'GBP/CNY': '英镑/人民币',
                '100JPY/CNY': '100日元/人民币',
                'EUR/CNY': '欧元/人民币'
            }

            # 动态获取列名
            cols = df.columns.tolist()
            symbol_col = cols[0] if cols else None
            # 查找价格列 - 尝试多种可能的列名
            price_col = None
            for col in cols:
                if '价' in col or 'rate' in col.lower() or '汇率' in col:
                    price_col = col
                    break
            if not price_col and len(cols) > 1:
                price_col = cols[1]

            print(f"使用列: symbol={symbol_col}, price={price_col}")

            for _, row in df.iterrows():
                symbol = str(row.get(symbol_col, ''))
                # 尝试多种货币对格式匹配
                matched_pair = None
                for pair in pairs:
                    if pair == symbol or symbol in pair or pair.replace('/', '') in symbol.replace('/', ''):
                        matched_pair = pair
                        break

                if matched_pair and price_col:
                    try:
                        rate_value = row.get(price_col)
                        if rate_value:
                            rates.append({
                                'pair': matched_pair,
                                'name': pairs[matched_pair],
                                'rate': float(rate_value),
                                'change': 0.0,
                                'changePercent': 0.0
                            })
                    except (ValueError, TypeError) as e:
                        print(f"⚠️ 解析汇率值失败: {e}")
                        continue

            if rates:
                data = {
                    'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'rates': rates
                }
                save_json('exchange.json', data)
            else:
                print("⚠️ 未找到匹配的汇率数据，使用模拟数据")
                create_mock_exchange()

        except Exception as e:
            print(f"⚠️ 汇率数据获取失败: {e}")
            create_mock_exchange()

    except ImportError:
        print("⚠️ AKShare not installed, using mock data")
        create_mock_exchange()

def create_mock_exchange():
    """创建模拟汇率数据"""
    from datetime import datetime

    data = {
        'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'rates': [
            {'pair': 'USD/CNY', 'name': '美元/人民币', 'rate': 7.2345, 'change': 0.0089, 'changePercent': 0.12},
            {'pair': 'GBP/CNY', 'name': '英镑/人民币', 'rate': 9.2890, 'change': -0.0234, 'changePercent': -0.25},
            {'pair': '100JPY/CNY', 'name': '100日元/人民币', 'rate': 4.8567, 'change': 0.0123, 'changePercent': 0.25},
            {'pair': 'EUR/CNY', 'name': '欧元/人民币', 'rate': 7.8912, 'change': -0.0156, 'changePercent': -0.20}
        ]
    }
    save_json('exchange.json', data)

def main():
    """主函数"""
    print("🚀 Financial Pulse 数据获取脚本")
    print("=" * 50)

    ensure_output_dir()

    print("\n📊 获取 A股/港股指数...")
    fetch_indices()

    print("\n🌍 获取全球市场数据...")
    fetch_global_markets()

    print("\n📈 获取 VIX 恐慌指数...")
    fetch_vix()

    print("\n💱 获取汇率数据...")
    fetch_exchange_rates()

    print("\n" + "=" * 50)
    print("✅ 数据获取完成!")

if __name__ == "__main__":
    main()
