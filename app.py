from flask import Flask, render_template, request, jsonify
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():

    # mengambil data dari database dengan koleksi diary
    # tanpa menunjukan id dan ditampung pada variabel articles
     articles = list(db.diary.find({}, {'_id': False}))
     return jsonify({
        'articles' : articles
     })

# menyimpan data judul dan deskripsi dalam database sparta
# dengan menerima data dari client(posting)
@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    # validasi server jika judul dan konten
    # tidak boleh kosong
    if not title_receive or not content_receive:
        return jsonify({
            'msg-error': 'Judul dan Konten tidak boleh kosong.'
        })

    today = datetime.now()  
    mytime = today.strftime('tanggal_%y-%m-%d_jam_%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename  = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    profile_extension = profile.filename.split('.')[-1]
    profileName  = f'static/profile-{mytime}.{profile_extension}'
    profile.save(profileName)

    # input data title dan content dll ke database mongodb
    time = today.strftime('%Y.%m.%d')
     
    doc = {
        'gambar' : filename,
        'profil': profileName,
        'judul' : title_receive,
        'konten' : content_receive,
        'tanggal' : time
    }
    db.diary.insert_one(doc)
    return jsonify({
        'msg' : 'data saved successfully ^_^'
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)