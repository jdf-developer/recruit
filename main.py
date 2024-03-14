import streamlit as st

st.set_page_config(layout="wide")

# アプリケーションのタイトル
st.title('ようこそ！')

# ウェルカムメッセージ
st.header('案件管理システムへようこそ')

# アプリケーションの説明
st.write('''
このアプリケーションでは、以下の機能を利用できます：
- **案件検索**：利用可能な案件を検索し、詳細を確認することができます。
- **案件登録**：新しい案件をシステムに登録することができます。

左のサイドバーからご希望の機能を選択してください。
''')

# 任意の追加情報や説明をここに追加することができます。
# 例えば、アプリケーションの使用方法に関するビデオやドキュメントへのリンクなどを提供することができます。
