# for python 3.7.0
# メール送信用
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 時刻
from datetime import datetime
# html request
import requests
# html scraping
from bs4 import BeautifulSoup
import re
suii = 0
# URL先のhtml取得
# 国土交通省　川の防災情報の観測所データページで10分毎の水位を選択したURL
res=requests.get('http://www.river.go.jp/kawabou/ipSuiiKobetu.do?obsrvId=0665700400003&gamenId=01-1003&stgGrpKind=survForeKjExpl&fldCtlParty=no/&fvrt=yes&timeType=10')
# エンコード推定機能をONに
res.encoding = res.apparent_encoding
# エラーチェック
res.raise_for_status()
# 取得したhtmlをパース(html5libのインストールが必要)
bs = BeautifulSoup(res.content,'html5lib')

# 観測地名を取得
topos = bs.select_one(".comHeaderspotLbl")
toposs = str.strip(topos.getText())
toposss = toposs.split("：")
kansokujo = toposss[1]
print(kansokujo)

# 最新の水位と時刻を取得
elems = bs.select_one('#hyou')
elemss = elems.find_all("tr")
elem = elemss[-1]
#print(elem)
elem0 = elem.find_all("td")
# 時刻
jikoku = str.strip(elem0[0].string)
# 水位(文字列、表示・送信用)
suii = str.strip(elem0[1].string)
# 水位(数値、判定用)
suii_float = float(suii)
print(jikoku)
print(suii)

# メール送信設定
srv_smtp = 'XXXXXXXXXXXXXXXXXXXXXX'  # SMTPサーバ
srv_port = 587                 # ポート番号
srv_user = 'XXXXXXXXXXXXXXXXXXXXXX'            # サーバのユーザ名
srv_pw   = 'XXXXXXXXXXXXXXXXXXXXXX'          # サーバのパスワード
jp_encoding = 'iso-2022-jp'    # 日本語文字エンコーディングの指定
add_sender = 'XXXXXX@XXXXXXXXXXXX.jp'  # 差出人アドレスの設定
add_to = 'XXXXX@XXXXXXXXXXXX.jp,YYYYY@XXXXXXXXXXXX.jp'	# 宛先アドレスの設定
#add_bcc = 'XXXX@XXXXXX.jp'     # BCCアドレスの設定
mail_subject = kansokujo + 'の水位:' + suii + "m"         # 件名
mail_body = jikoku + "の" + kansokujo + "の水位は" + suii + "mです。"	# 本文

# 水位が??m以上又は??時だけ送信
if (suii_float > 1.6 or ( datetime.now().hour == 8 and datetime.now().minute < 10 ) ) :
	# SMTPサーバへの接続
	server = smtplib.SMTP(srv_smtp, srv_port)
	server.ehlo()
	server.starttls()  # TLSでアクセス
	server.ehlo()
	server.login(srv_user,srv_pw)  # ログイン認証
	# 送信
	try:
		msg = MIMEText(mail_body.encode(jp_encoding), 'plain', jp_encoding,)
		msg['From'] = add_sender
		msg['Subject'] = Header(mail_subject, jp_encoding)
	#	msg['Bcc'] = add_bcc
		msg['To'] = add_to
		server.send_message(msg)  # 送信する
	except Exception as e:
	    print('=== エラー内容 ===')
	    print(str(e))
	# サーバ接続を終了
	server.close()

