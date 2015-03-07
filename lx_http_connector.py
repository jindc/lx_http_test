import threading
import logging
from datetime import datetime
import time
import socket
import urllib
from urllib import request
from urllib.error import  URLError, HTTPError
import lx_test_statistic
from lx_test_statistic import statistic_add,ok_flag,http_eflag,url_eflag,other_eflag
from lx_test_statistic import run_times,total_run_times,ok_times,http_error_times,url_error_times,other_error_times,result_map

class http_connector(threading.Thread):

    urls =["http://host:port/index.html",
           "http://host:port/test.html",
           "http://host:port/notexist.html"
            ]
    def __init__(self,run_time=None):
        super(http_connector,self).__init__()
        logging.debug('connector init')
        self.run_flag = True;
        if run_time is not None:
            self.run_time = run_time
    
    def run(self):
        logging.debug('connector call,run_time %d' % self.run_time)
        stop_time = time.time() + self.run_time
        timeout = 10
        socket.setdefaulttimeout(timeout)

        while True:
            for url in self.urls:
                try:
                    req = urllib.request.Request(url) 
                    resp = urllib.request.urlopen(req)
                    data = resp.read()
                    #print(data)
                    statistic_add(ok_flag,url,200)
                    logging.info('request ok .url:%s data len:%d' % (url, len(data) ) )
                except HTTPError as e:
                    statistic_add(http_eflag,url,e.code)
                    logging.error("request http error:%d url:%s,ecode:%d" % (threading.get_ident(),url,e.code) )
                except URLError as e:
                    statistic_add(url_eflag,url,url_eflag)
                    logging.error('request url error:%d url:%s,emsg:%s' %(threading.get_ident(),url,e.reason ) )
                except Exception as e:
                    statistic_add(other_eflag,url,other_eflag)
                    logging.error('request unexcept error:%d url:%s,emsg:%s' % (threading.get_ident(),url, e ) )
                
                if lx_test_statistic.run_times > 0 :
                    if lx_test_statistic.total_run_times >= lx_test_statistic.run_times:break
                elif time.time() >= stop_time:break
            
            if lx_test_statistic.run_times > 0 :
                if lx_test_statistic.total_run_times >= lx_test_statistic.run_times:break
            elif time.time() >= stop_time:break

        logging.debug("thread %d run over" %(threading.get_ident() ))
        self.run_flag = False

