import os
from g4f import Provider, models
from langchain.llms.base import LLM
from langchain_g4f import G4FLLM
#from langchain import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory,ConversationSummaryBufferMemory
from langchain.agents import initialize_agent, load_tools
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
from langchain.agents import load_tools
#tools = load_tools(["serpapi"])
from langchain.llms import GPT4All
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.prompt_selector import ConditionalPromptSelector
from langchain.memory import ConversationBufferWindowMemory,CassandraChatMessageHistory, ConversationBufferMemory
# connect the db
import cassandra_db_connect
# define llm
llm: LLM = G4FLLM(
    model=models.gpt_35_turbo,
    #provider=Provider.GPTalk
)
# define memory handler
message_history = CassandraChatMessageHistory(
    session_id="adventure",
    session=cassandra_db_connect.session,
    keyspace=cassandra_db_connect.ASTRA_DB_KEYSPACE,
    ttl_seconds=3600
)
# clear history
message_history.clear()
# create buffer
cass_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history
    )
# the template
template = """you are now the guide of a my summer car journey in my summer car including all cars from my summer car and including the charactors from my summer car teimo, pena, jani, suski, fleetari, and the town and repair shop and including all parts for satsuma and including the start of my summer car whare the satsuma is just a body with no parts and no engine.
A mechanic named Sjaak seeks to upgrade the satsuma to the max and win the rally.
You must navigate him through challenges, choices and consequences, 
dynamically adapting the tale based on the mechanic's decisions.
Your goal is to create a branching narrative experience where each choice leads to a new path, 
ultimately determining Maarten's fate.

Here are some rules to follow:
1. Start by asking the player the following game start settings one by one
    A. to choose some kind of tools that will be used later in the game
    B. to choose a vehicle to drive trough the game
2. Add some of the mods from my summer car like the colt 1911 or plymouth dustman
3. Have a few paths that lead to succes
4. Have some paths that lead to death. 
5. If the user dies generate a response that explains the death and ends in the following text exactly:"Game Over.", I will search for this text to end the game.

Here is the chat history, use this to understand what to say next: {chat_history}
Human: {human_input}
AI:"""

# define prompt
prompt = PromptTemplate(
    input_variables=["chat_history","human_input"],
    template=template
)
# define chain
llm_chain=LLMChain(
    llm=llm,
    prompt=prompt,
    memory=cass_buff_memory
)
human_input= "start the game"
# game loop
while True:
    # generate response
    response = llm_chain.predict(human_input=human_input)
    # look for the end
    print(response.strip())
    if "Game over" in response:
        break
    # let player input a reply
    human_input = input("Your reply: ")
