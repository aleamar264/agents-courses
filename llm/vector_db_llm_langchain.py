import os

from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(api_key=openai_key, model="get-4")

# load documents

loader = DirectoryLoader(
    path="./data/new_articles/", glob="*.txt", loader_cls=TextLoader
)
document = loader.load()

print(document)


# Split the text
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n"], chunck_size=1000, chunk_overlap=20
)
documents = text_splitter.split_documents(document)
print(f"Number of documents: {len(documents)}")


embedding = OpenAIEmbeddings(api_key=openai_key, model="text-embedding-3-small")

persist_directory = "./db/chroma_db_real_world"

vectordb = Chroma.from_documents(
    documents=document, embedding=embedding, persist_directory=persist_directory
)

# Query the Chroma object
retriever = vectordb.as_retriever()
res_docs = retriever.invoke("How much did microsoft raise ?", k=5)


from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatMessagePromptTemplate

system_prompt = (
    "You are an assitant for question-answering task. Use the following pieces of "
    "retrieved context to answer the question. If you don't know the answer, say that you"
    "don't know. Use three sentences maximum and keep the answer concise"
    "\n\n"
    "{context}"
)

prompt = ChatMessagePromptTemplate.format_messages(
    [("system", system_prompt), ("human", "{input}")]
)
question_answer_chain = create_stuff_documents_chain(llm=model, prompt=prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


response = rag_chain.invoke({"input": "talk about databricks"})
res = response["answer"]
print(res)
