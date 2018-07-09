# river_water_level

実現できること：
国土交通省 川の防災情報<http://www.river.go.jp/kawabou/ipTopGaikyo.do?init=init&gamenId=01-0101&fldCtlParty=no>を用いて河川の水位を取得し、メール送信する。

動作環境：Python 3.7.0, Windows 64bit

必要なパッケージ：requests, bs4, html5lib

必要な準備：
1.河川の水位の時間変化で10分毎の水位を選択したURLをスクリプトの所定の場所に記載
2.メールサーバ等のメール設定を記載
3.一定間隔で自動実行する場合は、タスクスケジューラやCRON等の設定が別途必要

備考：
・ダムの水位も取得可能
・Webサイトがリニューアルされると情報が取得できなくなるため、適切にデータが取得できているかを定期的にチェックする必要がある。
