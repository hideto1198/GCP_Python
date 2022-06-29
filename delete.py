# データ、ドキュメントを削除する

import json
from google.cloud import firestore
from google.oauth2.service_account import Credentials
from datetime import datetime

cred = Credentials.from_service_account_file(filename='serviceAccount.json')
db = firestore.Client(credentials=cred)

""" deploy用
db = firestore.Client()
"""

# エントリポイントをmainにする(自由)
def main(request):

    # ローカル用
    data = request['data']
    
    """ デプロイ用
    request_json = request.get_json()
    data = request_json['data']
    """

    user_ref = db.collection('USERS').document(data['userID'])

    # フィールドを削除する場合
    user_ref.set({'favorite': firestore.DELETE_FIELD}, merge=True)
    # or
    user_ref.update({'favorite': firestore.DELETE_FIELD})

    # ドキュメントを削除する場合
    user_ref.collection('datas').document('books').delete()
    
    # コレクションを削除する
    # 仕様上、コレクションを削除するにはコレクションの配下にある全てのデータを取得する必要がある。
    datas = user_ref.collection('datas').get()
    for data in datas:
        data.reference.delete()
    


# ローカル用　デプロイ時は削除する
if __name__ == '__main__':
    request = {
        'data': {
            'userID': '12345'
        }
    }
    main(request)
