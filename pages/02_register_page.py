import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

st.title("案件登録")

# データベース設定
DATABASE_URL = "mysql+pymysql://root:test@localhost/recruit"
engine = create_engine(DATABASE_URL)

def insert_job(job_title, company_name, job_category, job_description, required_skills, area, remote_work, prefecture, city, location_notes, billing_rate, salary_rate, average_annual_salary, expected_annual_salary_contract, expected_annual_salary_farewell, rate_notes, notes):
    """データベースに新しい案件を挿入する"""
    with engine.begin() as conn:  # トランザクション開始
        conn.execute(text("""
            INSERT INTO Jobs (JobTitle, CompanyName, JobCategory, JobDescription, RequiredSkills, Area, RemoteWork, Prefecture, City, LocationNotes, BillingRate, SalaryRate, AverageAnnualSalary, ExpectedAnnualSalaryContract, ExpectedAnnualSalaryFarewell, RateNotes, Notes) 
            VALUES (:job_title, :company_name, :job_category, :job_description, :required_skills, :area, :remote_work, :prefecture, :city, :location_notes, :billing_rate, :salary_rate, :average_annual_salary, :expected_annual_salary_contract, :expected_annual_salary_farewell, :rate_notes, :notes)
        """), {
            "job_title": job_title, "company_name": company_name, "job_category": job_category,
            "job_description": job_description, "required_skills": required_skills, "area": area,
            "remote_work": remote_work, "prefecture": prefecture, "city": city,
            "location_notes": location_notes, "billing_rate": billing_rate, "salary_rate": salary_rate,
            "average_annual_salary": average_annual_salary,
            "expected_annual_salary_contract": expected_annual_salary_contract,
            "expected_annual_salary_farewell": expected_annual_salary_farewell,
            "rate_notes": rate_notes, "notes": notes
        })

with st.form("job_form"):
    # 必須フィールドのラベルに赤字を使用
    st.markdown("**案件タイトル** *(必須)*", unsafe_allow_html=True)
    job_title = st.text_input("", key="job_title")

    st.markdown("**企業名** *(必須)*", unsafe_allow_html=True)
    company_name = st.text_input("", key="company_name")

    st.markdown("**職種カテゴリ** *(必須)*", unsafe_allow_html=True)
    job_category = st.text_input("", key="job_category")

    st.markdown("**仕事内容** *(必須)*", unsafe_allow_html=True)
    job_description = st.text_area("", key="job_description")

    st.markdown("**必要スキル** *(必須)*", unsafe_allow_html=True)
    required_skills = st.text_area("", key="required_skills")

    st.markdown("**地域** *(必須)*", unsafe_allow_html=True)
    area = st.text_input("", key="area")

    st.markdown("**リモートワーク** *(必須)*", unsafe_allow_html=True)
    remote_work = st.selectbox("", ["Yes", "No"], key="remote_work")

    st.markdown("**都道府県** *(必須)*", unsafe_allow_html=True)
    prefecture = st.text_input("", key="prefecture")

    st.markdown("**市区町村** *(必須)*", unsafe_allow_html=True)
    city = st.text_input("", key="city")

    # 任意フィールド
    location_notes = st.text_area("ロケーションに関する注記", key="location_notes")
    billing_rate = st.number_input("請求レート", format="%.2f", key="billing_rate")
    salary_rate = st.number_input("給与レート", format="%.2f", key="salary_rate")
    average_annual_salary = st.number_input("平均年収", format="%.2f", key="average_annual_salary")
    expected_annual_salary_contract = st.number_input("契約時期待年収", format="%.2f",
                                                      key="expected_annual_salary_contract")
    expected_annual_salary_farewell = st.number_input("退職時期待年収", format="%.2f",
                                                      key="expected_annual_salary_farewell")
    rate_notes = st.text_area("レートに関する注記", key="rate_notes")
    notes = st.text_area("その他の注記", key="notes")

    # フォーム送信ボタン
    submitted = st.form_submit_button("案件登録")

    # 必須項目が空の場合に警告を表示
    if submitted:
        if not all(
                [job_title, company_name, job_category, job_description, required_skills, area, remote_work, prefecture,
                 city]):
            st.warning("赤字で示された必須項目をすべて入力してください。")
        else:
            # データベースへの挿入処理を行う
            insert_job(job_title, company_name, job_category, job_description, required_skills, area, remote_work,
                       prefecture, city, location_notes, billing_rate, salary_rate, average_annual_salary,
                       expected_annual_salary_contract, expected_annual_salary_farewell, rate_notes, notes)
            st.success("案件が正しく登録されました。")

# 確認用に最近登録された案件を表示
st.write("### 最近登録された案件")
recent_jobs = pd.read_sql_query("SELECT * FROM Jobs ORDER BY JobID DESC LIMIT 5", engine)
st.dataframe(recent_jobs)