from pathlib import Path

BASE_DIR = Path(__file__).parent

PATH_TO_EMBS = BASE_DIR/'embeddings.pkl'
PATH_TO_LABELS = BASE_DIR/'labels.pkl'
REDIS_HOST = 'http://localhost'
BACK_SERV = 'http://localhost:8000'
POST_TO = 'http://localhost:8000/api/records/'