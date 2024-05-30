from dotenv import load_dotenv
from llama_index.core.settings import Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini

load_dotenv()

GEMINI_LLM = Gemini(model_name="models/gemini-pro", temperature=0.0)
GEMINI_EMBED = GeminiEmbedding()

Settings.embed_model = GEMINI_EMBED

LOG_FILE: str = "session_data/user_actions.log"
SESSION_FILE: str = "session_data/user_session_state.yaml"
CACHE_FILE: str = "cache/pipeline_cache.json"
CONVERSATION_FILE: str = "cache/chat_history.json"
QUIZ_FILE: str = "cache/quiz.csv"
SLIDES_FILE: str = "cache/slides.json"
STORAGE_PATH: str = "ingestion_storage"
INDEX_STORAGE: str = "index_storage"

QUIZ_SIZE: int = 5
ITEMS_ON_SLIDE: int = 4
