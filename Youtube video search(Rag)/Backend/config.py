import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://search:Padhai_123@35.222.253.146:5432/VideoSearchDB?sslmode=disable")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
