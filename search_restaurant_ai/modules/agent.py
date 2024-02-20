from typing import Any

from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI

from search_restaurant_ai.modules.tools import tavily_search_tool


def create_tavily_agent(tools: list[Any] = None, model_name: str = "gpt-3.5-turbo", temperature: float = 0.0) -> Any:
    if tools is None:
        tools = [tavily_search_tool]
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
    )
    return agent


def response_chatgpt(agent: Any, user_message: str, input_template: str | None =None, debug: bool = False) -> str:
    if debug:
        return "DEBUG: response_chatgpt"
    if input_template is None:
        input_value = f"""{user_message}
日本語で回答
インターネットの情報で詳しく
食べログの点数が高い店
駅からの距離が 1km 以内
存在しない場合は「ありません」と回答
存在する場合は以下の項目を含んで 3 つリストアップして回答、店名の重複は除外
- [店名](URL)
  - 駅からの距離
  - 種類
  - 特徴
  - 評価
  - 価格帯"""
    else:
        input_value = f"{user_message}{input_template}"
    messages = {"input": input_value}
    response = agent.run(messages)
    return response
