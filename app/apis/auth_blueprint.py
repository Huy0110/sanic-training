import uuid

from sanic import Blueprint
from sanic.response import json

from app.databases.mongodb import MongoDB
from app.hooks.error import ApiInternalError
from app.utils.jwt_utils import generate_jwt
from app.models.user import User

auth_bp = Blueprint('auth_blueprint', url_prefix='/auth')

_db = MongoDB()


@auth_bp.route('/register', methods=['POST'])
async def register(request):
    user_data = request.json
    print("user data: ", user_data)

    if _db.get_user_by_username(user_data['username']):
        raise ApiInternalError('Username already exists')
    
    user_id = str(uuid.uuid4())
    user = User(user_id).from_dict(user_data)
    # user.password = pbkdf2_sha256.hash(user.password)

    # Insert user to database
    inserted = _db.add_user(user)
    if not inserted:
        raise ApiInternalError('Fail to create user')

    # Create JWT token
    token = generate_jwt(username=user.username)

    return json({'status': 'success', 'token': token})

@auth_bp.route('/login', methods=['POST'])
async def login(request):
    login_data = request.json

    user = _db.get_user_by_username(login_data['username'])
    # if not user or not pbkdf2_sha256.verify(login_data['password'], user.password):
    if not user or (login_data['password'] != user.password):
        raise ApiInternalError('Invalid email or password')

    # Create JWT token
    token = generate_jwt(username=user.username)

    return json({'status': 'success', 'token': token})