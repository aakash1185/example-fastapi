from pydantic import BaseSettings
from dotenv import load_dotenv


load_dotenv('app/.env')
class Settings(BaseSettings):
    # database_hostname : str
    # database_name : str
    # database_username : str
    # database_port: str
    # database_password : str
    # secret_key : str
    # algorithm: str
    # access_token_expire_minutes: int

    #============================Testing============================
    database_hostname ='localhost'
    database_name ='fastapi'
    database_username ='postgres'
    database_port=5432
    database_password ='root'
    secret_key ='l2h454g4lh42og443hp25i35hp63423pi5634h7i12pi1293810rgf78e6rf8'
    algorithm='HS256'
    access_token_expire_minutes=30
    #============================Testing============================

    class Config:
        env_file='.env'

settings = Settings()