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

# Initiate MySQL variables and connection URI
db_user = "solsavsky"
db_host = "mysql80.r1.websupport.sk"
db_name = "llama_test"
db_port = "3314"
connection_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create SQLAlchemy engine and inspect table names
engine = create_engine(connection_uri)
sql_database = SQLDatabase(engine)
inspector = inspect(engine)
table_names = inspector.get_table_names()

# Configure LLM settings
Settings.llm = OpenAI(temperature=0.5, model="gpt-3.5-turbo-16k")

#Set query function
def chat_to_sql(question: str | list[str], tables: list[str] | None = None, synthesize_response: bool = True):
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=tables,
        synthesize_response=synthesize_response,
        settings=Settings,
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

    print(Fore.GREEN + "Question:", question)
    print(Fore.RED + "Response:", response_md)
    print(Fore.BLUE + "SQL Query I ran:", sql)
    if duration is not None:
        print(Fore.WHITE + f"Query took me: {duration:.2f} seconds")

#Define query against DB

chat_to_sql("Which employee except AI consultans has the bigger earnings and what's his position? Do you know what his position means?", table_names)
