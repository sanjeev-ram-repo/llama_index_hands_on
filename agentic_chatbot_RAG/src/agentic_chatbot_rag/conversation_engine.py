import streamlit as st
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from settings import CONVERSATION_FILE, GEMINI_LLM, INDEX_STORAGE


def load_chat_store() -> SimpleChatStore:
    """Load the chat store from the peristant directory

    Returns:
        SimpleChatStore: Returns the persisted store object.
    """
    try:
        chat_store = SimpleChatStore.from_persist_path(CONVERSATION_FILE)
    except FileNotFoundError:
        chat_store = SimpleChatStore()
    return chat_store


def display_messages(chat_store: SimpleChatStore, container: object) -> None:
    """Display messages from the chatstore in a streamlit container

    Args:
        chat_store (SimpleChatStore): Chatstore object
        container (object): Streamlit container object
    """
    with container:
        for message in chat_store.get_messages(key="0"):
            with st.chat_message(message.role):
                st.markdown(message.content)


def initialize_chatbot(
    user_name: str,
    study_subject: str,
    chat_store: SimpleChatStore,
    container: object,
    context: str,
) -> ReActAgent:
    """Initializes a chatbot with a ReAct agent.

    Args:
        user_name (str): Username who is going to use the bot.
        study_subject (str): The topic that we are dealing with.
        chat_store (SimpleChatStore): The chat storage
        container (object): Streamlit container
        context (str): The content from the slide for QA purposes.

    Returns:
        ReActAgent: Returns a ReAct agent.
    """

    memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000, chat_store=chat_store, chat_store_key="0"
    )
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE)
    index = load_index_from_storage(storage_context, index_id="vector")
    study_materials_engine = index.as_query_engine(similarity_top_k=3)
    study_materials_tool = QueryEngineTool(
        query_engine=study_materials_engine,
        metadata=ToolMetadata(
            name="study_materials",
            description=(
                f"Provides official information about "
                f"{study_subject}. Use a detailed plain "
                f"text question as input to the tool."
            ),
        ),
    )
    agent = ReActAgent.from_tools(
        tools=[study_materials_tool],
        GEMINI_LLM=GEMINI_LLM,
        memory=memory,
        system_prompt=(
            f"Your name is PITS, a personal tutor. Your "
            f"purpose is to help {user_name} study and "
            f"better understand the topic of: "
            f"{study_subject}. We are now discussing the "
            f"slide with the following content: {context}"
        ),
    )
    display_messages(chat_store, container)
    return agent


def chat_interface(agent, container) -> None:
    """Streamlit chat interface

    Args:
        agent (_type_): The ReAct agent.
        container (_type_): Streamlit container
    """
    prompt = st.chat_input("Type your question here:")
    if prompt:
        with container:
            with st.chat_message("user"):
                st.markdown(prompt)
            response = str(agent.chat(prompt))
            with st.chat_message("assistant"):
                st.markdown(response)
