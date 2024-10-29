# main.py

import time
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# タイトルと初期設定
st.title("学習特化型タイマーアプリ ⏳")
st.sidebar.header("タイマー設定")
focus_time = st.sidebar.number_input("集中時間 (分)", min_value=1, max_value=120, value=25)
break_time = st.sidebar.number_input("休憩時間 (分)", min_value=1, max_value=30, value=5)
task_input = st.sidebar.text_input("タスクを追加")
if st.sidebar.button("タスク追加"):
    if task_input:
        tasks.append({"task": task_input, "completed": False})
        task_input = ""

# タスクリスト表示
st.header("📝 タスクリスト")
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

tasks = st.session_state["tasks"]

# タスクの状態更新
for i, task in enumerate(tasks):
    col1, col2 = st.columns([0.8, 0.2])
    col1.text(task["task"])
    if col2.checkbox("完了", key=f"task-{i}"):
        task["completed"] = True

# タイマー機能
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "timer_active" not in st.session_state:
    st.session_state["timer_active"] = False

def start_timer():
    st.session_state["start_time"] = datetime.now()
    st.session_state["timer_active"] = True

def reset_timer():
    st.session_state["start_time"] = None
    st.session_state["timer_active"] = False

if st.button("タイマースタート"):
    start_timer()
elif st.button("タイマーリセット"):
    reset_timer()

# タイマーのリアルタイム表示
timer_display = st.empty()  # 動的に更新する領域を確保

while st.session_state["timer_active"]:
    elapsed_time = (datetime.now() - st.session_state["start_time"]).seconds
    remaining_time = focus_time * 60 - elapsed_time
    if remaining_time <= 0:
        timer_display.write("⏰ 集中時間終了！休憩時間に入りましょう。")
        reset_timer()
        break
    else:
        minutes, seconds = divmod(remaining_time, 60)
        timer_display.write(f"残り時間: {minutes}分 {seconds}秒")
        time.sleep(1)  # 1秒ごとに更新

# タイマーが停止中の表示
if not st.session_state["timer_active"]:
    timer_display.write("タイマーが停止中です")

# セッションデータ保存
if "session_data" not in st.session_state:
    st.session_state["session_data"] = pd.DataFrame(columns=["date", "focus_time"])

if st.button("セッションを保存"):
    new_data = pd.DataFrame([{"date": datetime.now(), "focus_time": focus_time}])
    st.session_state["session_data"] = pd.concat([st.session_state["session_data"], new_data], ignore_index=True)
    st.session_state["session_data"].to_csv("data/session_data.csv", index=False)
    st.success("セッションデータを保存しました！")

# 過去のセッションデータ表示
st.header("📊 学習履歴")
if "session_data.csv" in st.session_state:
    session_data = pd.read_csv("data/session_data.csv")
    st.line_chart(session_data.set_index("date")["focus_time"])

st.write("ご利用ありがとうございます！集中して学習を続けましょう💪✨")
