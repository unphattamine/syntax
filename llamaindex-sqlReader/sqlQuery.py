# SQL connector to personal MySQL DB
# to demonstrate functionality of Llama-index
# with connection towards OpenAI API
# Stefan Olsavsky - 17.7.2024
# v_0.1

import os
import time
import openai
from colorama import Fore
from llama_index.core import SQLDatabase, Settings
from llama_index.core.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI
from sqlalchemy import create_engine, inspect

# Get environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')
db_password = os.environ.get('DB_PASS')
db_user = os.environ.get('DB_USER')

# Initiate MySQL variables and connection URI
db_host = "mysql80.r1.websupport.sk"
db_name = "llama_test"
db_port = "3314"
connection_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# Function to get the question from the user
def get_question():
    question = input("Please ask your question here: ")
    return question


# Trigger question
user_question = get_question()

# Create SQLAlchemy engine and inspect table names
print("\nCreating DB connection...")
engine = create_engine(connection_uri)
sql_database = SQLDatabase(engine)
inspector = inspect(engine)
table_names = inspector.get_table_names()
print("Please wait, I'm gettin' results from following tables", table_names, "from", db_name, "database...\n")
# Configure LLM settings
Settings.llm = OpenAI(temperature=0.5, model="gpt-3.5-turbo-16k")


# Set query function
def chat_to_sql(question: str | list[str], tables: list[str] | None = None, synthesize_response: bool = True):
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=tables,
        synthesize_response=synthesize_response,
        settings=Settings
    )

    try:
        start_time = time.time()
        response = query_engine.query(question)
        end_time = time.time()
        response_md = str(response)
        sql = response.metadata["sql_query"]
        duration = end_time - start_time
    except Exception as ex:
        response_md = "Error"
        sql = f"ERROR: {str(ex)}"
        duration = None

    print(Fore.GREEN + "Question:\t", question)
    print(Fore.RED + "Response:\t", response_md)
    print(Fore.BLUE + "\nSQL Query I ran:\n", sql)
    if duration is not None:
        print(Fore.WHITE + f"Query took me: {duration:.2f} seconds")


# Define query against DB
chat_to_sql(user_question, table_names)
