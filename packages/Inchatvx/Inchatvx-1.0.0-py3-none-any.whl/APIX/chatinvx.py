import requests
import json
from rich import print

# ==============================
# Library by Vermouth
# ==============================

class InChatAPI:
    BASE_URL = "https://wenextinchat.com/api"
    LIBRARY_VERSION = "1.0"

    def __init__(self, device_id, new_device_id, token):
        self.headers = {
            "Accept-Encoding": "gzip",
            "app_name": "inchat",
            "channel": "google-play",
            "Connection": "Keep-Alive",
            "country_code": "IQ",
            "device": "Android",
            "device_id": device_id,
            "from_page": "com.adealink.weparty.MainActivity",
            "Host": "wenextinchat.com",
            "If-Modified-Since": "Tue, 21 Jan 2025 13:29:13 GMT",
            "lang_country_code": "EG",
            "language_code": "ar",
            "new_device_id": new_device_id,
            "package_name": "com.wenext.inchat",
            "platform": "android",
            "region": "DE",
            "req_id": "unique-request-id",
            "token": token,
            "User-Agent": "okhttp/4.12.0",
            "version_code": "25"
        }
        self._print_version()

    @staticmethod
    def _print_version():
        print("[yellow]Library Version: 1.0[/yellow] - Open-source library for Chat Golden, developed by Vermouth.")

    def _get(self, endpoint):
        self._print_version()
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"GET Request Failed: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"GET Request Error: {e}")
        return None

    def _post(self, endpoint, data):
        self._print_version()
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"POST Request Failed: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"POST Request Error: {e}")
        return None

    def get_user_info(self, uid, token):
        self.headers['token'] = token  # Token for dynamic usage
        endpoint = f"/user/getUserInfoByUid/{uid}"
        return self._get(endpoint)

    def get_follow_count(self, token):
        self.headers['token'] = token
        endpoint = "/user/getFollowCount"
        return self._get(endpoint)

    def verify_code(self, email, code, token):
        self.headers['token'] = token
        data = {
            "verifyCode": code,
            "mailAccount": email
        }
        endpoint = "/account/validate/verifyCode"
        return self._post(endpoint, data)

    def update_email(self, email, password, verify_code, token, temp_token, uid):
        self.headers['token'] = token
        data = {
            "mailAccount": email,
            "mailPassword": password,
            "verifyCode": verify_code,
            "tempToken": temp_token,
            "uid": uid
        }
        endpoint = "/account/updateMailUserInfo"
        return self._post(endpoint, data)

    def get_new_fans(self, token):
        self.headers['token'] = token
        endpoint = "/user/showNewFans"
        return self._get(endpoint)

# ==============================
# Developer Info (For Attribution)
# ==============================
# Developed by Vermouth
# GitHub: https://github.com/Vermouth4/
# Instagram: https://www.instagram.com/m3.a0/
# Pypi: https://pypi.org/user/Vermouth/

# ==============================
# جرب ولا تنسئ حقوقي :)
# ==============================
if __name__ == "__main__":
    device_id = "8193e6fc-2e23-42b8-8819-fa4c7d43570"
    new_device_id = "369721"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5ZTYzMjUxOC1mNWM4LTRjZjMtOWU2NC0zMDY4OWEwZDcwMjgiLCJpYXQiOjE3Mzc0NjQxMTYsImlzcyI6IndlcGFydHktZ2F0ZXdheSIsInN1YiI6IntcInVpZFwiOjM1MjgzMixcInNob3J0SWRcIjoxMDAzNTI3OTYsXCJ0eXBlXCI6XCJ3ZXBhcnR5X3dlYnNvY2tldFwifSIsImV4cCI6MTc0MDA1NjExNn0.A-rouOvi-5ZuObb7RIu5BF17ydIUJDj_zPvo-oCnaBM"
    api = InChatAPI(device_id, new_device_id, token)
    uid = 352832
    print(api.get_user_info(uid, token))
    print(api.get_follow_count(token))
    email = "dyam1487@gmail.com"
    code = "550788"
    print(api.verify_code(email, code, token))
    new_email = ""
    password = ""
    temp_token = "m66j7818fywe"
    print(api.update_email(new_email, password, code, token, temp_token, uid))
    print(api.get_new_fans(token))
