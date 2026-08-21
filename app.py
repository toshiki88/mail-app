import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="メール返信作成AI", page_icon="✉️")

st.title("✉️ メール返信案 自動生成アプリ")
st.write("受信したメールと返信の希望を入力すると、適切な返信文章を作成します。")

# SecretsからAPIキーを取得
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY が設定されていません。StreamlitのSecretsを設定してください。")
    st.stop()

client = Groq(api_key=api_key)

# 入力フォーム
received_email = st.text_area("受信したメール本文:", height=150, placeholder="ここに相手から届いたメールを貼り付けてください")
reply_intent = st.text_area("返信の要点・希望:", height=100, placeholder="例: 来週火曜の14時は都合が悪いので、水曜の15時に変更してほしい旨を丁寧に伝える")

tone = st.selectbox("返信のトーン:", ["丁寧・ビジネス（標準）", "感謝を強調", "お詫び・謝罪", "カジュアル"])

if st.button("返信案を作成する", type="primary"):
    if not received_email or not reply_intent:
        st.warning("「受信したメール本文」と「返信の要点」の両方を入力してください。")
    else:
        with st.spinner("AIが返信案を作成中..."):
            prompt = f"""
以下の要件に従って、適切なメールの返信文を作成してください。

【受信したメール】
{received_email}

【返信の要点・伝えたい内容】
{reply_intent}

【トーン】
{tone}

【出力フォーマット】
件名: [適切な件名]

本文:
[適切な本文]
"""
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "あなたは優秀なビジネスメール作成アシスタントです。"},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                
                st.success("作成が完了しました！")
                st.text_area("生成された返信案:", value=response.choices[0].message.content, height=300)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
