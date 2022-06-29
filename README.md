# GCP_Python
pythonでCloud Functionを書く

VScodeなどのIDEでコードを書く場合は以下のインストールが必須です

``` cmd
pip install google
```

個人的にはCloud Functionsのウェブ上でコードを書くことはお勧めしません。<br>
ウェブ上ではコードチェックがされないため、インデントや、小さなミスでデプロイに失敗することがあります。<br>
また、デプロイ時間にかなり時間がかかりますので、エラーが起きてまたデプロイするのは時間がかかり過ぎますので<br>
IDEで期待した結果を取得できるか確認してからデプロイするのが良いと思います。

<br>

- delete.py ・・・フィールド、ドキュメント、コレクションの削除サンプル
- transaction.py ・・・update,setでtransactionを利用するサンプル
