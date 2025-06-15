import os
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

openai_api_key = os.getenv("OPENAI_API_KEY")

st.write("APIキー:", openai_api_key)  # 一時的な確認用

chat = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)



# Streamlitアプリのタイトルと説明
st.title("LLM専門家アプリ")
st.write("""
このアプリでは、専門家を選んで質問を投げかけることができます。  
選択した専門家になりきったLLMが回答してくれます。
""")

# 専門家の選択肢を定義
expert_type = st.radio(
    "相談したい専門家を選んでください：",
    ("医者", "弁護士", "栄養士")
)

# 専門家の種類に応じたシステムメッセージを設定
def get_system_prompt(expert):
    if expert == "医者":
        return "あなたは親切で信頼できる日本人の医者です。患者に医学的アドバイスを分かりやすく提供してください。"
    elif expert == "弁護士":
        return "あなたは経験豊富な日本の弁護士です。法律の観点からユーザーの相談に対応してください。"
    elif expert == "栄養士":
        return "あなたはプロの栄養士です。ユーザーの健康や食生活の相談に専門的に答えてください。"
    else:
        return "あなたは親切なアシスタントです。"

# 入力テキスト
user_input = st.text_input("質問を入力してください：")

# 回答を取得する関数
def get_response(expert, user_message):
    system_prompt = get_system_prompt(expert)
    chat = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    response = chat(messages)
    return response.content

# ボタンを押すと回答が表示される
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("考え中..."):
            answer = get_response(expert_type, user_input)
            st.success("回答：")
            st.write(answer)
