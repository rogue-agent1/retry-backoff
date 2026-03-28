#!/usr/bin/env python3
"""retry_backoff - Retry with exponential backoff."""
import sys,time,random
def retry(fn,max_retries=5,base_delay=1,max_delay=60,backoff=2,jitter=True):
    for attempt in range(max_retries+1):
        try:return fn()
        except Exception as e:
            if attempt==max_retries:raise
            delay=min(base_delay*(backoff**attempt),max_delay)
            if jitter:delay*=random.uniform(0.5,1.5)
            print(f"  Attempt {attempt+1} failed: {e}, retrying in {delay:.1f}s")
            time.sleep(delay)
def with_timeout(fn,timeout):
    import threading
    result=[None];error=[None];done=threading.Event()
    def wrapper():
        try:result[0]=fn()
        except Exception as e:error[0]=e
        done.set()
    t=threading.Thread(target=wrapper);t.start();done.wait(timeout)
    if not done.is_set():raise TimeoutError(f"Timed out after {timeout}s")
    if error[0]:raise error[0]
    return result[0]
if __name__=="__main__":
    attempts=[0]
    def flaky():
        attempts[0]+=1
        if attempts[0]<4:raise ConnectionError(f"Attempt {attempts[0]} failed")
        return "Success!"
    result=retry(flaky,max_retries=5,base_delay=0.1)
    print(f"Result: {result} after {attempts[0]} attempts")
