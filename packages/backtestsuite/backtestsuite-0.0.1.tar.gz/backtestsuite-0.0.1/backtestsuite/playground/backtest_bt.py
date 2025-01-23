# coding=utf-8


from backtestsuite.analysis.bt_analysis import CereBroAnalyse
from backtestsuite.quote.akshare_quote import get_idx_quote

if __name__ == '__main__':
    # 添加行情数据
    df_ohlc = get_idx_quote(code="sh000852")

    # 假设你有一个包含信号的DataFrame

    df_ohlc['vol_pct_60'] = df_ohlc['volume'] / df_ohlc['volume'].rolling(60).mean()

    df_ohlc['vol_pct_60_rank4y'] = df_ohlc['vol_pct_60'].rolling(252 * 4).rank(pct=True)
    df_ohlc['vol_abnormal_up'] = (df_ohlc['vol_pct_60_rank4y'] >= 0.95) * 1
    df_ohlc['vol_abnormal_down'] = (df_ohlc['vol_pct_60_rank4y'] <= 0.05) * 0

    df_ohlc['vol_abnormal_signal'] = df_ohlc['vol_abnormal_up'] + df_ohlc['vol_abnormal_down']
    df_ohlc['vol_abnormal_signal_9'] = df_ohlc['vol_abnormal_signal'].replace(0, None).ffill(limit=9).fillna(0)

    df_ohlc['Signal'] = (df_ohlc['vol_abnormal_signal_9'] - 0.5) * 2
    df_ohlc.to_excel('df_ohlc异常成交波动95only_v2.xlsx')
    df_ohlc_merged = df_ohlc

    # signal_data = pd.read_excel('df_ohlc_sh000852.xlsx').set_index('date')
    # # # signal_data = ['Signal']
    # #
    # signal_data.index = pd.to_datetime(signal_data.index)
    #
    # up_threshold = 0.5
    # down_threshold = -0.5
    # signal_data['Signal'] = (signal_data['SignalRaw'] >= up_threshold) * 1 + (
    #             signal_data['SignalRaw'] <= down_threshold) * -1
    # # signal_data = signal_data.reindex(index=df_ohlc.index).fillna(0)
    # # df_ohlc_merged = df_ohlc
    #
    # # signal_data.index = pd.to_datetime(signal_data.index)
    # # signal_data = signal_data.reindex(index=df_ohlc.index).fillna(0)
    # #
    # df_ohlc_merged = pd.merge(df_ohlc, signal_data[['Signal']], left_index=True, right_index=True)

    # Ch = CereBroShow(df_ohlc, start_dt='2010-01-01', end_dt=None, init_cash=100000.0, commission=0.001,
    #                  position_percents=50)
    #
    # result = Ch.run_signal(DoubleSMACloseSignal, signal_type=bt.SIGNAL_LONGSHORT)
    #
    # daily_return, positions, transactions, gross_lev = Ch.get_portfolio_info()
    #
    # # daily_return.name = 'returns'
    # # daily_return.index = pd.to_datetime(daily_return.index.tz_localize(None))
    # #
    # # benchmark = df_ohlc['close'].pct_change().dropna()
    # # benchmark.name = 'benchmark'
    #
    # Ch.plot()
    #
    # Ch.sumamry()
    #
    # metrics = Ch.qs_summary(daily_return, df_ohlc, output='test.html')

    full_strategy_name, metrics, stored_path = CereBroAnalyse.smart_run('异常成交波动95only_v2', df_ohlc_merged,
                                                                        cls_obj=None,
                                                                        start_dt='2010-01-01', end_dt=None,
                                                                        init_cash=100000.0,
                                                                        commission=0.001,
                                                                        position_percents=99,
                                                                        base_pth='./', signal_type='SIGNAL_LONG')

    print(metrics)
    pass
