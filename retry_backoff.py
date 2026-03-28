#!/usr/bin/env python3
"""Retry with exponential backoff and jitter."""
import sys,time,random
def retry(func,max_retries=5,base_delay=0.1,max_delay=30,jitter=True):
    for attempt in range(max_retries+1):
        try: return func()
        except Exception as e:
            if attempt==max_retries: raise
            delay=min(base_delay*(2**attempt),max_delay)
            if jitter: delay*=random.uniform(0.5,1.5)
            print(f"  Attempt {attempt+1} failed: {e}. Retrying in {delay:.2f}s...")
            time.sleep(delay)
def main():
    random.seed(42);fails=[0]
    def unreliable():
        fails[0]+=1
        if fails[0]<=3: raise ConnectionError(f"timeout (attempt {fails[0]})")
        return f"Success after {fails[0]} attempts"
    result=retry(unreliable,max_retries=5,base_delay=0.01)
    print(f"Result: {result}")
if __name__=="__main__": main()
