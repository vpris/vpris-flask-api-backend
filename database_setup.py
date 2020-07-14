# for creating the mapper code
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
# for configuration
from sqlalchemy import create_engine
# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables

Base = declarative_base()

class Article(Base):

    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    intro = Column(String(300), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'intro': self.intro,
            'text': self.text,
            'date': self.date,
        }


# creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///blog.db')
Base.metadata.create_all(engine)