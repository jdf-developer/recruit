import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# データベース設定
DATABASE_URL = "mysql+pymysql://root:test@localhost/recruit"
engine = create_engine(DATABASE_URL)

def get_users():
    """データベースからユーザー一覧を取得"""
    with engine.connect() as conn:
        users = pd.read_sql("SELECT * FROM users", conn)
    return users
st.title("ユーザー一覧")

# データベースからユーザー一覧を取得
users = get_users()

# ユーザー一覧を表示
if not users.empty:
    st.dataframe(users)
else:
    st.write("ユーザーが見つかりません。")
