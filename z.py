# Importing relevant documents-----------
from langchain import OpenAI ,LLMMathChain
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.chat_models import ChatOpenAI
import os
import chainlit as cl
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
#End of import----------------------------


# LLM chain prompt template-------------
prompt = PromptTemplate(
    input_variables=["query"],
    template="{query}"
    )


def integral(x: str):
    return x*4

def loss_from_operation(x: list)->int:
    print(type(x))
    """Returns loss from operation given current year stub and last year stub and last year cost of revnue."""
    #a,b=[int(i) for i in x.split(" ")]
    values = x[1:-1].split(", ")
    a, b, c = map(int, values)
    return a-b+c

def depriciation_and_amoritization(x: list)->int:
    print(type(x))
    """Returns depriciation and amoritization given current year stub and last year stub and last financial year's depriciation and amoritization """
    #a,b=[int(i) for i in x.split(" ")]
    values = x[1:-1].split(", ")
    a, b ,c= map(int, values)
    return a-b+c

def fully_diluted_enterprise_value(x: list) -> int:
    """Calculates Fully Diluted Enterprise Value based on Fully Diluted Equity Value, total debt, and cash and cash equivalents."""
    
    # Fill missing values with zeros
    while len(x) < 3:
        x.append(0)
        
    fully_diluted_equity_value, total_debt, cash_and_cash_equivalents = x
    
    fully_diluted_enterprise_value = fully_diluted_equity_value + total_debt - cash_and_cash_equivalents
    
    return fully_diluted_enterprise_value

def total_diluted_shares_outstanding(x: list) -> int:
    """Calculates the total diluted shares outstanding based on basic shares outstanding, restricted stock options, stock options, restricted stock units, restricted stock awards, and convertible debt securities."""
    
    # Fill missing values with zeros
    while len(x) < 6:
        x.append(0)
        
    basic_shares, restricted_stock_options, stock_options, restricted_stock_units, restricted_stock_awards, convertible_debt_securities = x
    
    total_diluted_shares = (basic_shares + restricted_stock_options + stock_options + 
                             restricted_stock_units + restricted_stock_awards + convertible_debt_securities)
    
    return total_diluted_shares

def total_debt(x: list) -> int:
    """Calculates the total debt based on short-term debt (also known as current debt) and long-term debt."""
    
    # Fill missing values with zeros
    while len(x) < 2:
        x.append(0)
        
    short_term_debt, long_term_debt = x
    
    total_debt_value = short_term_debt + long_term_debt
    
    return total_debt_value

def cash_and_cash_equivalents(x: list) -> int:
    """Calculates Cash & Cash Equivalents based on Cash at Bank and Marketable Securities."""
    
    # Fill missing values with zeros
    while len(x) < 2:
        x.append(0)
        
    cash_at_bank, marketable_securities = x
    
    cash_and_cash_equivalents_value = cash_at_bank + marketable_securities
    
    return cash_and_cash_equivalents_value

#------

def stock_options(x: list) -> int:
    """Calculates stock options based on share price, exercise price, and units."""
    share_price, exercise_price, units = x
    
    if share_price > exercise_price:
        result = units - (units * exercise_price) / share_price
        
        if result.is_integer():
            return int(result)
        else:
            raise ValueError("Invalid input values. The result is not an integer.")
    else:
        return 0



def basic_shares_outstanding(x: list) -> int:
    """Returns the basic share outstanding."""
    print(x)
    seriesA,seriesB,seriesC=x[0],x[1],x[2]
    basic_shares_outstanding_result= seriesA+seriesB+seriesC
    return basic_shares_outstanding_result

def research_and_development(x: list)->int:
    print(type(x))
    """Returns research and development given current year stub and last year stub and last year value of research and development."""
    #a,b=[int(i) for i in x.split(" ")]
    values = x[1:-1].split(", ")
    a, b, c = map(int, values)
    return a-b+c

def fully_diluted_enterprise_value(x: list) -> int:
    """Calculates Fully Diluted Enterprise Value based on Fully Diluted Equity Value, total debt, and cash and cash equivalents."""
    
    # Fill missing values with zeros
    while len(x) < 3:
        x.append(0)
        
    fully_diluted_equity_value, total_debt, cash_and_cash_equivalents = x
    
    fully_diluted_enterprise_value = fully_diluted_equity_value + total_debt - cash_and_cash_equivalents
    
    return fully_diluted_enterprise_value


 
def ev_to_ltm_revenue(x: list) -> float:
    """Calculates the ratio of Enterprise Value (EV) to Last Twelve Months (LTM) Revenue."""
    
    # Fill missing values with zeros
    while len(x) < 2:
        x.append(0)
        
    enterprise_value, ltm_revenue = x
    
    # Check for division by zero
    if ltm_revenue == 0:
        raise ValueError("LTM Revenue cannot be zero.")
    
    ev_to_ltm_revenue_ratio = enterprise_value / ltm_revenue
    
    return ev_to_ltm_revenue_ratio


# End of python PlayBooks------------------------------

@cl.on_chat_start
def start():
    llm = ChatOpenAI(temperature=0, streaming=True)
    llm1 = OpenAI(temperature=0, streaming=True)
    llm_math_chain = LLMMathChain.from_llm(llm=llm1, verbose=True)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    tools = [
        Tool(
            name='Language Model',
            func=llm_chain.run,
            description='use this tool for general purpose queries, logic and general conversations like Hi hello etc'
        ),
        Tool(
            name="integral",
            func=integral,
            description="useful for when you need to find integral of a string",
        ),
        Tool(
            name="Basic_Share_Outstanding",
            func=basic_shares_outstanding,
            description="Returns the basic share outstanding when you are given series a , series b and series c shares of a company. give the input to this as a python list object.",
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math",
        ),
        Tool(
            name="loss_from_operation",
            func=loss_from_operation,
            description='''Returns loss from operation when you are given three values for a company 
                           that is current year stub , last year stub of a company and last year cost
                           of revnue, give the Action Input: as list of 3 integers only. Rememebr
                           the order 1. current year stub , 2. last year stub, 3. ast year cost of revnue'''
        ),
        Tool(
            name='depriciation and amoritization',
            func=depriciation_and_amoritization,
            description='''use this tool depriciation and amoritization given current year stub and last year stub and last financial years depriciation and amoritization,
                           give the Action input as: list of 3 integers only. remember the order: 1. current year stub 2. last year stub and 3. last financial years depriciation and amoritization'''
        ),
        Tool(
            name='Research and Development',
            func=research_and_development,
            description='''Use this tool to find Research and Development cost given current year stub and last year stub and last financial years Research and Development cost,
                           give the Action input as: list of 3 integers only. remember the order: 1. current year stub 2. last year stub and 3. last financial years Research and Development cost'''
        ),
        
        Tool(name='total debt',
             func=total_debt,
             description='Calculates the total debt based on short-term debt (also known as current debt) and long-term debt.'
            
        ),
        Tool( name='cash in cash equivalent',
             func=cash_and_cash_equivalents,
             description='Calculates Cash & Cash Equivalents based on Cash at Bank and Marketable Securities.'
             ),
        
        Tool(name='fully diluted enterprise value',
             func=fully_diluted_enterprise_value,
             description='Calculates Fully Diluted Enterprise Value based on Fully Diluted Equity Value, total debt, and cash and cash equivalents'
             ),
        
        Tool(name='ev to ltm revenue',
             func=ev_to_ltm_revenue,
             description='Calculates the ratio of Enterprise Value (EV) to Last Twelve Months (LTM) Revenue'
             ),
        
        Tool(name='total diluted  share outstanding',
             func=total_diluted_shares_outstanding,
             description='Calculates the total diluted shares outstanding based on basic shares outstanding, restricted stock options, stock options, restricted stock units, restricted stock awards, and convertible debt securities.'
             ),
        Tool(
            name='stock options',
            func=stock_options,
            description='Calculates stock options based on share price, exercise price, and units.'
        )
        
    ]
    agent = initialize_agent(
        tools, llm1, agent="zero-shot-react-description", verbose=True
    )
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(agent.run)(message, callbacks=[cb])