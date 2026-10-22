import os
import dotenv

dotenv.load_dotenv()

DEBUG = True
App_NAME = "PassGen"
Version = "1.0.0"

#Banco
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")