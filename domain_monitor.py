#import os
#import MySQLdb
#db = MySQLdb.connect("127.0.0.1", "root", "Mljrsecewq", "secpassword", charset='utf8',port=3307 )
#cursor = db.cursor()
#
#mljr_domain_path = "/opt/soft/ansible-playbook/nginx-111-112/files/vhosts/mljr.com" 
#for dir,folder,file in os.walk(mljr_domain_path):
#    for domain in file:
#        subdomain = domain[0:domain.find(".conf")] + "mljr.com"
#        sql = "SELECT * FROM domain WHERE  domain =  '%s'" % (subdomain) 
#        cursor.execute(sql)
#        results = cursor.fetchall()
#        if not results:
#            cursor.execute("insert into domain(domain,flag) values('%s','%s')" % (domain[0:domain.find(".conf")]+ '.mljr.com','1'))
#            db.commit()
#yyfq_domain_path = "/opt/soft/ansible-playbook/nginx-111-112/files/vhosts/yyfq.com" 
#
#for dir,folder,file in os.walk(yyfq_domain_path):
#    for domain in file:
#        print domain[0:domain.find(".conf")] + ".yyfq.com"
#        subdomain = domain[0:domain.find(".conf")] + ".yyfq.com"
#        sql = "SELECT * FROM domain WHERE  domain =  '%s'" % (subdomain)
#        cursor.execute(sql)
#        results = cursor.fetchall()
#        if not results:
#            cursor.execute("insert into domain(domain,flag) values('%s','%s')" % (subdomain,'1'))
#
#mlcjr_domain_path = "/opt/soft/ansible-playbook/nginx-111-112/files/vhosts/mlcjr.com" 
#for dir,folder,file in os.walk(mlcjr_domain_path):
#    for domain in file:
#        print domain[0:domain.find(".conf")] + ".mlcjr.com"
#        subdomain = domain[0:domain.find(".conf")] + ".mlcjr.com"
#        sql = "SELECT * FROM domain WHERE  domain =  '%s'" % (subdomain)
#        cursor.execute(sql)
#        results = cursor.fetchall()
#        if not results:
#            cursor.execute("insert into domain(domain,flag) values('%s','%s')" % (subdomain,'1'))
#


import re,git
import sys
import os,os.path
import MySQLdb
import time
import requests
from sendmail import SendEmail
from sqlalchemy import Column, String, create_engine,Sequence,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from base64 import b64decode,b64encode


db = MySQLdb.connect("127.0.0.1", "root", "Mljrsecewq", "secpassword", charset='utf8',port=3307 )
db.autocommit(1) 
cursor = db.cursor()
mljr_path = "/opt/soft/ansible-playbook/nginx-111-112/files/vhosts/mljr.com"
yyfq_path = "/opt/soft/ansible-playbook/nginx-111-112/files/vhosts/yyfq.com" 
mlcjr_path = "/opt/soft/ansible-playbook/nginx-111-112/files/vhosts/mlcjr.com" 

g = git.cmd.Git("/opt/soft/ansible-playbook/nginx-111-112/")
g.pull()

#pathlist = os.listdir(path)
def get_domain(path):
    
    for root,dirs,files in os.walk(path):
        for file in files:
            if file.endswith("conf"):
                with open(os.path.join(root,file),"r") as f:
                    for line in f:
                        if line.strip().startswith("server_name "):
                            for i in line.strip().split():
                                if (i.find("mljr.com") != -1  or i.find("yyfq.com") != -1 or i.find("mlcjr.com") != -1):
                                    sql = "select domain  from domain_table where domain =  '%s'" % (i.strip(';'))
                    
                                    cursor.execute(sql)
                                    results = cursor.fetchall()
                                #print results
                                    for result in results:
                                        print result
                                        domain = result[0].encode("utf8")
                                        sql = 'update domain_table set flag=0 where domain="{domain}" and flag=2'.format(domain=domain);
    #                                print sql
                                        cursor.execute(sql)
                                    
                                        db.commit()
                                    if not results:
                                        sql = 'insert into domain_table(domain,flag)  values("{domain}",1)'.format(domain=i.strip(';'))
                                        cursor.execute(sql)
                                        db.commit()
def sendmail(domain_list):
    send = SendEmail()
    domain = b64encode(",".join(domain_list))
    print domain,b64decode(domain)
    sub = b64decode('W+mAmuefpV3mnInmlrDnmoTlpJbnvZHln5/lkI3kuIrnur8=')
    content =  b64decode("5Y+R546w5paw55qE5aSW572R5Z+f5ZCNOg==") + b64decode(domain)
    
    print content
    send.send_mail(['zunkui.mou@mljr.com'],sub,content)


def sendding(domain_list):
    domain = b64encode(",".join(domain_list))
    print domain,b64decode(domain)
    text ={
    "users": [
        {   
            "username": "zunkui.mou",
        },
    ],
 "dingtalk": {
        "msg": {
            "msgtype": "text",
            "text":{
           "content":b64decode("5Y+R546w5paw55qE5aSW572R5Z+f5ZCNOg==")+b64decode(domain)
        }
    },
    "n_type": "mljr"
    }
}

    headers ={
    "content-type":"application/json"
}

    req = requests.post(url = "http://vctube.op.mljr.com/notice/message?access_key_id=9ZqH73guJvndwON7ohdaFqUhnY5GBNpYw3CW3Mtv",
                headers = headers,
               json = text)

def domain():
    cursor.execute("update domain_table  set flag = 2 where flag = 0")
    db.commit()
    get_domain(mljr_path)
    get_domain(yyfq_path)
    get_domain(mlcjr_path)
    cursor.execute("delete from domain_table where flag=2")
    db.commit()
    sql = "select domain  from domain_table where flag=1"
    cursor.execute(sql)
    results = cursor.fetchall()
    print list(results)
    if results:
        domain_list = []
        for i in results:
            domain_list.append(i[0])
        print domain_list
        sendmail(domain_list)
        sendding(domain_list)
    


if __name__ == '__main__':
    domain()
    db.close()
