######################
#赤外線操作モジュールクラス
#別ウィンドウでターミナルを起動して
# $ sudo lircd -n -d /dev/lirc0
#を実行しておくこと
######################
import subprocess

class Remote_module:

    def __init__(self):
        #####初期化#####
        # etc/share/doc/lirc/README.Debianの内容に基づく
        # 大元の名前？とりあえずroomで設定してるやつと
        # それぞれの操作の名前を設定
        # 照明オン、照明オフ、照明を常備灯にする、テレビオン、テレビオフ
        # の命令を想定してるよ。
        self.CURRENTNAME="room"                      
        self.ACTIONS = {"LIGHT_ON":"light_on",
                        "LIGHT_OFF":"light_off",
                        "LIGHT_ORANGE":"light_orange",
                        "TV_ON":"tv_on",
                        "TV_OFF":"tv_off"}

    #操作用の関数だよ、引数に↑のACTIONSディクショナリのキーを入れてね
    def remoteAction(self,action):
        subprocess.call(["irsend","SEND_ONCE",self.CURRENTNAME,self.ACTIONS[action]])