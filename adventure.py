import os
from g4f import Provider, models, Model,RetryProvider
from langchain.llms.base import LLM
from langchain_g4f import G4FLLM
#from langchain import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory,ConversationSummaryBufferMemory, CombinedMemory
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
from templates import my_summer_car_template, gta4_template, map_prompt
# define models
model35=Model(
    name="gpt_3.5_turbo",
    base_provider="openai",
    best_provider=RetryProvider([
                                Provider.GptGo,
                                Provider.NoowAi,
                                Provider.FreeGpt,
                                Provider.GeekGpt,
                                Provider.ChatgptAi
                            ])
)
#print(dir(models))

"""
['AiAsk', 'Aichat', 'Bard', 'BaseProvider', 'Bing', 'ChatBase', 'ChatgptAi', 'ChatgptX', 'FakeGpt', 
'FreeGpt', 'GPTalk', 'GeekGpt', 'GptChatly', 'GptForLove', 'GptGo', 'H2o', 'Model', 'ModelUtils', 
'NoowAi', 'Phind', 'RetryProvider', 'Union', 'Vercel', 'You', 
'_all_models', 'annotations', 'bloom', 'claude_instant_v1', 'claude_v1', 'claude_v2', 
'code_davinci_002', 'command_light_nightly', 'command_nightly', 'dataclass', 'default', 
'falcon_40b', 'falcon_7b', 'flan_t5_xxl', 'gpt_35_long', 'gpt_35_turbo', 'gpt_35_turbo_0613', 
'gpt_35_turbo_16k', 'gpt_35_turbo_16k_0613', 'gpt_4', 'gpt_4_0613', 'gpt_4_32k', 'gpt_4_32k_0613', 
'gpt_neox_20b', 'llama13b_v2_chat', 'llama70b_v2_chat', 'llama7b_v2_chat', 'llama_13b', 
'oasst_sft_1_pythia_12b', 'oasst_sft_4_pythia_12b_epoch_35', 'palm', 'santacoder', 
'text_ada_001', 'text_babbage_001', 'text_curie_001', 'text_davinci_002', 'text_davinci_003']
"""


#TODO: get better free llm, G4FLLM is not always stable
# define llm
llm: LLM = G4FLLM(
    model=models.gpt_35_turbo,
    #model=model35,
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

# create buffer memory
cass_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history,
    input_key="chat_history"
)
# creat summary memory
summary_memory = ConversationSummaryMemory(
    llm=llm, 
    chat_memory=message_history,
    input_key="chat_history"
)
#combine the memory types
memory = CombinedMemory(memories=[cass_buff_memory, summary_memory])

# define prompt
prompt = PromptTemplate(
    input_variables=["chat_history","human_input"],
    #template=my_summer_car_template
    template=gta4_template
)

# define buffer window memory chain
llm_combined_memory_chain=LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)
# define buffer memory chain
llm_chain=LLMChain(
    llm=llm,
    prompt=prompt,
    memory=cass_buff_memory
)
# initiating prompt
human_input= "start the game"
# game loop
while True:
    if "/map" in human_input:
        response = llm_chain.predict(human_input="Show a ascii representation of the total path the player has taken")
        #response = llm_combined_memory_chain.predict(human_input=map_prompt)
    else:
        # generate response
        response = llm_chain.predict(human_input=human_input)
        #response = llm_combined_memory_chain.predict(human_input=human_input)

    # look for the end
    print(response.strip())
    if "Game over" in response:
        break
    # let player input a reply
    human_input = input("Your reply: ")
