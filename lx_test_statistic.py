import threading
import logging

slock = threading.Lock()

start_time=0.0
end_time=0.0

run_times=0

total_run_times=0
ok_times=0
http_error_times=0
url_error_times=0
other_error_times=0
result_map = {}

ok_flag=0
http_eflag=1
url_eflag=2
other_eflag=3

def statistic_add(flag,url,code):
    global total_run_times,ok_times,http_error_times,url_error_times,other_error_times,result_map

    slock.acquire()
    total_run_times = total_run_times + 1
    if flag == ok_flag:
        ok_times+=1
    elif flag == http_eflag:
        http_error_times+=1
    elif flag == url_eflag:
        url_error_times+=1
    else:
        other_error_times+=1

    temp_map = {}
    if url in result_map:
        temp_map = result_map[url]
    else:
        result_map[url] = temp_map

    if code in temp_map:
        temp_map[code]+=1
    else:
        temp_map[code]=1
        
    slock.release()

