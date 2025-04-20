from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFacePipeline
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login
from dotenv import load_dotenv
import os

load_dotenv()


class LLMCall:

	@classmethod
	def azure_openai(cls, temperature: float = 0.4):
		"""Initialize Azure OpenAI LLM."""
		return AzureChatOpenAI(
			azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
			azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
			openai_api_version=os.environ["AZURE_OPENAI_CHAT_API_VERSION"],
			temperature=temperature,
		)
	

	@classmethod
	def huggingface(cls, model_name: str = "google/gemma-2b-it", temperature: float = 0.5):
		
		# Authenticate with Hugging Face Hub
		login(os.getenv("HUGGINGFACE_TOKEN"))

		"""Initialize Hugging Face LLM."""

		# 🧠 Model ID from Hugging Face Hub (you can replace this with any causal LLM)
		model_id = model_name

		# 🗝️ Load the tokenizer for the chosen model (handles input formatting and tokenization)
		tokenizer = AutoTokenizer.from_pretrained(model_id)

		# 🧱 Load the actual causal language model (Gemma-2B-IT in this case)
		model = AutoModelForCausalLM.from_pretrained(model_id)

		# 🛠️ Create a pipeline for text generation using the model and tokenizer
		pipe = pipeline(
			"text-generation",        # task type
			model=model,              # pre-trained model
			tokenizer=tokenizer,      # matching tokenizer
			max_new_tokens=512,       # output token limit
			do_sample=True,           # enables sampling (vs deterministic greedy decoding)
			temperature=temperature,          # sampling randomness (lower = more focused)
			top_p=0.95,               # nucleus sampling cutoff
			repetition_penalty=1.1,   # discourages repeating phrases
			trust_remote_code=True
			)
		return HuggingFacePipeline(pipeline=pipe)

	@classmethod
	def chat_groq(cls, model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.5):
		"""Initialize Groq LLM."""
		return ChatGroq(
			model_name=model_name, 
			temperature=temperature,
			)
	@classmethod
	def chat_ollama(cls, model_name: str = "llama3.2", temperature: float = 0.5):
		"""Initialize Ollama LLM."""
		return ChatOllama(
			model=model_name,
			temperature=temperature,
			)
