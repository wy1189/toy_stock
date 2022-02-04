# -*- coding:utf-8 -*-
# @Filename:    hello.py
# @Author:      woojong
# @Time:        12/15/21 6:55 PM

import yfinance as yf
import justpy as jp
import numpy as np

target_markets = ["AMZN"]

Amazon = yf.Ticker("AMZN")

temp = Amazon.history(period="3mo", interval="1d")
temp['Close (SMA)'] = temp['Close'].rolling(7).mean()
# temp['Close (SMA)'] = temp['Close'].rolling(7, win_type="gaussian").mean(std=temp['Close'].std())
# temp['Close (SMA)'] = temp['Close (SMA)'].fillna('null')
temp_tz = temp.index.tz.zone if hasattr(temp.index.tz, "zone") else "US/Central"
print(temp.index[0])
temp.index = temp.index.strftime("%s").astype(int) * 1000

hc_colors = ["#7cb5ec", "#434348", "#90ed7d", "#f7a35c", "#8085e9",
             "#f15c80", "#e4d354", "#2b908f", "#f45b5b", "#91e8e1"]
chart_options = jp.Dict({
    "time": {
        "timezone": temp_tz
    },
    "chart": {
        "type": "spline",
        "scrollablePlotArea": {
            "minWidth": 5000,
            "scrollPositionX": 0
        }
    },
    "title": {
        "text": "Amazon"
    },
    "series": [{
        "name": "Amazon",
        "data": [{
            "x": x,
            "y": temp.loc[x, "Close"],
        } for x in temp.index]
    }, {
        "name": "Amazon (SMA)",
        "data": [{
            "x": x,
            "y": temp.loc[x, "Close (SMA)"],
        } for x in temp.index if not np.isnan(temp.loc[x, "Close (SMA)"])]
    }],
    "xAxis": {
        "type": "datetime",
        "labels": {
            "format": "{value: %b-%e}"
        }
    },
    "tooltip": {
        "xDateFormat": "%m/%d/%y %H:%M",
        "pointFormat": "<span style='color: "+ f"{hc_colors[0]}'>\u25CF</span>" + "{series.name}: <b>${point.y:.2f}</b>"
    }
})

wp = jp.WebPage(delete_flag=False, tailwind=True, debug=True)
wp.head_html = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment-timezone/0.5.13/moment-timezone-with-data-2012-2022.min.js"></script>
"""

hc = jp.HighCharts(a=wp, options=chart_options, style="width: 100%")


def stock_chart():
    return wp


jp.justpy(stock_chart)
