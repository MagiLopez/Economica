import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'finly_secret_key_2024'
