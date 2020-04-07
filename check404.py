# coding:UTF-8
import time
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

check_url = []
alert_url = []
low_risk_url = []
again_low_risk_url = []

myfile = open("sample.txt")
data = myfile.readlines()
myfile.close()


try:
    for rstrip_url in data:
        i_url = rstrip_url.rstrip()
        check_url.append('http://' + i_url)

except Exception as e:
    print('http://の置き換えエラー')
    print(e)

for res in check_url:
    try:
        res_get = requests.get(res, timeout=(10, 15), verify=False)
    except Exception as e:
        low_risk_url.append(res)
        print('URLアクセスエラー')
        print(e)

    print(res_get.status_code, res)
    check_code = res_get.status_code
    if 500 == check_code:
        print('500発見' + res)
        alert_url.append(res)
    if 404 == check_code:
        alert_url.append(res)
        print('404発見' + res)
    if 403 == check_code:
        print('403発見' + res)
        alert_url.append(res)

for re_res in low_risk_url:
    print('low_risk_urlの2回目チェック')
    try:
        res_get = requests.get(re_res, timeout=(20, 45), verify=False)

    except Exception as e:
        again_low_risk_url.append(re_res)
        print('URLアクセスエラー(2回目チェック)')
        print(e)

    print(res_get.status_code, re_res)
    check_code = res_get.status_code
    if 500 == check_code:
        print('500発見' + re_res)
        alert_url.append(re_res)
    if 404 == check_code:
        alert_url.append(re_res)
        print('404発見' + re_res)
    if 403 == check_code:
        print('403発見' + re_res)
        alert_url.append(re_res)

for re_re_res in again_low_risk_url:
    print('again_low_risk_urlの3回目チェック')
    try:
        res_get = requests.get(re_re_res, timeout=(20, 45), verify=False)

    except Exception as e:
        print('URLアクセスエラー(3回目チェック)')
        print(e)
        alert_url.append(re_re_res)

    print(res_get.status_code, re_re_res)
    check_code = res_get.status_code
    if 500 == check_code:
        print('500発見' + re_re_res)
        alert_url.append(re_re_res)
    if 404 == check_code:
        alert_url.append(re_re_res)
        print('404発見' + re_re_res)
    if 403 == check_code:
        print('403発見' + re_re_res)
        alert_url.append(re_re_res)


print('クロール完了', '\n\n'.join(alert_url))

try:
    if not alert_url:
        message = 'WEBサイトチェック問題なし！'
    else:
        message = '※アクセスできないWEBサイト発見！※' + '\n'.join(alert_url)

    BASE_URL = 'https://api.chatwork.com/v2'
    roomid = ''  # ルームIDを記載
    apikey = ''  # APIのKeyを記載

    post_message_url = '{}/rooms/{}/messages'.format(BASE_URL, roomid)
    headers = {'X-ChatWorkToken': apikey}
    params = {'body': message}
    r = requests.post(post_message_url, headers=headers, params=params)

except Exception as e:
    print('チャットワークに書き込みエラー')
    print(e)
