from hashlib import sha256
import time
import rfc822
import base64
import hmac
import urllib
import requests

app_id = "app-cvts1w3s"

BASE_SSO_URL = "http://sso.nscccloud.com"
BASE_API_URL = "http://api.nscccloud.com:7777"


class QcControl:

    def __init__(self, access_token, refresh_token):
        self.access_key = ""
        self.secret_key = ""
        self.token = ""
        self.user = ""
        self.access_token = access_token
        self.refresh_token = refresh_token

        check_token_resp = self.check_token()
        if check_token_resp is None:
            print("check access_token failed")
            return

        self.handle_map = {
            "DescribeUserInfo": self.handle_describe_user_info,
            "NBDescribeBills": self.handle_nb_describe_bills,
            "NBGetCostsSimple": self.handle_get_costs_simple,
            "NBGetPrice": self.handle_nb_get_price,
            "NBCreatePrdOrderSimple": self.handle_nb_create_prd_order_simple,
            "NBSearchPrdOrders": self.handle_nb_search_prd_orders,
            "NBChargePrdOrder": self.handle_nb_charge_prd_order,
            "NBCancelPrdOrder": self.handle_nb_cancel_prd_order,
            "NBDescribeProdInstances": self.handle_nb_describe_prod_instances,
            "NBPauseProdInstance": self.handle_nb_pause_prod_instance,
            "NBRenewProdInstance": self.handle_nb_renew_prod_instance,
            "NBResumeProdInstance": self.handle_nb_resume_prod_instance,
            "NBStopProdInstance": self.handle_nb_stop_prod_instance,
        }

    def handle(self, action, **params):
        print "handle action of %s" % action
        return self.handle_map[action](action, **params)

    def handle_describe_user_info(self, user_id, **params):
        if isinstance(user_id, list):
            user_id = user_id[0]
        req = {
            "action": "DescribeUsers",
            "user_id": user_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_get_costs_simple(self, **params):
        req = {
            "action": "NBGetCostsSimple",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_get_price(self, **params):
        req = {
            "action": "NBGetPrice",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_create_prd_order_simple(self, **params):
        req = {
            "action": "NBCreatePrdOrderSimple",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_search_prd_orders(self, **params):
        req = {
            "action": "NBSearchPrdOrders",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_describe_bills(self, **params):
        req = {
            "action": "NBDescribeBills",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_charge_prd_order(self, **params):
        req = {
            "action": "NBChargePrdOrder",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_cancel_prd_order(self, **params):
        req = {
            "action": "NBCancelPrdOrder",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_describe_prod_instances(self, **params):
        req = {
            "action": "NBDescribeProdInstances",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_pause_prod_instance(self, **params):
        req = {
            "action": "NBPauseProdInstance",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_renew_prod_instance(self, **params):
        req = {
            "action": "NBRenewProdInstance",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_resume_prod_instance(self, **params):
        req = {
            "action": "NBResumeProdInstance",
            "app_id": app_id,
        }
        resp = self.send_appcenter_request(req)
        return resp

    def handle_nb_stop_prod_instance(self, **params):
        req = {
            "action": "NBStopProdInstance",
            "app_id": app_id,
            "search_word": "xxxx",
        }
        resp = self.send_appcenter_request(req)
        return resp

    def get_user_info(self):
        return self.user

    def check_token(self):
        url = BASE_SSO_URL + "/sso/check_token/"
        resp = requests.post(
            url=url,
            headers={
                "Authorization": "Bearer " + self.access_token,
                # 'content-type': 'application/x-www-form-urlencoded',
                'date': rfc822.formatdate(time.time())
            })
        if resp.status_code != 200:
            return
        check_token_resp = resp.json()
        print("check token response[%s]" % check_token_resp)
        self.access_key = get_utf8_value(check_token_resp.get("access_key"))
        self.secret_key = get_utf8_value(check_token_resp.get("secret_key"))
        self.token = get_utf8_value(check_token_resp.get("token"))
        self.user = check_token_resp.get("user")
        return "success"

    def refresh_token(self):
        url = BASE_SSO_URL + "/sso/refresh_token/"
        resp = requests.post(
            url=url,
            headers={
                "Authorization": "Bearer " + self.access_token,
                'Content-Type': 'application/x-www-form-urlencoded',
                'date': rfc822.formatdate(time.time())
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            }
        )
        if resp.status_code != 200:
            return
        refresh_token_resp = resp.json()
        self.access_token = refresh_token_resp.get("access_token")
        self.refresh_token = refresh_token_resp.get("refresh_token")
        return "success"

    def send_appcenter_request(self, req):
        url = BASE_API_URL + "/iam/"
        params = {
            'access_key_id': self.access_key,
            'open_name': 'appcenter',
            'signature_version': 1,
            'signature_method': 'HmacSHA256',
            'time_stamp': get_ts(),
            'token': self.token,
        }
        params.update(**req)
        sign, query_string = get_signature(params, self.secret_key, "/iam/", method="GET")
        url += '?%s&signature=%s&token=%s' % (query_string, sign, self.token)
        print("url[%s]" % url)
        resp = requests.get(url=url, verify=False)

        if resp.status_code == 401:
            if self.refresh_token() is None:
                print("failed to refresh token")
                return
            if self.check_token() is None:
                print("failed to check token")
                return
        print("IAM response:[%s]" % resp.json())
        return resp.json()


ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


def get_ts(ts=None):
    ''' get formatted UTC time '''
    if not ts:
        ts = time.gmtime()
    return time.strftime(ISO8601, ts)


def get_signature(params, secret_access_key, path, method="POST"):
    string_to_sign = '%s\n%s\n' % (method, path)
    keys = sorted(params.keys())
    pairs = []
    for key in keys:
        val = get_utf8_value(params[key])
        pairs.append(urllib.quote(key, safe='') + '=' + urllib.quote(val, safe='-_~'))
    qs = '&'.join(pairs)
    string_to_sign += qs
    print("string_to_sign[%s]" % string_to_sign)
    h = hmac.new(secret_access_key, digestmod=sha256)
    h.update(string_to_sign)
    sign = base64.b64encode(h.digest()).strip()
    signature = urllib.quote_plus(sign)

    return signature, qs


def get_utf8_value(value):
    if not isinstance(value, str) and not isinstance(value, unicode):
        value = str(value)
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value


if __name__ == '__main__':
    req = {
        'action': 'DescribeUsers',
        'access_key_id': 'W3wyXVT05ji70pscFQEkXQ',
        'open_name': 'appcenter',
        'signature_version': 1,
        'signature_method': 'HmacSHA256',
        'time_stamp': '2020-11-25T07:48:07Z',
        'user_id': 'admin',
        'token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY3IiOiIxIiwiYXVkIjoiaWFtIiwiYXpwIjoiaWFtIiwiY29ucyI6Im5zY2NjbG91ZCIsImN1aWQiOiJpYW1yLXBlN2lpamxuIiwiZWlzayI6IjRYR05vMS1HenNZSUpvcmRBTXR6STJoZmVOdjMwU1pNNTJBQlVNMW1fTG89IiwiZXhwIjoxNjA2MjkzMjczLCJpYXQiOjE2MDYyODk2NzMsImlzcyI6InN0cyIsImp0aSI6Ilczd3lYVlQwNWppNzBwc2NGUUVrWFEiLCJuYmYiOjAsIm9yZ2kiOiJhcHAtQ1FIWXJhS2YiLCJvd3VyIjoiYWRtaW4iLCJwcmVmIjoicXJuOnFpbmdjbG91ZDppYW06Iiwicm91ciI6ImFkbWluIiwicnR5cCI6InJvbGUiLCJzdWIiOiJzdHMiLCJ0eXAiOiJJRCJ9.Lf-zIRcYDf5t9Qqqki3Q2f1xAh5sWd_kaSm1_JtS-m9SXG7FaCgXsI3ha_VdL88SUeAn16w_b8--MQX0d00aclZIiSw8GLwEb6q2tgH0GCP5WAYD9BRu1outcqKspKieSzwx3uH7I462i9YHMpcwuF4lRlEiSVPwtrnPXypd1rg',
    }
    sign, query_string = get_signature(req, 'qUbMeccvYb8a4c0', "/`/", method="GET")
    print("signature[%s]" % sign)
    print("url[https://api.qingcloud.com/iaas/?%s&signature=%s]" % (query_string, sign))
