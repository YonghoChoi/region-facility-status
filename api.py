import json

import requests
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.yummy_restaurant


@app.route('/api/list', methods=['GET'])
def facilities():
    datas = list(db.facility.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'datas': datas})


@app.route('/api/init', methods=['POST'])
def init():
    params = {
        'key': 'cb8afdf02e874e858b1ad9ff6be5cf93',
        'Type': 'json'
    }

    res = requests.get('https://openapi.gg.go.kr/RegionMnyFacltStus', params)
    if res.status_code != 200:
        return jsonify({'result': 'error', 'msg': f"error : status code is {res.status_code}"})

    res_json = res.json()
    if "RegionMnyFacltStus" not in res_json:
        return jsonify({'result': 'error', 'msg': f"error : invalid api result"})

    if len(res_json['RegionMnyFacltStus']) == 0:
        return jsonify({'result': 'error', 'msg': f"error : not exist api data"})

    statuses = []
    for d in res_json['RegionMnyFacltStus']:
        if "row" not in d:
            continue

        statuses.extend(d['row'])

    db.facility.insert_many(statuses)
    return json.dumps({'result': 'success', 'msg': f'{len(statuses)}개의 지역 화폐 정보를 갱신하였습니다.'})


@app.route('/api/delete', methods=['POST'])
def delete():
    db.facility.drop()
    return jsonify({'result': 'success', 'msg': '삭제 되었습니다!'})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
