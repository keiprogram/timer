# main.py

import os
import time
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# ディレクトリが存在するか確認し、なければ作成
if not os.path.exists("data"):
    os.makedirs("data")

# タイトルと初期設定
st.title("学習特化型タイマーアプリ ⏳")
st.sidebar.header("タイマー設定")

# タイマーの集中時間と休憩時間を設定
focus_time = st.sidebar.number_input("集中時間 (分)", min_value=1, max_value=120, value=25)
break_time = st.sidebar.number_input("休憩時間 (分)", min_value=1, max_value=30, value=5)

# タスク入力フィールドと追加ボタン
task_input = st.sidebar.text_input("タスクを追加")
if st.sidebar.button("タスク追加"):
    if task_input:
        st.session_state["tasks"].append({"task": task_input, "completed": False})
        task_input = ""  # 入力欄をクリア

# タスクリストの初期化
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

# タスクリスト表示
st.header("📝 タスクリスト")
tasks = st.session_state["tasks"]

# タスクの状態更新
for i, task in enumerate(tasks):
    col1, col2 = st.columns([0.8, 0.2])
    col1.text(task["task"])  # タスク名表示
    if col2.checkbox("完了", key=f"task-{i}"):  # 完了チェックボックス
        task["completed"] = True  # タスクを完了に設定

# タイマー機能の初期化
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "timer_active" not in st.session_state:
    st.session_state["timer_active"] = False

# タイマーの開始とリセット機能
def start_timer():
    st.session_state["start_time"] = datetime.now()  # タイマーの開始時刻を記録
    st.session_state["timer_active"] = True

def reset_timer():
    st.session_state["start_time"] = None
    st.session_state["timer_active"] = False

# タイマーのスタート・リセットボタン
if st.button("タイマースタート"):
    start_timer()
elif st.button("タイマーリセット"):
    reset_timer()

# タイマーのリアルタイム表示
timer_display = st.empty()  # 動的に更新する領域を確保

while st.session_state["timer_active"]:
    # 経過時間の計算
    elapsed_time = (datetime.now() - st.session_state["start_time"]).seconds
    remaining_time = focus_time * 60 - elapsed_time  # 残り時間の計算
    if remaining_time <= 0:
        timer_display.markdown("<h1 style='text-align: center; color: red;'>⏰ 集中時間終了！休憩時間に入りましょう。</h1>", unsafe_allow_html=True)
        reset_timer()  # タイマーをリセット
        break
    else:
        minutes, seconds = divmod(remaining_time, 60)
        timer_display.markdown(f"<h1 style='text-align: center; font-size: 72px;'>{minutes}分 {seconds}秒</h1>", unsafe_allow_html=True)
        time.sleep(1)  # 1秒ごとに更新

# タイマー停止時の表示
if not st.session_state["timer_active"]:
    timer_display.write("タイマーが停止中です")

# セッションデータ保存の初期化
if "session_data" not in st.session_state:
    st.session_state["session_data"] = pd.DataFrame(columns=["date", "focus_time"])

# セッションデータ保存ボタンとデータ保存処理
if st.button("セッションを保存"):
    new_data = pd.DataFrame([{"date": datetime.now(), "focus_time": focus_time}])
    st.session_state["session_data"] = pd.concat([st.session_state["session_data"], new_data], ignore_index=True)
    # CSVファイルにデータ保存
    st.session_state["session_data"].to_csv("data/session_data.csv", index=False)
    st.success("セッションデータを保存しました！")

# 過去のセッションデータ表示
st.header("📊 学習履歴")
if os.path.exists("data/session_data.csv"):
    session_data = pd.read_csv("data/session_data.csv")
    st.line_chart(session_data.set_index("date")["focus_time"])

st.write("ご利用ありがとうございます！集中して学習を続けましょう💪✨")
