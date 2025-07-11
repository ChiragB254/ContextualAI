from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

class Embeddings:
	@classmethod
	def azure_openai(cls):
		"""Initialize Azure OpenAI Embeddings."""
		return AzureOpenAIEmbeddings(
			azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
			azure_deployment=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
			openai_api_version=os.environ["AZURE_OPENAI_EMBEDDING_API_VERSION"],
			model="text-embedding-3-small"
		)
	@classmethod
	def huggingface(cls, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):

		# 🔧 Specify the Hugging Face embedding model to use
		model_name = embedding_model

		# ⚙️ Model-specific arguments (e.g., run on CPU)
		model_kwargs = {'device': 'cpu'}

		# 🧮 Embedding behavior settings
		# normalize_embeddings=False ensures raw embeddings are used (not L2-normalized)
		encode_kwargs = {'normalize_embeddings': False}

		# 🤗 Initialize the HuggingFaceEmbeddings class with specified settings
		hf = HuggingFaceEmbeddings(
		model_name=model_name,
		model_kwargs=model_kwargs,
		encode_kwargs=encode_kwargs
		)

		return hf