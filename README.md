# 我が家のあかねちゃんプロジェクト
我が家のあかねちゃんプロジェクトで使用したソースコード等のリポジトリです．  
プロジェクトの概要は，[紹介動画](http://www.nicovideo.jp/watch/sm31762094)や[Webサイト](http://wagayakane.html.xdomain.jp/)を参照してください．  
![overview](https://github.com/hmhm903/WagayaNoAkaneChan/blob/master/img/overview.png)
以下で各機能の詳細を記載します．  

## 音声認識機能(voice_recognizer)
### config.pyのvoice_recognizerの項目を編集する。
1. VR_THRESHOLD
手を叩く等の大きい音を検知した際に、音声認識モードに切り替える為に設定する値。
大きい音として判定する閾値を入力する。
値を小さくしすぎると小さな雑音にも反応してしまうので注意。
環境によって適切な値変わる事が予想されるので、何度も値を変化させつつ試しながら設定するといいかも。

1. VR_RECORD_SECONDS
音声認識モードの時間（音声の録音時間）
初期設定は3秒。
Docomo音声認識APIの仕様上、10秒以内に設定する必要がある。

1. VR_API_KEY
以下のページを参考に取得したDocomo音声認識APIのAPIキーを入力。
http://uepon.hatenadiary.com/entry/2016/12/20/000353

1. VR_URL
Docomoの音声認識サーバーにリクエストを送信するためのURL。
初期値のままでOK。

### 再生する茜ちゃんの音声設定
clieent.pyのself.VOICEの項目を再生したい音声ファイルに差し替える。  
赤外線の操作項目を増やした時はここの項目も増やすといいと思います。  
ファイルの再生は play(self.VOICE[ディクショナリキー]) で出来ます。  
- "VOICE_RECOGNITION":音声認識モードに移行した際の音声
- "WEATHER":指示を受けて天気予報画像に切り替えた祭の音声
- "MAIL":同様にメール画面に切り替えた際の音声
- "SCHEDULE":スケジュール画面に切り替えた際の音声
- "LIGHT_ON":照明を付ける際の音声
- "LIGHT_OFF":照明を消す祭の音声
- "LIGHT_ORANGE":常備灯に切り替えた際の音声
- "TV_ON":テレビを付ける際の音声
- "TV_OFF":テレビを消す祭の音声

## 音声認識およびツイッターのリプライ反応での認識文字列
音声から認識した文字列およびツイッターのリプライに以下の文字列が含まれている場合、命令を実行します。
- "天気":天気画面への変更
- "スケジュール":スケジュール画面への変更
- "メール":メール画面への変更
- "電気"および"つけて":電気をつける
- "電気"および"消して":電気を消す
- "常備":常備灯にする
- "テレビ"および"つけて":テレビをつける
- "テレビ"および"消して":テレビを消す
我々のプログラムはまともに例外処理を書いていないので
これらを完璧に設定しなければ動作が停止します。

## ツイッターに関する設定項目
ツイッターから命令を受け取るには以下の項目を設定してください。
### ツイッターの各種キーの取得
コンシューマキー、コンシューマシークレット、アクセストークン、アクセストークンシークレットが要ります。
取得の仕方は[このページ](https://qiita.com/konojunya/items/59a68d35e44db8b87186))を参照。
取得した各キーをconfig.pyの
- TW_CONSUMER_KEY:コンシューマキー
- TW_CONSUMER_SECRET:コンシューマシークレット
- TW_ACCESS_TOKEN:アクセストークン
- TW_ACCESS_TOKEN:アクセストークンシークレット
にそれぞれ文字列として設定してください。

### 命令を認識するアカウントの設定
ツイッターからの命令を認識するアカウントの設定としてツイッターIDが要ります。
任意のIDをconfig.pyのTW_OWNER_ACCOUNTに設定してください。
このツイッターアカウントからのリプライを命令として取得します。

## Googleのデータ（メール、予定）に関する設定
各種データを表示するためには以下の項目を設定してください。
### メール、予定共通
Googleのデータを取得するには、まずGoogle Developers ConsoleからOAuthクライアントIDを作成する必要があります。
作成の仕方は[このページ](https://qiita.com/t-mochizuki/items/ab4a0b2f70426f73e1b6)を参照。
その後ダウンロードボタンからJSON形式の認証情報ファイルを入手し、main_view直下に配置してください。
そして、以下の項目を設定してください。
- GO_CLIENT_SECRET_FILE:認証情報ファイル名
- GO_APPLICATION_NAME:作成したクライアントIDの名前

### mailに関する設定
Google Developers ConsoleからGmail APIを有効にしてください。
またconfig.pyのMA_LABEL_IDを取得したいメールのラベルを文字列で指定してください。
特に指定がなければ*INBOX*に設定してください。

### Googleカレンダーの予定に関する設定
Google Developers ConsoleからGoogle Calendar APIを有効にしてください。
またconfig.pyのSC_CALENDAR_IDを取得したいメールのラベルを文字列で指定してください。
特に指定がなければ*primary*に設定してください。

## 天気に関する設定
天気情報を表示するには以下の設定を行ってください。

### 天気情報の取得
天気に関するデータは[Weather Hacks](http://weather.livedoor.com/weather_hacks/)から取得しています。
これには地域別に指定されたID番号を設定する必要があります。
ID番号は[このページ](http://weather.livedoor.com/forecast/rss/primary_area.xml)から検索して調べてください。
このID番号をconfig.pyのWE_LOCATIONに文字列として設定してください。

### 天気画像の設定
著作権上の観点からこのリポジトリには画像データが含まれていません。
そのため自ら天気の画像を取得してくる必要があります。
必要な画像は以下の3枚です。
- sunny.png:晴れを表す画像
- rainy.png:雨を表す画像
- cloudy.png:曇りを表す画像
maing_viewフォルダ内にimgフォルダを作成し、これらの画像をその直下に配置してください。

## 赤外線通信について
赤外線通信については，主に[Raspberry pi 3 で部屋の赤外線受信できる機器をコントロール！](http://qiita.com/_kazuya/items/62a9a13a4ac140374ce8)を参考に作成しています．
### 赤外線送受信モジュールの作成
赤外線通信を行うためには，別途赤外線通信用モジュールを作成する必要があります．
[Webサイトの回路図](http://wagayakane.html.xdomain.jp/explanation.html)や以下を参考に，各自作成をお願いします．
![circuit_module](https://github.com/hmhm903/WagayaNoAkaneChan/blob/master/img/circuit.jpg)

#### 使用部品
- 赤外線受光モジュール：VS1838B　×1  
- 5mm赤外線LED：OSI5LA5113A　×3  
- トランジスタ：2SC1815GR 60V 150mA　×1  
- カーボン抵抗：1/6W 10Ω　×1  
- カーボン抵抗：1/6W 680Ω　×1  

※ジャンパ線等は省略
#### 受信部分
ラズパイに赤外線送信モジュールをそのまま接続しています。VS1838Bを使うと鉄壁のシールドによりノイズ耐性強し。

#### 送信部分
ラズパイに赤外線LEDを繋いでます。送信強度を増すために3つのLEDを駆動しています。

#### 赤外線送受信モジュール
送信部分と受信部分を1枚の基板にはんだ付けしてモジュール化しています．
![circuit_module](https://github.com/hmhm903/WagayaNoAkaneChan/blob/master/img/circuit_board.jpg)

### 赤外線送受信モジュールとRaspberry Piの接続
作成した赤外線送受信モジュールをRaspberry Piを以下のように接続します．  
- 1pin(3V3)- 受信モジュールのVCC  
- 18pin(GPIO24)- 受信モジュールのOUT
- 20pin(GND)- 受信モジュールのGNDと赤外線LEDのGND
- 22pin(GPIO25)- 赤外線LEDの電源  

なお使用するピンは，/boot/config.txtを編集することで変更できます．

### 赤外線の登録・発信
次に受信モジュールを利用し，何らかのリモコン(エアコン，テレビなど)の操作を登録します(上記のリンク参照)．
このリポジトリでは，"light_on",  "light_off", "light_orange", "tv_on", "tv_off"という名目で，それぞれの操作を登録し，remote_module.pyでそれらを利用した発信操作を行っています．  
なおirsendコマンド実行時に  
"irsend: could not connect to socket"  
"irsend: No such file or directory"  
と出てくる場合は  
"$sudo killall lircd"  
"$sudo lircd"  
とするとうまくいきます．
参考：https://teratail.com/questions/24338

また  
"irsend: hardware does not support sending"  
と出てくる場合は，別ターミナルで以下のコマンドを実行しておけばうまくいきます．  
"$ sudo lircd -n -d /dev/lirc0"  
参考：http://myoji.blog.so-net.ne.jp/2017-02-13

## MMD
MMDについては，shirobuさんの[mmdpi](https://github.com/shirobu2400/mmdpi)を使わせていただきました．紹介動画では，天気等が表示される領域とMMDの領域を2:1に分けて描画していす．
