from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import *
from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:1234@cluster0.txh1xie.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = '1234',
)


jwt = JWTManager(app)

@app.route('/test')
def home():
    return render_template('test.html')


@app.route("/login", methods=["GET"])
def login():
    user_id = 'test_id'
    user_pw = '1234'

    if user_id == 'test_id' and user_pw == '1234':
        result = 'success'
        access_token = create_access_token(identity = user_id, expires_delta = False)
        return jsonify(result, access_token)
    else:
        return jsonify(result = 'invalid params')

@app.route("/post", methods=["GET"])
@jwt_required()
def user_only():
    # request.headers.set("Authorization", 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3Mzg1MDY2NSwianRpIjoiZThmOTcyOGQtMTNmOC00YWIyLWE3ZWQtMTU0NjU3YmIyZjViIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3RfaWQiLCJuYmYiOjE2NzM4NTA2NjV9.HSpctsP3FKL9QjIa2PfeIH9gMPvOAl0YVMXkGsk_cZs')
    # print(request.get_data())
    cur_user = get_jwt_identity()

    if cur_user is None:
        return "User Only!"
    else:
        return "Hi" + cur_user




@app.route("/homework", methods=["GET"])
def homework_get():
    comment_list = list(db.comments.find({}, {'_id': False}))

    return jsonify({'comments': comment_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
