from copy import deepcopy
from enum import Enum

import streamlit as st

from search_restaurant_ai.modules.agent import response_chatgpt


class ChatCommand(Enum):
    SEARCH = "search"
    RESET = "reset"

    def __str__(self):
        return self.value
    
    @property
    def message(self):
        match self:
            case ChatCommand.SEARCH:
                return "さがして"
            case ChatCommand.RESET:
                return "リセット"
            case _:
                raise ValueError(f"Invalid ChatCommand: {self}")

def initialize_session_state(st: st):
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []


def start_chat(st: st, assitant_name):
    with st.chat_message(assitant_name):
        st.write("こんにちは！探したいレストランの条件を教えてください")


def show_chat_log(st: st):
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])


def show_latest_message(st: st, user_name: str, user_message: str):
    with st.chat_message(user_name):
        st.write(user_message)


def search_with_agent(st, agent, user_name: str, assistant_name: str, debug: bool = False) -> str:
    user_messages = [chat["msg"] for chat in st.session_state.chat_log if chat["name"] == user_name]
    user_messages = "\n".join(user_messages)
    with st.chat_message(assistant_name):
        with st.spinner("考え中..."):
            response = response_chatgpt(agent, user_messages, debug=debug)
            assistant_response_area = st.empty()
            assistant_response_area.markdown(response)
    return response


def reset_state(st: st, assistant_name: str):
    st.session_state.chat_log = []
    with st.chat_message(assistant_name):
        assistant_response_area = st.empty()
        assistant_response_area.markdown("リセットしました")


def create_assitant_message(user_name: str, user_message: str):
    user_messages = [chat["msg"] for chat in st.session_state.chat_log if chat["name"] == user_name]
    user_messages.append(user_message)
    assistant_msg = deepcopy(user_messages)
    assistant_msg = [f"- {msg}" for msg in assistant_msg]
    assistant_msg.append("  \n他に条件はありませんか？")
    assistant_msg = "  \n".join(assistant_msg)
    return assistant_msg


def show_assistant_message(st: st, assistant_name: str, assistant_message: str):
    with st.chat_message(assistant_name):
        assistant_response_area = st.empty()
        assistant_response_area.markdown(assistant_message)
