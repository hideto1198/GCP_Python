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
