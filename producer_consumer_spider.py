import queue
import blog_spider
import time
import random
import threading

#爬取获得页面源码--生产者
def do_craw(json_queue:queue.Queue, html_queue:queue.Queue):
    while True:
        json = json_queue.get()
        html = blog_spider.craw(json)
        html_queue.put(html)
        
        print(threading.currentThread().name,f"craw {json}",
             "json_queue.size=",json_queue.qsize())
        time.sleep(random.randint(1,2))

#解析--消费者
def do_parse(html_queue:queue.Queue, fout):
    while True:
        html = html_queue.get()
        results = blog_spider.parse(html)
        for result in results:
            fout.write(str(result) + '\n')
        
        print(threading.currentThread().name,f"results.size",len(results),
              "json_queue.size=",json_queue.qsize())
        
        time.sleep(random.randint(1,2))

if __name__ == "__main__":

    json_queue = queue.Queue()
    html_queue = queue.Queue()
    
    for json in blog_spider.json_list:
        json_queue.put(json)

    for idx in range(20):
        t = threading.Thread(target=do_craw,args=(json_queue,html_queue),
                            name = f"craw{idx}")
        t.start()
    
    fout = open("data.txt",'w',encoding='utf-8')
    
    for idx in range(20):
        t = threading.Thread(target=do_parse,args=(html_queue,fout),
                            name=f"parse{idx}")
        t.start()