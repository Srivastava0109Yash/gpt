# Importing relevant documents-----------
from langchain import OpenAI ,LLMMathChain
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.chat_models import ChatOpenAI
import os
import chainlit as cl
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from LLM import *
from playbook import *
#End of import----------------------------


# LLM chain prompt template-------------

@cl.on_chat_start
def start():
    agent = initialize_agent(
        tools, callFunction(1), agent="zero-shot-react-description", verbose=True
    )
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")  
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(agent.run)(message, callbacks=[cb])