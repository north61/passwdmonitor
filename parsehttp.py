from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message =emessage

request_text = (
'''POST /login HTTP/1.1
Host: 10.101.1.176:8080
Content-Length: 133
Cache-Control: max-age=0
Origin: http://10.101.1.176:8080
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Referer: http://10.101.1.176:8080/login
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: session=eyJjc3JmX3Rva2VuIjp7IiBiIjoiWXpjd1pHTTFOV1k1WkRCa05tSmxNVFl6WVdJMVltVTJOVGN6TXpVd09UZ3pNMlkzTURFeVlRPT0ifX0.EAB5Tg.0paj5LaeVnvHPORxn6xFZBiTwbk
Connection: close

csrf_token=ImM3MGRjNTVmOWQwZDZiZTE2M2FiNWJlNjU3MzM1MDk4MzNmNzAxMmEi.EAB5Yg.Yb3kcYvmIpMRVGWBg_yEVJ3oC64&account=$admin$&password=*mljr123*'''
    )

request = HTTPRequest(request_text)

print request.error_code       # None  (check this first)
print request.command          # "GET"
print request.path             # "/who/ken/trust.html"
print request.request_version  # "HTTP/1.1"
print len(request.headers)     # 3
print request.headers.keys()   # ['accept-charset', 'host', 'accept']
print request.headers['host']  # "cm.bell-labs.com"
