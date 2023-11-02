import os

from flask import Flask, render_template, request
from google.cloud import bigquery

from google.cloud import bigquery
from google.oauth2 import service_account


#key_path = "..\\ssh\\credencial-key.json"
#credentials = service_account.Credentials.from_service_account_file(
#    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
#)
#bigquery_client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

bigquery_client = bigquery.Client()
app = Flask(__name__)

# リクエストを受け付ける関数
@app.route('/', methods=['GET'])
def diplay():

    #BigQueryにクエリを投げる
    query_job = bigquery_client.query(
        """
        SELECT
            *
        FROM 
            `your-database-name`
        ORDER BY 
            day
        """
    )

    # クエリの実行結果をデータフレームに取得する
    df = query_job.to_dataframe()
    
    #print(type(df))
    # print(df.fillna(0))
    # df = df.fillna(0)
    
    labels = df["day"]
    datas = [df["Goods_and_services"], df["Goods_total"], df["Exports"], df["Imports"], df["Services"]]
    
    return render_template('chart.html', datas=datas, labels=labels)


if __name__ == '__main__':
    #ローカル実行時はCloud Shell推奨の8080ポートを使用する
    app.run(host='0.0.0.0', port=8080)
