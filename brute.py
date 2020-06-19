import requests 
import argparse
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
import re
import MySQLdb
import md5
import sys
import json

db = MySQLdb.connect("127.0.0.1","root","123456","secpassword",port=3307,charset="utf8")

cursor = db.cursor()

#cursor.execute("SELECT VERSION()")
#
#data = cursor.fetchone()
#cursor.execute("select * from http_body where id=%s" % (1) )
#rows = cursor.fetchone()
##for row in rows:
##    print row
#data_id = rows[0]
#data_title = rows[1]
#body = rows[2]
#print "Database version : %s " % data

#db.close()


def getrequest(id):
    sql = "select httpbody from http_body where id = %s"  % (int(id))
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message
#proxies={"http":"http://172.28.13.91:8080"}
headers = {}

#body = '''POST /login HTTP/1.1
#Host: 10.101.1.176:8080
#Content-Length: 133
#Cache-Control: max-age=0
#Origin: http://10.101.1.176:8080
#Upgrade-Insecure-Requests: 1
#Content-Type: application/x-www-form-urlencoded
#User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
#Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
#Referer: http://10.101.1.176:8080/login
#Accept-Encoding: gzip, deflate
#Accept-Language: zh-CN,zh;q=0.9
#Cookie: session=eyJjc3JmX3Rva2VuIjp7IiBiIjoiTnpFd1pHUXdZV1kxWm1NeU16RmtORFU0T0dFeU1XUTJaVFV4WVRFek9UTTNOamMzTjJOaU13PT0ifSwibG9naW4iOnsiIGIiOiIifX0.EAWU8w.J5PkqgwFH6jQbne1TMuLlNvcUOI
#Connection: close
#
#csrf_token=IjcxMGRkMGFmNWZjMjMxZDQ1ODhhMjFkNmU1MWExMzkzNzY3NzdjYjMi.EAWU8w.cHKAFMn2-JR8DsaWRUP2G6d0JQ8&account=$admin$&password=*Mljr123*'''



##print request.headers['cookie']

#print request.error_code       # None  (check this first)
#print request.command          # "GET"
user_list = [] 
passwd_list = [] 
def getuser(usertype):
    global user_list 
    sql = "select %s from user_dict" % (usertype) 
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        user_list.append(row[0])
    if usertype == 'employid':
        user_list = []
        user_list = ["M0"+ str(num).rjust(5,'0') for num in range(1, 50000)]
    

def getpass(pwdtype):
    sql = "select password from password_dict where dicttype=\"%s\"" % (pwdtype)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        passwd_list.append(row[0])


def bruteforce(body,responsecode,responselen,response_partern,password_md5,httpbody_type):
    #user_list = ['hebei.zhang01@mljr.com']
    #passwd_list = ["88888888","1234567"]
    request = HTTPRequest(body)
    content_len = int(request.headers['content-length'])
    headers = {}
    for key,value in request.headers.items():
        headers[key] = value    
    print headers
    print body
    #sys.exit()
    #print content_len + 4
    #print request.headers['host']
    post_body = request.rfile.read(content_len + 4)
    #print post_body
    url = "http://"+request.headers['host'] + request.path
    #print url
    #print request.headers,type(request.headers)

    user = ''
    passwd = ''
    if httpbody_type == "1":
        payload = {}
        x = re.search(".*?(\w+)=\$(.*?)\$.*",post_body)

        if request.command == "POST":
            x = re.search(".*?(\w+)=\$(.*?)\$.*",post_body)
            user,v = x.groups()
            post_body=  post_body.replace("{}=${}$".format(user,v),"{}={}".format(user,"secusername"))
            #print post_body 
            x = re.search(".*?(\w+)=\*(.*?)\*.*",post_body)
            passwd,v = x.groups()
            post_body=  post_body.replace("{}=*{}*".format(passwd,v),"{}={}".format(passwd,"secpassword"))
        for post in post_body.split('&'):
            key = post.split('=')[0]
            value = post.split('=')[1]
            payload[key] = value
        for username in user_list:
            payload[user] = username
            for pwd in passwd_list:
                payload[passwd] = pwd.strip('\r\n')
                if password_md5 == "1":
                    m = md5.new()
                    m.update(pwd)
                    payload[passwd]= m.hexdigest()
        #print post_body 
                try:
                    r = requests.post(url,data=payload,headers=headers,allow_redirects = False)
                except:
                    pass
                else:
                    if r.status_code == int(responsecode) or int(responsecode) == 1:
                        print payload,r.status_code, len(r.text)
                    #print payload
                    #print r.status_code,r.headers['Content-Length']
                        #if r.headers['Content-Length'] == int(responselen):
                        if response_partern == '':
                            sql = 'insert into web_result(username,password,httpbody_id,http_code,http_length) values("%s","%s",%d,"%s","100")' % (username,pwd,1,r.status_code)
                            cursor.execute(sql)
                            db.commit()
                        elif r.text.find(response_partern) != -1:
                            print r.text,response_partern
                            sql = 'insert into web_result(username,password,httpbody_id,http_code,http_length) values("%s","%s",%d,"%s","100")' % (username,pwd,1,r.status_code)
                            cursor.execute(sql)
                            db.commit()
                        else:
                            continue
    elif httpbody_type == "2":
        payload = {}
        if request.command == "POST":
            x = re.search("[\"|'].*?(\w+)[\"|']:[\"|']\$(.*?)\$.*[\"|']",post_body)
            print post_body 
            user,v = x.groups()
            print user,v
            print '''aaaa'''
            post_body=  post_body.replace("{}:${}$".format(user,v),"{}:{}".format(user,"secusername"))
            x = re.search("[\"|'].*?(\w+)[\"|']:[\"|']\*(.*?)\*.*[\"|']",post_body)
            passwd,v = x.groups()
            print passwd,v
            post_body=  post_body.replace("{}:*{}*".format(passwd,v),"{}:{}".format(passwd,"secpassword"))
            print post_body
            #sys.exit()
            payload = json.loads(post_body)
            #for post in post_body.split(','):
            #    key = post.split(':')[0]
            #    value = post.split(':')[1]
            #    print key,value
            #    #payload[key] = value
        
#    for post in post_body.split('&'):
#        key = post.split('=')[0]
#        value = post.split('=')[1]
#        payload[key] = value
        for username in user_list:
            payload[user] = username
            for pwd in passwd_list:
                payload[passwd] = pwd
                if password_md5 == "1":
                    m = md5.new()
                    m.update(pwd)
                    payload[passwd]= m.hexdigest()    

                #r = requests.post(url,data=json.dumps(payload),headers=headers,allow_redirects = False,proxies=proxies)
                try:
                    r = requests.post(url,data=json.dumps(payload),headers=headers,allow_redirects = False)
                except:
                    pass
                else:
                    if r.status_code == int(responsecode) or int(responsecode) == 1: 
                        print 
                        print payload,r.status_code,r.headers['Content-Length']
                    #print payload
                    #print r.status_code,r.headers['Content-Length']
                        #if r.headers['Content-Length'] == int(responselen):
                        if response_partern == '':    
                            sql = 'insert into web_result(username,password,httpbody_id,http_code,http_length) values("%s","%s",%d,"%s","100")' % (username,pwd,1,r.status_code)  
                            cursor.execute(sql)
                            db.commit()
                        elif r.text.find(response_partern) != -1:
                            print r.text,response_partern
                            sql = 'insert into web_result(username,password,httpbody_id,http_code,http_length) values("%s","%s",%d,"%s","100")' % (username,pwd,1,r.status_code)  
                            cursor.execute(sql)
                            db.commit()
                        else:
                            continue
            
            #print r.text
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('id', nargs='+', help='id')
    parser.add_argument('usertype', nargs='+', help='user')
    parser.add_argument('passtype', nargs='+', help='pass')
    parser.add_argument('responsecode',nargs='+',help='http response code')
    parser.add_argument('responselen',nargs='+',help='http response length')
    parser.add_argument('response_partern',nargs='+',help='partern')
    parser.add_argument('password_md5',nargs='+',help='password md5')
    parser.add_argument('httpbody_type',nargs='+',help='keyvalue,json')
    args = parser.parse_args()
   # print args.id,type(args.id)
   # print args.usertype,type(args.usertype)
   # print args.passtype,type(args.passtype)
    getuser(args.usertype[0])
    getpass(args.passtype[0])
    #print user_list
    #print args
    httpbody = getrequest(args.id[0])
   ## print httpbody
   ## print passwd_list
   # #print httpbody[0],type(httpbody[0])
    request = bruteforce(httpbody[0],args.responsecode[0],args.responselen[0],args.response_partern[0],args.password_md5[0],args.httpbody_type[0])
    #print args.password_md5[0]
    
