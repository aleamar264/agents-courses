import os

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

pinecone_key = os.getenv("PINECONE_API")
openai_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(api_key=openai_key, model="gpt-3.5")

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


pc = Pinecone(api_key=pinecone_key)
index_name = "tester-index"

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if index_name not in index_name:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
index = pc.Index(index_name)
from langchain_pinecone import PineconeVectorStore

docsearch = PineconeVectorStore.from_documents(
    documents=documents, embedding=embedding, index_name=index_name, index=index
)

retriever = docsearch.as_retriever()

# query = "tell me about writter strike"
# docs = docsearch.similarity_search(query)
# print(docs)


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
