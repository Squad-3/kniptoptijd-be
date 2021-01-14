# settings.py
from dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# settings.py
import os
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD') 
db_host = os.getenv('DB_HOST')