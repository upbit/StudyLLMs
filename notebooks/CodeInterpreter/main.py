import os
import logging
import openai
import asyncio
from dotenv import dotenv_values
import streamlit as st
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from CodeInterpreter import CodeInterpreter

# logging.basicConfig(filename='steps.log', encoding='utf-8', level=logging.DEBUG)


CHATGPT_SYSTEM_PROMPT = """You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture.

Knowledge cutoff: 2022-01

Current date: 2023-11-11"""


@st.cache_resource(show_spinner=False)
def create_kernel():
    with st.spinner(text="Connect to GPT-4 and Python Kernel..."):
        # export OPENAI_API_BASE=https://api-qpilot.woa.com/v1
        # Prepare OpenAI service using credentials stored in the `.env` file
        current_path = os.path.split(os.path.realpath(__file__))[0]
        cfg = dotenv_values(os.path.join(current_path, ".env"))

        async_client = openai.AsyncOpenAI(
            api_key=cfg["OPENAI_API_KEY"], base_url=cfg["OPENAI_API_BASE"]
        )

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        kernel = sk.Kernel(log=logger)
        kernel.add_chat_service(
            "chat-gpt",
            OpenAIChatCompletion("gpt-4", async_client=async_client, log=logger),
        )
        return kernel


def show_history():
    avators = {
        "user": "🧑‍💻",
        "assistant": "🤖",
        "system": "🦖",
    }
    for msg in st.session_state.history:
        role = msg["role"]
        with st.chat_message(role, avatar=avators[role]):
            # st.write(msg["content"])
            st.markdown(msg["content"])


def main():
    st.set_page_config(
        page_title="Code Interpreter with GPT-4",
        page_icon=":rocket:",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("Code Interpreter")
    st.markdown(
        "<sub>Code Interpreter 使用 jupyter kernel 执行代码，请确认执行环境安全后再与大模型交互</sub>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        top_p = st.slider("top_p", 0.0, 1.0, 0.7, step=0.01)
        temperature = st.slider("temperature", 0.0, 1.5, 0.9, step=0.01)
        max_new_token = st.slider("Output length", 5, 32000, 2048, step=1)

        cols = st.columns(2)
        export_btn = cols[0]
        clear_history = cols[1].button("Clear History", use_container_width=True)
        retry = export_btn.button("Retry", use_container_width=True)

        system_prompt = st.text_area(
            label="System Prompt", height=300, value=CHATGPT_SYSTEM_PROMPT
        )

    kernel = create_kernel()

    if "history" not in st.session_state.keys():
        kernel = create_kernel()
        content = kernel.create_new_context()
        st.session_state.history = [
            {"role": "system", "content": system_prompt},
        ]

    prompt_text = st.chat_input("Chat with GPT-4", key="chat_input")

    if clear_history:
        print("\n== Clean ==\n")
        st.session_state.history = [
            {"role": "system", "content": system_prompt},
        ]
        return

    if prompt_text:
        st.session_state.history.append({"role": "user", "content": prompt_text})
        show_history()

        response = asyncio.run(
            chat(kernel, st.session_state.history, top_p, temperature, max_new_token)
        )
        st.session_state.history.append({"role": "assistant", "content": response})

    show_history()


async def chat(kernel, session_history, top_p, temperature, max_tokens) -> str:
    sk_prompt = """{{$system}}

{{$history}}
assistant: 
""".strip()
    chat_function = kernel.create_semantic_function(
        prompt_template=sk_prompt,
        function_name="Chat",
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
    )

    context = kernel.create_new_context()
    history = []
    for msg in session_history:
        if msg["role"] == "system":
            context["system"] = msg["content"]
        else:
            history.append("{}: {}".format(msg["role"], msg["content"]))
    context["history"] = "\n".join(history)

    gpt_answer = await chat_function.invoke_async(context=context)
    print("assistant:", gpt_answer)
    return gpt_answer


if __name__ == "__main__":
    main()
