#////////////////////////////////////////
#// name: DateCulc.py
#// description: 日付計算用
#////////////////////////////////////////
import datetime

NUM_DAY = 3     # 受け取る引数の数
NUM_DAY_LEN = 8  # 引数の文字列

def DateDiff(StartDay, EndDay):
    """
    description: 二つの引数を受け取り、日付の差分を返す
    """
    # args check
    if len(StartDay) != NUM_DAY_LEN or len(EndDay) != NUM_DAY_LEN:
        print('[:ERROE:]引数はYYYYMMDDの形式にしてください')

    # main process
    Start = datetime.datetime.strptime(StartDay, '%Y%m%d')
    End = datetime.datetime.strptime(EndDay, '%Y%m%d')
    if (End - Start).days < 0:
        print('[ERROR]args[0] < StartDay となるように入力してください')

    return  (End - Start).days 

def DateAdd(StartDay, AddDay):
    """
    description:日付と何日加えるかを引数として受け取り、結果を返す
    args: 
        StartDay: 開始日 (YYYYMMDD形式の文字列)
        AddDay: 加算する日数 (数値)
    return:
        加算した後の日付 (datetime型)
    """
    if len(StartDay) != NUM_DAY_LEN:
        print('[:ERROR:] Your input:={0} but must be YYYYYMMDD format'.format(StartDay))
    
    # get datetime from StartDay(str)
    Start = datetime.datetime.strptime(StartDay, '%Y%m%d')
    result = Start + datetime.timedelta(days=AddDay)
    return result

def DateUTime(Date):
    """
    description: 日付(YYYYMMDD 文字列)を受け取り、Unix用の形式(YYYY-MM-DD)に変換する    
    """
    # chech numver of char
    if len(Date) != NUM_DAY_LEN:
        print('[:ERROR:] Wrong Number Of Char:{}'.format(len(Date)))

    return Date[0:4] + '-' + Date[4:6] + '-' + Date[6:8] 

# for test
if __name__ == "__main__":
    a = DateDiff('20181110', '20181120')
    print('DateDiff:{0}'.format(a))
    b = DateAdd('20181110', 1)
    print('DateAdd:{0}'.format(b))
    c = DateUTime('20181110')
    print('DateUTime:{0}'.format(c))