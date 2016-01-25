#coding:utf-8 
 
import os  
import sys  
import urllib  
from time import time, sleep  
import multiprocessing
 
class RateLimit(object):  
    """Rate limit a url fetch"""  
    def __init__(self, rate_limit):  
        """rate limit in kBytes / second"""  
        self.rate_limit = rate_limit  
        self.start = time()  
    def __call__(self, block_count, block_size, total_size):  
        total_kb = total_size / 1024  
        downloaded_kb = (block_count * block_size) / 1024  
        elapsed_time = time() - self.start  
        if elapsed_time != 0:  
            rate = downloaded_kb / elapsed_time  
            #print "%d kb of %d kb downloaded %f.1 kBytes/s\n" % (downloaded_kb ,total_kb, rate),  
            expected_time = downloaded_kb / self.rate_limit  
            sleep_time = expected_time - elapsed_time  
            #print "Sleep for", sleep_time  
            if sleep_time > 0:  
                sleep(sleep_time)  
 
def main():  
    """Fetch the contents of urls"""  
    if len(sys.argv) != 3:  
        print 'Syntax: %s "rate in kBytes/s" URL ' % sys.argv[0]  
        raise SystemExit(1)  
    rate_limit, url = sys.argv[1:]  
    rate_limit = float(rate_limit)  
    #print "Fetching %r with rate limit %.1f" % (url, rate_limit)  
    urllib.urlretrieve(url,reporthook=RateLimit(rate_limit))  
 
if __name__ == "__main__": 
    start = time()
    pool = multiprocessing.Pool(processes=10)
    for i in xrange(10):
        print "This's %d process" % i 
        pool.apply_async(main)
    pool.close()
    pool.join()
    end = time()
    print str(round(end-start,3))+'s'
