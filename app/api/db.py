from sqlalchemy import create_engine
from sqlalchemy import Text, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
import os
from dotenv import load_dotenv
from databases import Database
from datetime import datetime
import asyncio


load_dotenv()

DB_URL = os.getenv('URL')
PORT = os.getenv('PORT')
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass

class Secrets(Base):
    __tablename__ = 'secrets'

    refresh_token: Mapped[Text] = mapped_column(Text, primary_key=True)
    access_token: Mapped[Text] = mapped_column(Text)
    creation_time: Mapped[datetime.timestamp] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now)

#create the engine
engine = create_engine(url=url)
#create tables if they don't already exist
db = Database(url)

if __name__ == '__main__':
    Base.metadata.create_all(engine)

