import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "prod")
DATABASE_URL = os.getenv("DATABASE_URL", "")
