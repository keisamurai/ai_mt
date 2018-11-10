#////////////////////////////////////////////////////////////////////
#// name:TestSentimentData.py
#// description: Watson Discoveryから特定のワード対する極性
#//  (positive/neutoral/negative)を集計してデータ出力する
#////////////////////////////////////////////////////////////////////
import os
import datetime
import pandas as pd
import requests
import json

# 個別モジュール
import DateCulc

def AggregateSentimentData(NLQ, SSD, SED, USERNAME, PASS):
    """
    description: watsonにSentimentデータをクエリする
    args: 
        NLQ:Natural_Language_Query:検索キーワード
        SSD:Search_Start_Date:検索開始日 (YYYYMMDD)
        SED:Search_End_Date:検索終了日  (YYYYMMDD)
        USERNAME: discoveryに照会をかけるためのユーザーID 
        PASS:discoveryに照会をかけるためのパスワード
    """
    # 変数設定
    VERSION='2018-08-01'                            # discovery API version
    SEARCH_START_DATE=DateCulc.DateUTime(SSD)       # date for query
    SEARCH_END_DATE=DateCulc.DateUTime(SED)         # date for query
    QUERY_NLQ=NLQ                                   # Query word for Natural Language Query
    USERNAME='a0766d60-1d62-4cbc-abb9-1542a790bdca' # auth username
    PASS='Sfi1P1AhZFGk'                             # auth password
    URL_NEWS='https://gateway.watsonplatform.net/discovery/api/v1/environments/system/collections/news-en/query'
    
    # curl用パラメータセット
    params = (
        ('version', VERSION),
        ('filter', 'crawl_date>{0}T00:00:00+0900,crawl_date<{1}T23:59:59+0900'.format(SEARCH_START_DATE, SEARCH_END_DATE)),
        ('aggregation', 'term(host).term(enriched_text.sentiment.document.label)'),
        ('natural_language_query', QUERY_NLQ),
    )
    # curl実行
    response = requests.get(
        url=URL_NEWS,
        params=params, 
        auth=(USERNAME, PASS)
    )
    # エラーチェック
    if response.status_code != 200:
        print('[:ERROR:]response error : {0}'.format(response.status_code))
    # APIからのリターンをjson_dataに格納 
    json_data = response.json()

    NumberOfPositive = 0
    NumberOfNeutral = 0
    NumberOfNegative = 0

    # positive/neutral/negativeを集計
    for tmp in json_data['aggregations'][0]['results']:
        for result in tmp['aggregations'][0]['results']:
            if result['key'] == 'positive':
                NumberOfPositive += result['matching_results']
            if result['key'] == 'neutral':
                NumberOfNeutral += result['matching_results']
            if result['key'] == 'negative':
                NumberOfNegative += result['matching_results']
    return NumberOfPositive, NumberOfNeutral, NumberOfNegative

# main process
# 例としてdai-ichi-lifeを照会している
if __name__ == '__main__':
    NLQ='dai-ichi-life'
    SSD='20180920'
    SED='20180921'
    USERNAME=[Username] # auth username
    PASS=[Password]                             # auth password
    OUTPUTFILE='TestSentimentData.csv'
    # 処理用定義
    POSITIVE=0
    NEUTRAL=1
    NEGATIVE=2

    print("------Process Start------")

    # DateDiffから日数差を取得
    Duration = DateCulc.DateDiff(SSD, SED)
    # 日付ループ
    for i in range(Duration + 1):
        # 照会する日付取得
        QueryDay = DateCulc.DateAdd(SSD, i)  
        # 0埋めした日付文字列を生成
        QueryDay = str(QueryDay.year) + '{:02}'.format(QueryDay.month) + '{:02}'.format(QueryDay.day)
        # SentimentData取得
        sentiments = AggregateSentimentData(NLQ, QueryDay, QueryDay, USERNAME, PASS)
        # for debug
        print('NumberOfPositive:{}'.format(sentiments[POSITIVE]))
        print('NumberOfNeutral:{}'.format(sentiments[NEUTRAL]))
        print('NumberOfNegative:{}'.format(sentiments[NEGATIVE]))

        # DataFrameを生成
        df = pd.DataFrame(
            [[NLQ, QueryDay, sentiments[POSITIVE], sentiments[NEUTRAL], sentiments[NEGATIVE]]],
            columns=['Company Name', 'Date', 'Positive', 'Neutral', 'Negative']
            ) 
        
        # 初回はヘッダー含めて新規作成、2回目以降はヘッダー不要で追記
        if i == 0:
            df.to_csv(
                OUTPUTFILE,
                index=False,
            )
        else:
            # csvに追記
            df.to_csv(
                OUTPUTFILE,
                index=False,
                mode='a',
                header=False
            ) 
    
    print("------Process End------")
