# coding=utf-8
import akshare as ak
import pandas as pd
from CodersWheel.QuickTool.file_cache import file_cache

import re


def reshape_code(s, pattern=r"^(\d{6})\.([A-Za-z]{2})$"):
    # 测试正则表达式

    match = re.match(pattern, s)
    if match:
        digits = match.group(1)  # 提取数字部分
        letters = match.group(2).lower()  # 提取字母部分
        return letters + digits
    else:
        return s


@file_cache(enable_cache=True, granularity='d')
def get_idx_quote(code):
    stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=code).set_index('date')
    stock_zh_index_daily_df.index = pd.to_datetime(stock_zh_index_daily_df.index)
    return stock_zh_index_daily_df

def get_idx_quote_v2(code:str):
    code2 = reshape_code(code)
    return get_idx_quote(code2)
#




if __name__ == '__main__':
    # 定义正则表达式

    # 测试字符串
    test_strings = [
        "123456.AB",  # 匹配成功
        "123456.aB",  # 匹配成功
        "12345.A",  # 匹配失败（数字不足6位）
        "1234567.AB",  # 匹配失败（数字超过6位）
        "123456.A",  # 匹配失败（字母不足2位）
        "123456.ABC",  # 匹配失败（字母超过2位）
    ]

    for s in test_strings:
        print(s, reshape_code(s))

    df_ohlc = get_idx_quote(code="sh000852")


