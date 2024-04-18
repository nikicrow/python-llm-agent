from langchain.memory import ConversationBufferMemory 
from langchain.agents import AgentExecutor
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
import streamlit as st
from langchain_experimental.tools import PythonREPLTool
from langchain.memory import ChatMessageHistory
from langchain.agents import load_tools
from langchain import hub
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_openai_functions_agent


# page config
st.set_page_config(page_title="PythonBot",
                   page_icon=':sparkles:',
                   layout='centered',
                   initial_sidebar_state='collapsed')
st.title(":robot_face: Niki's PythonBot")
# set up open ai key
openai_key = st.secrets["OPEN_AI_KEY"]
# initialise chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# add memory to the chat for conversation history
formatted_chat_history = ChatMessageHistory()
for message in st.session_state.chat_history:
    if message['role']=='user':
        formatted_chat_history.add_user_message(message['content'])
    elif message['role']=='assistant':
        formatted_chat_history.add_ai_message(message['content'])
memory = ConversationBufferMemory(chat_memory=formatted_chat_history,
                                    return_messages=True,
                                    memory_key="chat_history",
                                    output_key="output")
tools = [PythonREPLTool()]

instructions = """You are an agent designed to write and execute python code to answer questions.
You have access to a python REPL, which you can use to execute python code.
If you get an error, debug your code and try again.
Only use the output of your code to answer the question. 
You might know the answer without running any code, but you should still run the code to get the answer.
Always put the code you wrote in the output and print any images of charts you create.
If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
"""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)
# load model from open AI
llm = ChatOpenAI(model_name = "gpt-3.5-turbo-0125",
                    openai_api_key = openai_key,
                    temperature = 0.2, 
                    streaming=True)

agent = create_openai_functions_agent(llm, 
                                      tools, 
                                      prompt)

agent_executor = AgentExecutor(agent=agent, 
                               tools=tools, 
                               verbose=True,
                               memory=memory)


def display_chat():
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.write(entry["content"])

# function to get model answer
def create_answer(question):
    # create answer
    result = agent_executor.invoke({'input':question})
    # add that message too the chat history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result["output"],
    })

# If we get a question, start doing stuff!
if question := st.chat_input(placeholder="Let's chat"):
    st.session_state.chat_history.append({
        "role": "user",
        "content": question,
    })
    create_answer(question)
    display_chat()
    