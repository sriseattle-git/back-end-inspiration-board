from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    title=request_body["title"]
    owner=request_body["owner"]

    if not title or not owner:
        return make_response({"message":"Title or owner empty"}, 400)
    
    new_board = Board(title=request_body["title"], 
                      owner=request_body["owner"])
    
    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(f"Board {new_board.title} successfully created"), 201)

@boards_bp.route("", methods=["GET"])
def list_all_boards():
    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(
            {
                "title":board.title,
                "owner": board.owner
            }
        )
    return jsonify(boards_response)

@boards_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):
    pass

@boards_bp.route("/<board_id>", methods=["PUT"])
def update_one_board(board_id):
    pass

@boards_bp.route("<board_id>/cards", methods=["GET"])
def read_all_cards_for_board(board_id):
    pass

@boards_bp.route("<board_id>/cards/<card_id>", methods=["PATCH"])
def update_card(board_id, card_id):
    pass
