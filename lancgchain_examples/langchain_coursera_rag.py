"""Simple RAG"""

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from langchain_openai.embeddings import OpenAIEmbeddings

# Choose the model
llm_model = "gpt-3.5-turbo-0301"
llm = ChatOpenAI(temperature=0.0, model=llm_model)
file = "Clothing.csv"

# Load the documents

loader = CSVLoader(file_path=file)
docs = loader.load()

# Embeddings
embeddings = OpenAIEmbeddings()
db = DocArrayInMemorySearch.from_documents(documents=docs, embedding=embeddings)

retriever = db.as_retriever()
qa_stuff = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    verbose=True
)

query = "Please give me a list of all sun protection shirts in a table" \
        "in markdown and summarize each one"
response = qa_stuff.run(query)