#!/bin/bash
#////////////////////////////////////////////////////////////////////
#// name:MakeSentimentData.sh
#// description: Watson Discoveryから特定のワード対する極性
#//  (positive/neutoral/negative)を集計してデータ出力する
#// input: 
#//   1 --> NLQ: Natural_Language_Query:検索対象キーワード
#//   2 --> SSD: Search_Start_Date:検索開始日
#//   3 --> SED: Search_End_Date:検索終了日
#// output: 以下のフォーマットのcsv形式で検索結果を出力する。
#//   NLQ,SSD,SED,positive数,neutoral数,negative数
#// return:
#//   0 --> 正常終了
#//   1 --> 以上終了
#////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////
#//name: Query_SentimentData
#//description:　日付とキーワードで極性情報のデータをdiscoveryから取得する
#//input:
#// 1 --> NLQ
#// 2 --> SSD
#// 3 --> SED
#// 4 --> OUTPUTFILE
#////////////////////////////////////////////////////////////////////
function Query_SentimentData () {
# import access info
#. ../../na/.accessinfo

    NLQ=$1
    DAY=$2
    OUTPUTFILE=$3
    NPOS="" # positive数
    NNTR="" # neutoral数
    NNEG="" # negative数
    INTERFILE=Intermidiate.json
    USER_NAME=[USER NAME]
    PASS=[PASS]
    QUERY_VERSION="2018-08-01"

    
    # main command
    WATSON_URL="https://gateway.watsonplatform.net/discovery/api/v1/environments/system/collections/news-en/"
    VERSION_MAIN="query?version=$QUERY_VERSION"
    FILTER_DATE="&filter=crawl_date%3E${DAY}T00%3A00%3A00%2B0900%2Ccrawl_date%3C${DAY}T23%3A59%3A59%2B0900"
    AGGREGATION="&aggregation=term(host).term(enriched_text.sentiment.document.label)"
    QUERY_NLQ="&natural_language_query=dai-ichi-life"
    QUERY_URL=$WATSON_URL$VERSION_MAIN$FILTER_DATE$AGGREGATION$QUERY_NLQ
    echo $QUERY_URL >> $LOGFILE

    # execute main command
    curl -u $USER_NAME:$PASS $QUERY_URL -o $INTERFILE

    # check file existance of INTERFILE
    if [ -e $INTERFILE ] ; then
        echo [:INFO:] Complete Intermidiate file >> $LOGFILE
    else
        echo [:ERROR:] NO Intermidiate file >> $LOGFILE
    fi

    NPOS=`cat $INTERFILE | /usr/local/bin/jq -r '[.aggregations[].results[].aggregations[].results[] | select(.key == "positive") |.matching_results] | add'` 
    NNTR=`cat $INTERFILE | /usr/local/bin/jq -r '[.aggregations[].results[].aggregations[].results[] | select(.key == "neutral") |.matching_results] | add'`
    NNEG=`cat $INTERFILE | /usr/local/bin/jq -r '[.aggregations[].results[].aggregations[].results[] | select(.key == "negative") |.matching_results] | add'`

    # make output
    echo $NLQ,$DAY,$NPOS,$NNTR,$NNEG >> $OUTPUTFILE 
    echo 1
}

#////////////////
#// Main
#////////////////
NLQ=$1
SSD=$2
SED=$3
OUTPUTFILE=MakeSentimentData_$(date '+%Y%m%d%H%M%S').csv
LOGFILE=MakeSentimentData.log

echo ----------Process Start \($(date '+%Y/%m/%d %T')\)------------- >> $LOGFILE
# input check
if [ -z "$1" ] ; then
    echo Natural_Language_Queryのinputを入力してください:
    read NLQ
    if [ -z "$NLQ" ] ; then
        echo Natural_Language_Queryが入力されませんでした
        exit 1
    fi
fi

if [ -z "$2" ] ; then
    echo Search_Start_Dateのinputを入力してください:
    read SSD 
    # input check in detail
fi

if [ -z "$3" ]; then
    echo Search_End_Dateのinputを入力してください:
    read SED
    # input check in detail
fi

echo Netural_Language_Query:$NLQ >> $LOGFILE
echo Search_Start_Date:$SSD >> $LOGFILE
echo Search_End_Date:$SED >> $LOGFILE
echo OutPutFile:$OUTPUTFILE >> $LOGFILE

# DateDiffから日数差を取得
DIFFDAYS=`./DateDiff.sh $SSD $SED`
# DIFFDAYS+1分ループさせる
LOOP=`expr $DIFFDAYS + 1`

for ((i=0; i < $LOOP; i++)); do
    # 照会をかける対象日付を計算　yyyy-mm-ddフォーマット
    DAY=`date -d "$SSD $i days" "+%Y-%m-%d"`
    # Query_SentimentDataを使って照会
    Query_SentimentData $NLQ $DAY $OUTPUTFILE 
    echo $i
done
echo ----------Process End \($(date '+%Y/%m/%d %T')\)------------- >> $LOGFILE