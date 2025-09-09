import threading
import time
import heapq

def current_millis():
    return int(time.time() * 1000)

class InMemoryKVStore:
    def __init__(self, cleanup_interval = 1):
        self.store = {} # key -> {value, expiryTime}
        self.min_heap = [] # [(expiry_time, key)]
        self.lock = threading.Lock()
        self.cleanup_interval = cleanup_interval
        self.running = True

        # Start background cleanup thread
        self.cleanup_thread = threading.Thread(target=self._background_cleanup, daemon=True)
        self.cleanup_thread.start()


    def put(self, key: str, value: str, ttl: int):
        # O (log N) due to heap
        expiry_time = current_millis() + ttl
        with self.lock:
            self.store[key] = (value, expiry_time)
            heapq.heappush(self.min_heap, (expiry_time, key))


    def get(self, key: str) -> str | None:
        # O(1)
        with self.lock:
            if key not in self.store:
                return None
            value, expiry = self.store[key]
            if expiry < current_millis():
                del self.store[key]
                return None
            return value
        
    
    def delete(self, key: str):
        with self.lock:
            if key in self.store:
                del self.store[key]

    
    def _background_cleanup(self):
        while self.running:
            self.cleanup()
            time.sleep(self.cleanup_interval)


    def cleanup(self):
        # Background thread calls this
        with self.lock:
            while self.min_heap and self.min_heap[0][0] < current_millis():
                _, key = heapq.heappop(self.min_heap)
                if key in self.store and self.store[key][1] < current_millis():
                    del self.store[key]

    
    def stop(self):
        self.running = False
        self.cleanup_thread.join()


# ------------------- TEST CASE -------------------
if __name__ == "__main__":
    kv = InMemoryKVStore()

    print("Putting key1=hello with TTL=2000ms")
    kv.put("key1", "hello", 2000)

    print("Get key1 immediately:", kv.get("key1"))  # should print "hello"

    time.sleep(1)
    print("Get key1 after 1 second:", kv.get("key1"))  # still "hello"

    time.sleep(2)
    print("Get key1 after 3 seconds:", kv.get("key1"))  # should be None (expired)

    kv.stop()
