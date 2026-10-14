import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_tavily import TavilySearch

load_dotenv()

model = init_chat_model("gpt-5.4-mini")

@tool
def get_weather(location: str) -> str:
    """특정 지역의 날씨 정보 조회 도구"""
    return f"{location}의 날씨는 -5도에 미세먼지는 매우 나쁨"

tavily_tool = TavilySearch(max_results=5, topic="general")

agent = create_agent(model, tools=[get_weather, tavily_tool])

st.title("1 페이지 입니다.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 기록 먼저 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("무엇이든 물어보세요")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = agent.invoke({"messages": st.session_state.messages})
    answer = response["messages"][-1].content

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)