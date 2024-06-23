import logging
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
import openai
import chromadb.utils.embedding_functions as embedding_functions

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('custom_qa_chain')

class CustomQAChain:

    def __init__(self):

        """
        Initialising necessary variables.
        """

        self.gpt_model = 'gpt-3.5-turbo-0125'
        self.api_key = os.getenv("OPENAI_API_KEY") 
        self.ef = embedding_functions.OpenAIEmbeddingFunction(
                        api_key = self.api_key,
                        model_name="text-embedding-3-large"
                    )
        openai.api_key = self.api_key
        self.chroma_client = chromadb.Client(settings=Settings(allow_reset=True)) 

    def load_pdf(self):

        """
        Reads the contents from a pdf file and returns a list of Document objects.
        """

        try:
            pdf_path = 'downloaded_file.pdf'
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            return docs
        except Exception as e:
            logger.error(f"Failed to load PDF: {e}")
            return []
        
    def create_collection(self, docs):
        """
        Creates a collection in ChromaDB.
        """

        collection_name = 'slack_bot'
        self.chroma_client.reset()
        
        if len(docs) > 0:
        
            collection = self.chroma_client.get_or_create_collection(f"{collection_name}", metadata={"hnsw:space": "cosine"}, embedding_function= self.ef)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
            splits = text_splitter.split_documents(docs)
            
            page_content_list = []
            metadata = []
            ids = []

            logger.info(f"Splitting {len(splits)} documents")
            for i, doc in enumerate(splits):
                ids.append(str(i + 1))
                page_content_list.append(doc.page_content.replace('{', '(').replace('}', ')'))
                metadata.append(doc.metadata)

            collection.add(
                documents=page_content_list,
                metadatas=metadata,
                ids=ids
            )
            logger.info(f"Collection created for {collection_name}")

        else:

            logger.info(f"Cant Create collection for {collection_name}")

    def query_collection(self,user_questions):

        """
        Queries and retrieves the contexts from chromaDB.
        """

        contexts = []
        collection_name = 'slack_bot'
        try:
            collection = self.chroma_client.get_collection(f"{collection_name}", embedding_function= self.ef)
            for question in user_questions:
                similarity = collection.query(
                    query_texts=[question],
                    n_results=3
                )
                results = similarity['documents'][0]
                contexts.extend(results)
        except Exception as e:
            logger.error(f"Failed to query collection: {e}")
        
        return contexts
    
    def call_gpt(self, user_questions, text):
        """
        Sends the prompt to OpenAI API using the chat interface and gets the model's response.
        """
        prompt = f"""
        -- You're a helpful AI assistant. Given user questions and some contexts, generate answers.
            If none of the articles answer the question or If the answer is of low confidence, reply with “Data Not Available”.\n\n
            Check the constraints given below and answer the questions accordingly.
    
            question:
            {user_questions}

            context:
            {text}


            -- Strict Constraints:

            -- 1. Thoroughly examine the contexts provided and answer the questions.
            -- 2. STRICTLY GENERATE COMPLETE ANSWER WORD TO WORD FROM THE GIVEN CONTEXT.
            -- 3. GENERATE LONG ANSWERS IF REQUIRED.
            -- 4. The question might require to go through mutliple contexts and generate a proper answer only after going through all of them.
            -- 5. You need to generate the output in a json format. The json must be a list of dictionaries. Where each dictionary's key is the question asked and
                value should be the answer.
            -- 6. Check the output format from the example given below and strictly generate the output in that format.
            -- 7. Dont generate anything that is not in the context provided.
            
            
            **output_format example:**
                [ 
                    [ // note
                        "question": "what is the company name?",
                        "answer": "Zania, inc" 
                    ] // note,
                    [ // note
                        "question": "what is the company domain?",
                        "answer": "AI Agents" 
                    ] // note 
                ]
            STRICLTY Take the above example as reference and generate the response.
    
        """
        message = {
            'role': 'user',
            'content': prompt
        }

        response = openai.chat.completions.create(
            model=self.gpt_model,
            messages=[message]
        )

        chatbot_response = response.choices[0].message.content
        return chatbot_response
