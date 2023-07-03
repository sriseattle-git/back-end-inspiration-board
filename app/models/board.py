from app import db
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")
