# テストなどでローカルで使用する場合はこっちを使用する
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from firebase_admin import messaging
from datetime import datetime
from random import choice

# serviceAccount.jsonを同一フォルダ内に配置
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

""" Cloud Functionsにデプロイする場合はこっち
import json
import firebase_admin
from firebase_admin import messaging
from google.cloud import firestore
from datetime import datetime
from random import choice

firebase_admin.initialize_app()
db = firestore.Client()
"""

# エントリポイントをmainにする(自由)
def main(request):
    transaction = db.transaction()

    # ローカル用
    data = request['data']
    
    """ デプロイ用
    request_json = request.get_json()
    data = request_json['data']
    """
    
    @firestore.transactional
    def set_in_transaction(data):
        # 基本的な書き方
        ref = db.collection('YOUR_COLLECTION_NAME').document('YOUR_DOCUMENT_NAME')
        transaction.set(ref, {}, merge=True)
        # transaction.update(ref, {}) updateバージョン
        
        # transaction内でデータを取得し、そのデータを元に(加算、減算など)
        ref = db.collection('USER').document(f'{data["userID"]}')
        user_info = ref.get().to_dict()
        transaction.update(ref, {
            'access_count': user_info['access_count'] + 1
        })
    
    set_in_transaction(data)
    


# ローカル用　デプロイ時は削除する
if __name__ == '__main__':
    request = {
        'data': {
            'userID': '1234567890'
        }
    }
    main(request)
