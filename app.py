import streamlit as st
from src import date_util
from src.metrics_cards import read_config
from src.metrics_cards import create_metrics_col
from src.metrics_cards import create_metrics_dailycases
from src.metrics_cards import create_metrics_dailycases_10m
from src.plot_figure import plot_new_cases
from src.plot_figure import plot_generation_severe_cases
from src.plot_figure import plot_newly_cases_stack
from src.plot_figure import plot_pcr_org
from src.plot_figure import plot_positive_rate

from src.prefecture_dictionary import create_pref_dict

st.set_page_config(
    page_title="厚労省DBクローン(streamlit)",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None)

st.warning("""技術的な検討のために厚労省ダッシュボードをクローンしたサイトです。
           政府オープンデータを使用していますが、各種指標の評価を目的としていませんので、数値は正しくない可能性があります。""")

st.markdown("## データからわかる -新型コロナウイルス感染症情報- のコピーダッシュボード(streamlit版)")
# info
conf = read_config("src/data.toml")
pref = create_pref_dict()

opt_prefecture = st.selectbox("都道府県ごとに閲覧できます。",
                              options=list(pref.keys()))

tab1, tab2 = st.tabs(["🏥感染者動向", "📊レベルの判断で参考とされる指標関連データ"])

with tab1:
    with st.spinner("Loading data..."):
        st.subheader("現在の状況")
        st.markdown(date_util.get_today() + "版")
        create_metrics_col("src/data.toml", pref[opt_prefecture][0])

        st.subheader("感染者動向")
        st.markdown(date_util.get_today() + "版")

        colplot1, colplot2, colplot3 = st.columns(3)

        with colplot1:
            st.markdown("### 新規陽性者数の推移(日別)")
            create_metrics_dailycases("src/data.toml", pref[opt_prefecture][0])

            period_1 = st.radio("グラフ表示期間", ("1週間", "1か月", "3か月", "1年"),
                                index=3, horizontal=True, key="radio1")
            st.altair_chart(plot_new_cases(
                period_1,
                url=conf["url"]["newly_confirmed_cases_daily"],
                ytick_space=50000,
                color="#fd6262",
                prefecture=pref[opt_prefecture][0]),
                use_container_width=True,
            )

        with colplot2:
            st.markdown("### 人口10万人当たり新規陽性者数")
            create_metrics_dailycases_10m("src/data.toml", pref[opt_prefecture][0])

            period_2 = st.radio("グラフ表示期間", ("1週間", "1か月", "3か月", "1年"),
                                index=3, horizontal=True, key="radio2")
            st.altair_chart(plot_new_cases(
                period_2,
                url=conf["url"]["newly_confirmed_cases_per_100_thousand_population_daily"],
                ytick_space=40,
                color="#a1b8e8",
                prefecture=pref[opt_prefecture][0]),
                use_container_width=True,
            )

        with colplot3:
            st.markdown("### 性別・年代別新規陽性者数(週別)")
            st.altair_chart(plot_generation_severe_cases(
                url=conf["url"]["newly_confirmed_cases_detail_weekly"],
                prefec_order=pref[opt_prefecture][1]
            ),
                use_container_width=True)

with tab2:
    with st.spinner("Loading data..."):
        with st.expander("レベル分類の考え方とレベル判断のための指標について", expanded=False):
            st.write("""
                    厚生労働省のこのページに使用されているデータはアクセスできないものが多かったため、ありあわせのデータで取り繕っています。
                    再現不可能なものは諦め、なんとかなりそうなデータ(陽性率とか)は適当に取り繕いました。
                    """)

        st.subheader("レベルの判断で参考とされる指標関連データ")
        st.markdown(date_util.get_today() + "版")

        colplot_1, colplot_2, colplot_3 = st.columns(3)
        with colplot_1:
            st.markdown("### 新規感染者報告数")
            st.altair_chart(plot_newly_cases_stack(
                url=conf["url"]["newly_confirmed_cases_detail_weekly"]
            ), use_container_width=True)

        with colplot_2:
            st.markdown("### 検査状況")
            st.altair_chart(plot_pcr_org(
                url=conf["url"]["pcr_case_daily"]
            ), use_container_width=True)

        with colplot_3:
            st.markdown("### 陽性率")
            st.altair_chart(plot_positive_rate(
                url_pcr=conf["url"]["pcr_tested_daily"],
                url_detected=conf["url"]["newly_confirmed_cases_daily"]
            ), use_container_width=True)
