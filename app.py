# 대욱 app.py
import hashlib
import datetime
import jwt
import certifi
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)


ca = certifi.where()


# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;


client = MongoClient('mongodb+srv://sparta:1234@cluster0.txh1xie.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)

db = client.linkle
app = Flask(__name__)


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', user_id=user_info["id"])
    except jwt.ExpiredSignatureError:
        # return jsonify({'msg': '로그인 시간이 만료되었습니다.'})
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        # return jsonify({'msg': '로그인 정보가 존재하지 않습니다.'})
        return render_template('index.html')

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/category')
def category():
    return render_template('home-category.html')

@app.route('/post')
def posts():
    return render_template('home-posts.html')


@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_name']
    pw_receive = request.form['passwd_one']

    user = db.user.find_one({'id': id_receive})
    if user is None:
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
        db.user.insert_one({'id': id_receive, 'pw': pw_hash})
        return jsonify({'result': 'success'})
    else:
        return jsonify({'msg': '이미 존재하는 아이디 입니다.'})


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=18000)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'id': userinfo['id']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
        

@app.route('/api/category', methods=['POST'])
def category_register():
    token_receive = request.cookies.get('mytoken')
    try:
        category_receive = request.form['category_name']
        img_receive = request.form['category_img_url']

        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        category_list = list(db.category.find({}, {'_id': False}))
        category = db.category.find_one({'name': category_receive})
        if category is None:
            count = len(category_list) + 1

            doc = {
                'id': count,
                'author': userinfo['id'],
                'img' : img_receive,
                'name': category_receive,
                'status': 0
            }
            db.category.insert_one(doc)

            return jsonify({'result': 'success'})
        else:
            return jsonify({'result': 'fail', 'msg': '해당 이름의 카테고리가 이미 존재합니다.'})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route('/api/comment', methods=['POST'])
def comment_register():
    token_receive = request.cookies.get('mytoken')
    try:
        post_id = request.form['post_id']
        comment_receive = request.form['comment']


        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        category_list = list(db.category.find({}, {'_id': False}))
        count = len(category_list) + 1

        doc = {
            'id': count,
            'post_id': post_id,
            'author': userinfo['id'],
            'comment': comment_receive,
            'reg_dt': datetime.now()
        }
        db.comment.insert_one(doc)

        return jsonify({'result': 'success'})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route('/api/like', methods=['POST'])
def like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        post_id = request.form['post_id']
        category_id = request.form['category_id']

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        doc = {
            'post_id': post_id,
            'category_id': category_id,
            'author': userinfo['id'],
        }
        like = db.like.find_one(doc)
        if like is None:
            db.like.insert_one(doc)
        else:
            db.like.delete_one(doc)

        return jsonify({'result': 'success'})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route('/api/categories', methods=['GET'])
def category_list():
    category_list = list(db.category.find({}, {'_id': False}))

    return jsonify({'categories': category_list})


@app.route('/api/posting', methods=['POST'])
def post_register():
    token_receive = request.cookies.get('mytoken')

    try:
        title_receive = request.form['post_title']
        desc_receive = request.form['post_desc']
        url_receive = request.form['post_url']
        category_receive = request.form['post_category']

        url = url_receive

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url, headers=headers)

        soup = BeautifulSoup(data.text, 'html.parser')

        # title = soup.select_one('meta[property="og:title"]')['content']
        image = soup.select_one('meta[property="og:image"]')['content']
        # desc = soup.select_one('meta[property="og:description"]')['content']
  
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        post_list = list(db.post.find({}, {'_id': False}))
        count = len(post_list) + 1

        doc = {
            'id': count,
            'author': userinfo['id'],
            'title': title_receive,
            'desc': desc_receive,
            'image': image,
            'category': int(category_receive),
            'reg_dt': 'dkei',
            'link_url': url,
            'status': 0

        }
        db.post.insert_one(doc)

        return jsonify({'result': 'success'})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route("/api/posts", methods=["GET"])
def post_list():
    category_id = int(request.args.get('category_id'))
    posts_list = list(db.post.find({'category': category_id}, {'_id': False}))
    like_list = list(db.like.find({}, {'_id': False}))
    for i in range(0, len(posts_list)):
        like_total = list()
        for j in range(0, len(like_list)):
            if(posts_list[i]['id'] == like_list[j]['post_id']):
                 like_total.append(like_list[j])
        posts_list[i]['likes'] = like_total


    return jsonify({'posts': posts_list, 'like_list' : like_list})

@app.route("/api/post", methods=["GET"])
def get_post():
    post_id = int(request.args.get('post_id'))
    post = db.users.find_one({'id': post_id})
    like_list = list(db.like.find({'post_id': post_id}, {'_id': False}))
    comment_list = list(db.comment.find({'post_id': post_id}, {'_id': False}))

    return jsonify({'post': post, 'comments': comment_list, 'likes' : like_list})


@app.route("/api/remove", methods=["POST"])
def remove_post():
    remove_id = request.form['remove_id']
    db.post.delete_one({'id':int(remove_id)})
    return jsonify({'remove':'성공적으로 삭제하였습니다.'})


@app.route("/api/cateRemove", methods=["POST"])
def remove_cate():
    remove_id = request.form['remove_id']
    posts_list = list(db.post.find({'category':int(remove_id)}, {'_id': False}))
    if len(posts_list) > 0:
        return jsonify({'remove':'안에 내용을 지워주세요.'})
    else:
        db.category.delete_one({'id':int(remove_id)})
        return jsonify({'remove':'삭제 성공했습니다.'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)