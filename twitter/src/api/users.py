from flask import Blueprint, jsonify, request, abort
from ..models import Tweet, User, db
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['GET'])
def index():
    users = User.query.all() # getting all users
    result = []
    for u in users:
        result.append(u.serialize()) # build a list of users as Python dic
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id:int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())

@bp.route('', methods=['POST']) # MAYBE MAKE A TRY AND CATCH FOR EXISTING USERS
def create():
    # check if either username or password are missing
    if "username" in request.json and "password" in request.json:
        pass
    else:
        return abort(400)
    # check username and password lengths
    if len(request.json["username"]) < 3 or len(request.json["password"]) < 8:
        return abort(400)

    # construct User
    u = User(
        username=request.json["username"],
        password=scramble(request.json["password"])
    )
    db.session.add(u) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(u.serialize())

@bp.route('<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id)
    try:
        db.session.delete(u) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        return jsonify(False)

@bp.route('<int:id>', methods=['PATCH', 'PUT'])
def update(id:int): # need to comment out some parts here to make Task 6: tests 2 and 4 work
    u = User.query.get_or_404(id)
    if "username" not in request.json and "password" not in request.json:
        return abort(400)

    if 'username' in request.json:
        if len(request.json["username"]) < 3:
            return abort(400)
        u.username = request.json["username"]
    if 'password' in request.json:
        if len(request.json["password"]) < 8:
            return abort(400)
        u.password = scramble(request.json["password"])

    try:
        db.session.add(u)
        db.session.commit()
        return jsonify(u.serialize())
    except:
        return jsonify(False)

@bp.route('/<int:id>/liked_tweets', methods=['GET'])
def liked_tweets(id: int):
    u = User.query.get_or_404(id)
    result = []
    for t in u.liked_tweets:
        result.append(t.serialize())
    return jsonify(result)