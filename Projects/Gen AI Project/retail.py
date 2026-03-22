import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_ollama import OllamaLLM

#page title
st.title("AI Retail Data Assistant")

st.write("Ask question about retail dataset:")

#connect database
db = SQLDatabase.from_uri("sqlite:///retail.db")

#load local llm
llm = OllamaLLM(model='llama3')

#create sql chain
db_chain = SQLDatabaseChain.from_llm(llm,db,verbose=True)

#user input 
user_question = st.text_input("Ask a question:")

#run query 
if user_question:
    response = db_chain.run(user_question)
    st.write(response)