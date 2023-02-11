from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.wlcw8cv.mongodb.net/luster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.trabucket

import requests as requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://travel.naver.com/domestic', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trabuckets = soup.select('#DomesticHome > div.season_Seasonals__3IGq4 > ul > li')
for trabucket in trabuckets:
    code = trabucket.select_one('div > a > div.item_head__eQx5Y > b').text
    title = trabucket.select_one('div > a > div.item_head__eQx5Y > span').text
    sub_title = trabucket.select_one('div > a > div.item_head__eQx5Y > i').text
    desc = trabucket.select_one('div > a > div.item_description__1ENSh').text
    tag = trabucket.select_one('div > a > div.item_keywords__ZF5rC').text
    image = trabucket.select_one('div > div.item_images__3k522 > a')

    doc = {
        'code': code,
        'title': title,
        'sub_title': sub_title,
        'desc': desc,
        'tag': tag,
        'image': image,
    }
    print(doc)
    # db.travel.delete_one(doc)
    # db.travel.insert_one(doc)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/sub')
def sub():
    return render_template('sub.html')

#각 상세페이지들 만들기
@app.route('/sub/<code>')
def view(code):
    return render_template('sub.html')

# @app.route("/bucket", methods=["POST"])
# def bucket_post():
#     bucket_receive = request.form['bucket_give']
#     code_receive = request.form['code_give']
#     # bucket_list = list(db.bucket.find({},{'_id': False}))
#     # count = len(bucket_list) + 1
#     idnum = db.bucket.find_one(sort=[('num',-1)])['num']+1
#     if idnum == 0 :
#         doc = {
#             'code': code_receive,
#             'num': 1,
#             'bucket': bucket_receive,
#             'done': 0
#         }
#     else:
#         doc = {
#                 'code': code_receive,
#                 'num': idnum,
#                 'bucket': bucket_receive,
#                 'done': 0
#             }
#     db.bucket.insert_one(doc)
#     return jsonify({'msg': '등록 완료'})

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    code_receive = request.form['code_give']
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    if len(bucket_list) == 0:
        count = 1
        doc = {
            'code': code_receive,
            'num': count,
            'bucket': bucket_receive,
            'done': 0
        }
        db.bucket.insert_one(doc)
        return jsonify({'msg': '등록 완료'})
    else:
        count = db.bucket.find_one(sort=[("num", -1)])["num"] + 1
        doc = {
            'code': code_receive,
            'num': count,
            'bucket': bucket_receive,
            'done': 0
        }
        db.bucket.insert_one(doc)
        return jsonify({'msg': '등록 완료'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})

#버킷 완료했을 때
@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}}) #변수로 가져온 숫자는 int()로 숫자로 바꿔줘야함
    return jsonify({'msg': '버킷 완료'})

#버킷 완료를 취소
@app.route("/bucket/cancle", methods=["POST"])
def bucket_cancle():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}}) #변수로 가져온 숫자는 int()로 숫자로 바꿔줘야함
    return jsonify({'msg': '버킷 취소'})

#버킷을 삭제
@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form['num_give']
    db.bucket.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료'})

#여행장소 인포주기
@app.route("/info", methods=["GET"])
def info_get():
    info_list = list(db.travel.find({}, {'_id': False}))
    return jsonify({'info_list': info_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=False)