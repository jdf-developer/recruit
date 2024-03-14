import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# データベース設定
DATABASE_URL = "mysql+pymysql://root:test@localhost/recruit"
engine = create_engine(DATABASE_URL)

# セッション状態の取り扱いを簡易化
if 'jobs' not in st.session_state:
    st.session_state['jobs'] = pd.DataFrame()
if 'applied_jobs' not in st.session_state:
    st.session_state['applied_jobs'] = []

def load_skills():
    """利用可能なスキル一覧をデータベースからロード"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT RequiredSkills FROM Jobs"))
        skills = []
        for row in result:
            skills.extend(row[0].split(', '))
        return sorted(set(skills))

def search_jobs(selected_skills, min_salary, max_salary, selected_area):
    conditions = []
    params = {}
    if selected_skills:
        for i, skill in enumerate(selected_skills):
            conditions.append(f"RequiredSkills LIKE :skill{i}")
            params[f"skill{i}"] = f"%{skill}%"
    if min_salary is not None and max_salary is not None:
        conditions.append("AverageAnnualSalary >= :min_salary AND AverageAnnualSalary <= :max_salary")
        params["min_salary"] = min_salary
        params["max_salary"] = max_salary
    if selected_area:
        conditions.append("Area = :selected_area")
        params["selected_area"] = selected_area

    query_str = "SELECT * FROM Jobs WHERE " + " AND ".join(conditions) if conditions else "SELECT * FROM Jobs"
    query = text(query_str)

    with engine.connect() as conn:
        result = conn.execute(query, params)
        jobs = pd.DataFrame(result.fetchall(), columns=result.keys())
    return jobs

# 地域のリストを取得するための関数（ダミーのデータを返す）
def get_areas():
    return ['関東', '関西', '中部', '九州', '東北']

# 検索UIをサイドバーに移動
st.sidebar.title("案件検索")

available_skills = load_skills()
selected_skills = st.sidebar.multiselect("スキルで検索", available_skills)

min_salary, max_salary = st.sidebar.slider("給与範囲を選択", 0, 10000000, (3000000, 7000000), step=100000)

available_areas = get_areas()
selected_area = st.sidebar.selectbox("地域を選択", available_areas)

if st.sidebar.button("検索"):
    st.session_state.jobs = search_jobs(selected_skills, min_salary, max_salary, selected_area)

jobs = st.session_state.jobs

if not jobs.empty:
    for index, row in jobs.iterrows():
        with st.expander(f"{row['JobID']} - {row['JobTitle']}", expanded=True):
            st.write(f"**企業名:** {row['CompanyName']}")
            st.write(f"**必要スキル:** {row['RequiredSkills']}")
            st.write(f"**給与範囲:** {row['AverageAnnualSalary']}")
            st.write(f"**地域:** {row['Area']}")
            apply_button_clicked = st.button("応募する", key=f"apply_{row['JobID']}")
            if apply_button_clicked:
                st.session_state.applied_jobs.append(row['JobID'])
                st.success(f"案件「{row['JobTitle']}」に応募しました！")
else:
    st.write("条件に合う案件が見つかりませんでした。")
