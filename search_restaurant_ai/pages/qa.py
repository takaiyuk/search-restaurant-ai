import langchain
import streamlit as st
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI

from search_restaurant_ai.modules.tools import tavily_search_tool

langchain.verbose = True


st.title("QA")

user_message = st.text_input(label="何を食べたいですか？")

if user_message:
    with st.spinner("考え中..."):
        tools = [tavily_search_tool]
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.OPENAI_FUNCTIONS,
        )

        messages = {
            "input": f"""
                {user_message}
                日本語で回答をお願いします
                インターネットの情報を用いて詳しく教えてください
                食べログ高評価
                駅からの距離が 1km 以内
                存在しない場合は「ありません」と回答してください
                存在する場合は、以下の項目を含んだものを 3 つリストアップして回答してください
                - [お店の名前](URL)
                    - 駅からの距離
                    - 種類
                    - 特徴
                    - 評価
                    - 価格帯
            """,
        }
        result = agent.run(messages)

        st.write(result)
