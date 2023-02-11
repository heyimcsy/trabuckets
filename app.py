from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.dcruhdw.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.test


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/signup", methods=["POST"])
def sign_up():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    gender_receive = request.form['gender_give']
    pnum_receive = request.form['pnum_give']
    birth_receive = request.form['birth_give']
    postal_recieve = request.form['postal_give']
    address_receive = request.form['addr_give']
    address2_receive = request.form['addr2_give']

    doc = {
        'id': id_receive,
        'password': password_receive,
        'name': name_receive,
        'email': email_receive,
        'gender': gender_receive,
        'pnum': pnum_receive,
        'birth': birth_receive,
        'postal': postal_recieve,
        'address': address_receive,
        'address2': address2_receive
    }
    print(doc)
    print(id())
    print(id_receive)
    db.test.insert_one(doc)

    return jsonify({'msg': '회원가입 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
