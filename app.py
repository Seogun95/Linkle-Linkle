from pymongo import MongoClient

client = MongoClient("mongodb+srv://sparta:1234@cluster0.txh1xie.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta

#Flask 기본 코드
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/post')
def home_post():
   return render_template('home-posts.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
