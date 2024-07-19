import os
#from dotenv import load_dotenv
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex

def query():
    query = input("Please ask your question here: ")
    #query = "Tell me which services are offered and what is the contact email address or phone?"
    return query

def main(url:str)-> None:
    while True:
        q = query()
        #print("QUERY:\n", q)
        try:
            if q == "exit":
                break
            documents = SimpleWebPageReader(html_to_text=True).load_data(urls=[url])
            index = VectorStoreIndex.from_documents(documents=documents)
            query_engine = index.as_query_engine()
            response = query_engine.query(q)
            print("Thinking...\n")
            print("ANSWER:\n", response)
        except: print("ERROR - Invalid URL")

if __name__ == '__main__':
    #load_dotenv()
    print("Starting Llamaindex...")
    url = input("Please put URL here (example: https://syntax.com/): ")
    main(url)