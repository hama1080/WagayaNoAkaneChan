# -*- coding:utf-8 -*-
#voice_recognizer
VR_THRESHOLD = 0.5
VR_RECORD_SECONDS = 3
VR_API_KEY = ""
VR_URL = URL = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(VR_API_KEY)

#twitter
TW_CONSUMER_KEY = ""
TW_CONSUMER_SECRET = ""
TW_ACCESS_TOKEN = ""
TW_ACCESS_TOKEN_SECRET = ""
TW_OWNER_ACCOUNT_ID = ""

#weather
WE_LOCATION = "130010"

#Google共通
GO_CLIENT_SECRET_FILE = "client_secret.json"
GO_APPLICATION_NAME = ""

#mail
MA_SCOPES = "https://www.googleapis.com/auth/gmail.readonly"
MA_LABEL_ID = "INBOX"

#schedule
SC_SCOPES = "https://www.googleapis.com/auth/calendar.readonly"
SC_CALENDAR_ID = "primary"

#clocker
MAIN_PROGRESS_BAR_MAX = 20



def check():
    import re
    settings = [v for k,v in globals().items() if not re.match("__.+__", k)]
    if (None or "") in settings:
        raise Exception("Some config values are empty")


if __name__ == "__main__":
    check()
