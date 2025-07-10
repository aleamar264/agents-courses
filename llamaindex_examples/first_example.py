import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.readers.web import SimpleWebPageReader


def main(url:str)->None:
    documents = SimpleWebPageReader(html_to_text=True).load_data(urls=[url])
    index = VectorStoreIndex.from_documents(documents=documents)
    query_engine = index.as_query_engine()
    response = query_engine.query("About what is the web page?")
    print(response)

if __name__ == "__main__":
    load_dotenv()
    main(url="https://docs.llamaindex.ai/en/stable/examples/data_connectors/WebPageDemo/")