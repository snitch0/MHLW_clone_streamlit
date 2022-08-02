import streamlit as st

import pandas as pd
import tomli


class MetricData:
    def __init__(self, title: str, num: int, diff: float = 0) -> None:
        self.title: str = title
        self.num: str = "{:,}".format(num) + "人"
        if num:
            self.diff: str = "{:,}".format(diff) + "人"
        else:
            self.diff = ""
        
    def to_card_info(self):
        if self.diff:
            return (self.title, self.num, self.diff)
        else:
            return (self.title, self.num, None)
        

def metrics_get_diff(url: str, pref: str) -> tuple[int, int]:
    df = pd.read_csv(url)
    num = df[pref]
    today_num = num.iloc[-1]
    diff = today_num - num.iloc[-2]
    return today_num, diff

def metrics_cumulative_newly_cases(url: str, pref: str) -> int:
    df = pd.read_csv(url)
    return df[pref].sum()

def read_config(configpath: str):
    with open(configpath, 'rb') as f:
        config: dict = tomli.load(f)
        return config
        
def week_average(url: str, week_shift: int, pref: str) -> int:
    df = pd.read_csv(url)
    ave = df[pref].iloc[-8-(7*week_shift):-1-(7*week_shift)].mean()
    return int(ave)
    
def new_cases_p_10thousand(url: str, pref: str):
    df = pd.read_csv(url)
    return int(df["ALL"].iloc[-1]), int(df["ALL"].iloc[-2]) - int(df["ALL"].iloc[-1])
    
def create_metrics_col(configpath: str, pref: str) -> None:
    conf = read_config(configpath)
    
    new_cases_url = conf["url"]["newly_confirmed_cases_daily"]
    nc_v1, nc_v2 = metrics_get_diff(new_cases_url, pref)

    cumulative_url = conf["url"]["newly_confirmed_cases_daily"]
    cl_v = metrics_cumulative_newly_cases(cumulative_url, pref)

    severe_url = conf["url"]["severe_cases_daily"]
    sv_v1, sv_v2 = metrics_get_diff(severe_url, pref)
    
    death_url = conf["url"]["deaths_cumulative_daily"]
    dt_v1, dt_v2 = metrics_get_diff(death_url, pref)
    
    t1_col1, t1_col2, t1_col3, t1_col4 = st.columns(4)
    
    t1_col1.metric(* MetricData("新規の陽性者数", nc_v1, nc_v2).to_card_info())
    t1_col2.metric(* MetricData("陽性者数の累積", cl_v, 0).to_card_info())
    t1_col3.metric(* MetricData("現在の重症者数", sv_v1, sv_v2).to_card_info())
    t1_col4.metric(* MetricData("新規の陽性者数", dt_v1, dt_v2).to_card_info())
    
def create_metrics_dailycases(configpath: str, pref: str):
    conf = read_config(configpath)
    
    new_cases_url = conf["url"]["newly_confirmed_cases_daily"]
    nc_v1, nc_v2 = metrics_get_diff(new_cases_url, pref)

    w1_v = week_average(new_cases_url, 0, pref)
    w2_v = week_average(new_cases_url, 1, pref)
    
    df = pd.DataFrame(
        {
            "新規陽性者数": ["{:,}".format(nc_v1)],
            "1週間平均": ["{:,}".format(w1_v)],
            "前週平均": ["{:,}".format(w2_v)]
        }
    )
    st.table(df)

def create_metrics_dailycases_10m(configpath: str, pref: str):
    conf = read_config(configpath)
    
    new_cases_10m_url = conf["url"]["newly_confirmed_cases_per_100_thousand_population_daily"]
    w1_v, w2_v = new_cases_p_10thousand(new_cases_10m_url, pref)
    df = pd.DataFrame(
        {
            "新規陽性者数": [f"{w1_v} /10万人"],
            "前日比": [f"{w2_v} /10万人"]
        }
    )
    st.table(df)