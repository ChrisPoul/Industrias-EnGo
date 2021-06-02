from EnGo.models import db, MyModel
from sqlalchemy import (
    Column, Integer, String, Text
)


class Post(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)

    def get(id):
        return Post.query.get(id)
    
    def get_all():
        return Post.query.all()

    def search(search_term):
        return Post.query.filter_by(title=search_term).first()