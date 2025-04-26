import os
from dotenv import load_dotenv

load_dotenv()

SAS_API_KEY = os.getenv('SAS_API_KEY', 'isb13')
SAS_API_URL = 'https://www.simonandschuster.com/ws/authors/1666839' 