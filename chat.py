from langchain.embeddings import HuggingFaceEmbeddings
from llama_index.indices.prompt_helper import PromptHelper
from langchain import OpenAI
from llama_index import SimpleDirectoryReader, GPTListIndex,GPTVectorStoreIndex
from llama_index import LLMPredictor, ServiceContext
import sys
#from google.colab import drive
import os

#os.environ["OPENAI_API_KEY"] = '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'

os.environ["OPENAI_API_KEY"] = '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'


def construct_index(directory_path):
  # set maximum input size
  max_input_size = 4096
  # set number of output tokens
  num_outputs = 256
  # set maximum chunk overlap
  max_chunk_overlap = 0.8
  # set chunk size limit
  chunk_size_limit = 600

  prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

  # define LLM
  llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-002", max_tokens=num_outputs))
  
  documents = SimpleDirectoryReader(directory_path).load_data()
  
  service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
  index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
  
  index.storage_context.persist('index.json')
  
  return index

from llama_index import StorageContext, load_index_from_storage

def ask_bot(input_index='index.json'):
    # Rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="index.json")
    # Load index from the storage context
    new_index = load_index_from_storage(storage_context)

    new_query_engine = new_index.as_query_engine()

    while True:
        query = input('What do you want to ask the bot?   \n')

        if query.lower()=="by":
            break
            
        response = new_query_engine.query(query)
        if not response.response or response.response.isspace():
            print("\nBot says: \n\nSorry, I can't answer this question.\n\n\n")
        else:
            print("\nBot says: \n\n" + response.response + "\n\n\n")
        
        
        
        
index = construct_index(directory_path='C:/Users/Admin/Music/')
#index = construct_index(directory_path='C:/Users/Admin/Videos/Captures')

ask_bot('index.json')        