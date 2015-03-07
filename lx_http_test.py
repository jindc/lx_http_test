"""Test http performance by multithread
"""
import argparse
import sys
import logging
import threading
import time
from time import strftime,localtime
from lx_http_connector import http_connector
import lx_test_statistic
from lx_test_statistic import total_run_times,ok_times,http_error_times,url_error_times,other_error_times,result_map
from lx_test_statistic import ok_flag,http_eflag,url_eflag,other_eflag

def main():
    print("Welcome to use LanXin Http Test Suit")
    
    parser = argparse.ArgumentParser(description = "LanXin Http Test Suit")
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-t","--run_time", action="store",default=60,type=int,help="the time that the test suit to run(unit:second)")
    group.add_argument("-n","--run_times",action="store", type=int, help="the total times that the test suit to run")
    
    parser.add_argument("--thread_num",action="store",type=int,default=3, help="run thread number")
    parser.add_argument("--log_file",action="store", help="record log ,if not set,the log will print to standard output")
    parser.add_argument("--version" ,action="version",version="%(prog)s 1.0")

    args = parser.parse_args(sys.argv[1:])
    print(args)

    loglevel = logging.DEBUG
    logger = logging.getLogger()
    logger.setLevel(loglevel)
    
    if args.log_file:
        ch = logging.FileHandler(args.log_file)
    else:    
        ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    format = logging.Formatter('%(asctime)s_%(levelname)s_%(module)s: %(message)s')
    ch.setFormatter(format)
    logger.addHandler(ch)
    logger.debug('lx http test suit init ok')
    
    lx_test_statistic.start_time = time.time()
    if args.run_times:
        lx_test_statistic.run_times=args.run_times

    works = [] 
    for i in range(args.thread_num):
        connector = http_connector(args.run_time)
        connector.start()
        logging.debug('work thread %d start' % connector.ident)
        works.append(connector)
   
    for work in works:
        while work.run_flag:
            time.sleep(1)
    #while threading.active_count() > 1:
    #    time.sleep(1)
    
    lx_test_statistic.end_time = time.time()
    time_format = '%Y-%m-%d %H:%M:%S'
    logging.info('start at %s,end at %s,run time:%f second,time_per_request:%f millisecond' 
                %( strftime(time_format,localtime(lx_test_statistic.start_time)) ,
                   strftime(time_format,localtime(lx_test_statistic.end_time)),
                   lx_test_statistic.end_time - lx_test_statistic.start_time,
                   (lx_test_statistic.end_time - lx_test_statistic.start_time)/lx_test_statistic.total_run_times*1000 ))

    logging.info("ok_flag:%d http_eflag:%d url_eflag:%d other_eflag:%d" 
            % (ok_flag,http_eflag,url_eflag,other_eflag) )

    logging.info('total_run_times:%d ok_times:%d http_error_times:%d url_error_times:%d other_error_times:%d'
           % (lx_test_statistic.total_run_times,
              lx_test_statistic.ok_times,
              lx_test_statistic.http_error_times,
              lx_test_statistic.url_error_times,
              lx_test_statistic.other_error_times))
    logging.info('result map:%s' % result_map)
    
    print("work done")

if __name__ == '__main__':
    main()
