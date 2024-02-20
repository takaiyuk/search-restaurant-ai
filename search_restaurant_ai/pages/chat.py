import langchain
import streamlit as st

from search_restaurant_ai.modules.agent import create_tavily_agent
from search_restaurant_ai.modules.st_utils import (
    ChatCommand,
    create_assitant_message,
    initialize_session_state,
    reset_state,
    search_with_agent,
    show_assistant_message,
    show_chat_log,
    show_latest_message,
    start_chat,
)

langchain.verbose = True

USER_NAME = "user"
ASSISTANT_NAME = "assistant"
DEBUG = False
TEMPERATURE = 0.0


st.title("Chat")

agent = create_tavily_agent(temperature=TEMPERATURE)

# チャットログを保存したセッション情報を初期化
initialize_session_state(st)

# アシスタントの最初のメッセージを表示
start_chat(st, ASSISTANT_NAME)

user_message = st.chat_input("ここにメッセージを入力してください")
search = st.button(ChatCommand.SEARCH.message)
reset = st.button(ChatCommand.RESET.message)

if user_message:
    # 以前のチャットログを表示
    show_chat_log(st)
    # 最新のメッセージを表示
    show_latest_message(st, USER_NAME, user_message)

    match user_message:
        case ChatCommand.SEARCH.message:
            assistant_message = search_with_agent(st, agent, USER_NAME, ASSISTANT_NAME, debug=DEBUG)
            # セッションにチャットログを追加
            st.session_state.chat_log.append({"name": USER_NAME, "msg": user_message})
            st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_message})
        case ChatCommand.RESET.message:
            reset_state(st, ASSISTANT_NAME)
        case _:
            # アシスタントのメッセージを作成・表示
            assistant_message = create_assitant_message(USER_NAME, user_message)
            show_assistant_message(st, ASSISTANT_NAME, assistant_message)
            # セッションにチャットログを追加
            st.session_state.chat_log.append({"name": USER_NAME, "msg": user_message})
            st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_message})

if search:
    # 以前のチャットログを表示
    show_chat_log(st)
    # 最新のメッセージを表示
    show_latest_message(st, USER_NAME, ChatCommand.SEARCH.message)

    search_with_agent(st, agent, USER_NAME, ASSISTANT_NAME, debug=DEBUG)

if reset:
    # 以前のチャットログを表示
    show_chat_log(st)
    # 最新のメッセージを表示
    show_latest_message(st, USER_NAME, ChatCommand.RESET.message)

    reset_state(st, ASSISTANT_NAME)
