### Overview

- Store key-value pairs in memory.
- Each key can have a TTL (time-to-live).
- After expiration, the key should not be retrievable.
- Support typical operations: put(key, value, ttl), get(key), delete(key).
- Discuss thread-safety, scalability, and cleanup strategy.

# Functional Requirements:

- Insert a key-value pair with TTL.
- Fetch a key (return value if valid & not expired).
- Delete a key.
- Update value or TTL for existing key.

# Non-Functional Requirements:

- O(1) average time complexity for get and put.
- Efficient cleanup of expired keys.
- Thread-safe (multiple readers/writers).
- Memory-efficient (avoid memory leak with expired keys).

# Strategies

1. Lazy Deletion:

- whenever a key is being fetched, if TTL is passed delete it
- not memory efficient, as keys continue to be present even after TTL
- fast

2. Proactive Deletion:

- run a background thread
- maintain priority_queue or min_heap to delete passed TTL entries
- memory efficient, but overhead is there
