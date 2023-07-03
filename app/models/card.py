from app import db
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    board = db.relationship("Board", back_populates="cards")    