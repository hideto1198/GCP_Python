"""
本番環境では使えません。
transactionの必要性を確認する用のコード
あまり考えられませんが、アクセス回数をカウントするとします。
threadを使用して擬似的に同時アクセスを再現しています。
通常期待される結果はthreadに関係なくカウントアップさせたいとこですが、
transactionを使用しない場合排他制御は行われません。
"""
from google.cloud import firestore
from google.oauth2.service_account import Credentials
import threading

cred = Credentials.from_service_account_file(filename='serviceAccount.json')
db = firestore.Client(credentials=cred)

""" deploy用
db = firestore.Client()
"""

def main(request):
    # ローカル用
    data = request['data']
    """ デプロイ用
    request_json = request.get_json()
    data = request_json['data']
    """  

    """ トランザクションを利用する場合はコメントアウトを外す
    transaction = db.transaction()
    @firestore.transactional
    def set_count(transaction):
        ref = db.collection('DATA').document('test_document')
        ref_data = ref.get(transaction=transaction).to_dict()
        transaction.set(ref, {'access_counts': ref_data['access_counts'] + 1}, merge=True)

    set_count(transaction=transaction)
    """


    ref = db.collection('DATA').document('test_document')

    # 現在のアクセスカウントを取得
    ref_data = ref.get().to_dict()

    ref.set({'access_counts': ref_data['access_counts'] + 1}, merge=True)
    db.close()


if __name__ == '__main__':
    request = {
        'data': {
            'key': 'value'
        }
    }

    thread1 = threading.Thread(target=lambda: main(request=request))
    thread2 = threading.Thread(target=lambda: main(request=request))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()