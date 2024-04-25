from openai import OpenAI
import streamlit as st


# page config
st.set_page_config(page_title="PythonBot",
                   page_icon=':sparkles:',
                   layout='centered',
                   initial_sidebar_state='collapsed')
st.title(":robot_face: Niki's PythonBot")
# set up open ai key
openai_key = st.secrets["OPENAI_API_KEY"]
# initialise chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def display_chat():
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.write(entry["content"])

# function to get model answer
def create_answer():
    # create answer
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=st.session_state.chat_history,
        temperature=0.7,
        top_p=1
    )
    # add that response to the chat history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content,
    })

# If we get a question, start doing stuff!
if question := st.chat_input(placeholder="Let's chat"):
    st.session_state.chat_history.append({
        "role": "user",
        "content": question,
    })
    create_answer()
    display_chat()
    