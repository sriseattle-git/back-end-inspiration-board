from app import db
from sqlalchemy import Column, ForeignKey, Integer, Table

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
