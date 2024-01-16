#1. Uncoment the below to install the environmental dependencies

! pip install streamlit 
! pip install OpenAI
! pip install langchain
! pip install wikipedia


#2. Set the value of the environment variable OPENAI_API_KEY to the your apikey
import os
os.environ['OPENAI_API_KEY'] = "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"

#3. Import StreamLit
import streamlit as st
# 4. Set the title using StreamLit
st.title(' TRG Support Chatbot ')
input_text = st.text_input('How can I help you? ')

# 5. Import the  prompt templates
from langchain.prompts import PromptTemplate
# 6.  Setup the prompt templates
title_template = PromptTemplate(
    input_variables = ['Infor'],
    template='Give me the list of  {concept} products'
)

script_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'],
    template='''Give me the list based on {title}
    while making use of the information and knowledge obtained from the Wikipedia research:{wikipedia_research}'''
)

# 7.  Import Conversation Buffer Memory
from langchain.memory import ConversationBufferMemory
# We use the ConversationBufferMemory to can be used to store a history of the conversation between the user and the language model.
# This information can be used to improve the language model's understanding of the user's intent, and to generate more relevant and coherent responses.

memoryT = ConversationBufferMemory(input_key='concept', memory_key='chat_history')
memoryS = ConversationBufferMemory(input_key='title', memory_key='chat_history')

# 8. Import OpenAI
from langchain.llms import OpenAI
# Importing the large language model OpenAI via langchain
model = OpenAI(temperature=0.6)

from langchain.chains import LLMChain
chainT = LLMChain(llm=model, prompt=title_template, verbose=True, output_key='title', memory=memoryT)
chainS = LLMChain(llm=model, prompt=script_template, verbose=True, output_key='script', memory=memoryS)

# 9. Import Wikipedia API Wrapper
from langchain.utilities import WikipediaAPIWrapper
wikipedia = WikipediaAPIWrapper()

# Display the output if the the user gives an input
if input_text:
    title = chainT.run(input_text)
    wikipedia_research = wikipedia.run(input_text)
    script = chainS.run(title=title, wikipedia_research=wikipedia_research)

    st.write(title)
    st.write(script)

    with st.expander('Wikipedia-based exploration: '):
        st.info(wikipedia_research)
