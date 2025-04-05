import os

class Config:
    DEBUG = True
    PORT = 5000
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/rpm')