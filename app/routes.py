from os import abort
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    board_title=request_body["title"]
    board_owner=request_body["owner"]

    if not board_title or not board_owner:
        return make_response({"message":"Title or owner empty"}, 400)
    
    new_board = Board(title=board_title, 
                      owner=board_owner)
    
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
                "title": board.title,
                "owner": board.owner,
                "id": board.board_id
            }
        )
    return jsonify(boards_response)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id) 

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model
   
@boards_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):
    board = validate_model(Board, board_id)

    return(
        {
            "title": board.title,
            "owner": board.owner,
            "id": board.board_id
        }
    )

@boards_bp.route("/<board_id>", methods=["PUT"])
def update_one_board(board_id):
    pass

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_all_cards_for_board(board_id):
    board = validate_model(Board, board_id)

    cards_response = []
    for card in board.cards:
        cards_response.append(
            {
                "message": card.message,
                "likes_count": card.likes_count,
                "id": card.card_id
            }
        )

    return jsonify(cards_response)

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_new_card(board_id):
    request_body = request.get_json()

    card_message = str(request_body["message"])
    if not card_message or len(card_message) > 40:
        return make_response({"message":"Card message missing or empty"}, 400)
    
    board = validate_model(Board, board_id)
    new_card = Card(message=card_message)

    new_card.likes_count = 0 # Likes count always set to 0 for a new card
    new_card.board = board # Map card to board it belongs to

    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify(f"Card {new_card.message} successfully created"), 201)

@boards_bp.route("/<board_id>/cards/<card_id>", methods=["PATCH"])
def update_card_likes_count(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)

    # Ignore the request body, only thing that can be changed on card is +1 on likes count
    # Card to be updated should belong to the board passed in, raise error if not
    if card in board.cards:
        card.likes_count += 1
    else:
        make_response({"message":f"Card {card.card_id} does not belong to board {board.board_id}"}, 404)

    return make_response(jsonify(f"Card {card.message} likes count successfully updated"), 200)