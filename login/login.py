import json
import requests

from utils.encrypt import RSAUtil
from utils.settings import GLOBAL_HEADERS


def _get_server_timestamp():
    resp = requests.get(url="https://i.zmlearn.com/tracker/getServerTimestamp", headers=GLOBAL_HEADERS)
    json_obj = json.loads(resp.text)
    return str(json_obj["time"])
    pass


def _get_rsa_pub():
    resp = requests.get(url="https://chat.zmlearn.com/gateway/zmc-login/api/oauth/rsaPubKey",
                        headers=GLOBAL_HEADERS)
    json_obj = json.loads(resp.text)
    return str(json_obj["data"])
    pass


class AuthCenter:

    pre_url = "https://chat.zmlearn.com/react/teacherhome"

    login_url = "https://chat.zmlearn.com/gateway/zmc-login/api/oauth/loginNew"

    def __init__(self, mobile, password):
        self.mobile = str(mobile)
        self.password = str(password)
        self.user_info = None
        self.cookie = None

        pass

    def get_cookie(self):
        if self.cookie is None:
            self.cookie = self._get_cookie()
            return self.cookie
            pass
        else:
            return self.cookie
        pass

    def get_access_token(self):
        if self.user_info is None:
            self.user_info = self._fetch_user_info()
            self.cookie = self._get_cookie()
            return self.user_info["accessToken"]
            pass
        else:
            return self.user_info["accessToken"]
        pass

    def _fetch_user_info(self):
        # timestamp = int(time.time() * 1000)
        timestamp = 1615392910653
        json_text = str(json.dumps({
            "mobile": str(self.mobile),
            "password": self.password,
            "timestamp": str(timestamp)
        }))

        json_text = json_text.replace(" ", "")

        print("login payload brfore encrypt:", json_text)
        pub_key = _get_rsa_pub()
        print("rsa public key:", pub_key)

        crypto = RSAUtil.encrypt(pub_key, json_text)
        payload = dict()
        payload["msg"] = crypto
        print("login payload:", payload)
        resp = requests.post(url=AuthCenter.login_url, headers=GLOBAL_HEADERS, json=payload)
        print("login response code:", resp.status_code)
        print("login response body:", resp.text)

        json_obj = json.loads(resp.text)
        return json_obj["data"]
        pass

    def _get_cookie(self):
        resp = requests.get(url=self.pre_url, headers=GLOBAL_HEADERS)
        GLOBAL_HEADERS["Cookie"] = resp.headers["Set-Cookie"]
        return resp.headers["Set-Cookie"]
        pass

    pass
