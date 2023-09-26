from langchain.chat_models import ChatOpenAI
from langchain import OpenAI

llm = ChatOpenAI(temperature=0, streaming=True)
llm1 = OpenAI(temperature=0, streaming=True)

def callFunction(value):
    if(value == 2) :
        return llm

    else:
        return llm1