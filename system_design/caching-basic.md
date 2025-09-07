# Caching[[Link](https://neetcode.io/courses/system-design-for-beginners/10)]
- __Client perspective__
    - When a browser need to load resource, it follows a sequece in:
        1. Check the Memory Cache
            - first check browser memory cache
            - used for resources download in the current browsing sessions
        2. Check the Disk Cache
            - then check this if not in memory cache
            - a more presistent cache that contains resources from sites visited in the past
        3. Network Request
            - if neither in 1 nor 2
            - browser makes a request to the server hosting the resources
        - Cache Hit: cached file is found
        - Cache Miss: cached file is not found
- __Cache Ratio:__
    - formula: no. cache hit / (no. cache hit + no. cache miss)
    - this ratio is important for CDNs (Content Delivery Networks)
- __Server Perspective__
    - Scenario: create tweet & get tweet cycle, and only a minor proportion of tweets really go viral, typically posted by public figures or celebrities, 
    - The bulk of content creators won't see much engagement on their posts
    - Cache modes can be:
        - Write-around chache:
            - When new tweet is posted, it written directly to the main page (disk/database) rather than chache (redis)
            - Twitter will sace cache space for more popular content that is accessed more frequently
        - Write-through cache:
            - Each new tweet is posted, it would be written to both main storage and the cache and is readily avaible in both location
            - Avoid stale data and data inconsistency
            - But this might put more load on the memory bus, filling cache up with data that might not be accessed again
        - Write-back cache
            - Only write data to the cache intially
            - Data is written into the cache every time a change occurs but to the disk only when cache is full
            - Cache data can be written to the disk when the system less busy
- __Eviction Policies__
    - A system that determines which item get removed from the cache when the cache is full and new items need to be added
    - FIFO (First In First Out)
        - Similar to queue interface
        - When cache is full, the first piece of data is evicted first
    - LRU (Least Recently Used)
        - Concept: if an item has not been accessed for a long time, it is less likely to be accessed in the future as well
        - Would be particularly useful if there were a single person with a really popular tweet, as we wouldn't want that tweet to be removed from the cache
    - LFU
        - It assumes that if an item is not accessed frequently, it is unlikely to be access frequently in the future as well
        - Can be implemented using key-value pair
        - Limitiation when applied to Twitter, for example:
            - tweets from 2013 have a large number of views might never evicted due to its huge number of frequency
            - LRU cache is better for Twitter
        - Real world use case for LFU cache:
            - Image or **Font Caching in Web Browsers** or Rendering Engines
                - Browsers render fonts, SVGs, or images repeatedly.
                - **Fonts/images that are used often (like site logos or common fonts) stay cached.**

# CDNs (Content Delivery Network)[[Link](https://neetcode.io/courses/system-design-for-beginners/11)]
- A group of cache servers (or edge servers) that are located around the world so they can cache content close to end users
- Using CDN, data can be accessed faster than fetching it from the origin server.
- Caching and CDNs are closely related because:
    - Behind CDN is to store copies of a website's content on multiple servers in different geographical locations
    - Speeds up content delivery
    - Reduces the load on the original server and the amount of data that has to be transmitted over a long distance
    - CDN store static content, including:
        - HTML, CSS, static JavaScript files
        - images (etc..)
- __Push CDN__
    - Well-suited for websites where the content is static and doesn't change frequently
    - Once new data is added to the origin server, it is immediately pushed to all of the cache servers
    - Note: the content needs to be widely requested for a push CDN to be efficient
        - they can be inefficient if the content isn't requested by user near those servers.
    - Example:
        ```text
        A good example of a suitable use case for push CDNs is websites that host video content consumed around the globe. 
        Push CDNs offer an advantage in that users don't have to wait for the content to be transferred from the original server to 
        the CDN.
        ```
        - each user request will result in cache hit since the data has already been copied over

- __Pull CDN__
    - If the data that client or user is trying to access does not exist on the CDN:
        - the cache server will be checked first
        - cache server will retrive the data from the origin server and cache it (for this specific CDN) for future requests if the data is not found in local cache server
    - This operation pull the content from the origin server on an 'as needed' based.
    - Websites like Twitter are ideal candidates for a pull CDN due to enormous amount of content genrated every second
        - would be a significant burden for twitter team to proactively push all that content to the CDN

# Supplements
![img](./img/Screenshot%202025-09-07%20103340.png)

__Client Cache:__
- Caches can be located on the client side (OS or browser), server side, or in a distinct cache layer.

__CDN Cache:__
- CDNs are considered a type of cache.

__Web Server Caching:__
- Reverse proxies and caches such as `Varnish` can serve static and dynamic content directly. Web servers can also cache requests, returning responses without having to contact application servers.

__Database Caching:__
- Your database usually includes some level of caching in a default configuration, optimized for a generic use case. Tweaking these settings for specific usage patterns can further boost performance.

__Application Caching__
- Memcached and Redis are in-memory cache.
    - Key-value store
    - Between Application and data storage
    - Data is held in RAM
        - much faster than typical databases where data is stored on disk
- Redis has the following additional features
    - Persistence options
    - Built-in data structure such as sorted set and lists
- There are multiple levels you can cache that fall into two general categroies:
    - Database queries
        - Row Level
        - Query Level
    - Objects:
        - Fully-formed serializable objects
        - Fully-rendered HTML

__Caching at databse query level__
- Whenever you query the database, hash the query as a key and store the result to the cache. This approach suffers from expiration issues:
    - Hard to delete a cached result with complex queries
    - If one piece of data changes such as a table cell, you need to delete all cached queries that might include the changed cell

__Caching at the object level__
- See your data as an object, similar to what you do with your application code. Have your application assemble the dataset from the database into a class instance or a data structure(s):
    - Remove the object from cache if its underlying data has changed
    - Allows for asynchronous processing: workers assemble objects by consuming the latest cached object
- Suggestions of what to cache:
    - User sesions
    - Fully rendered web pages
    - Activity streams
    - User graph data

__Different Cache Design Pattern:__
- [Cache-aside](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#cache-aside)
    - "Cache-aside" (also called lazy loading) is a common caching pattern where the application code manages what gets loaded into and invalidated from the cache.
    1. Read request
        - The app first checks the cache (e.g., Redis) to see if the data is there.
        - If the data is found (cache hit), it’s returned immediately.
        - If the data is missing (cache miss), the app loads it from the database (or other backing store), then stores it in the cache before returning it.
    2. Write request
        - On updates or inserts, the app writes directly to the database.
        - Then it invalidates or updates the corresponding cache entry so future reads don’t return stale data.
    - Disadvantage
        - Each cache miss results in three trips, which can cause a noticeable delay.
        - Data can become stale if it is updated in the database. This issue is mitigated by setting a time-to-live (TTL) which forces an update of the cache entry, or by using write-through.
        - When a node fails, it is replaced by a new, empty node, increasing latency.

- [Write-through](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#write-through)
    - Read:
        - App checks cache first
        - If cache hit -> return data
        - If cache miss -> load from DB -> store it in cache -> return it
    - Write/Update:
        - App writes the data to the database
        - Simultaneously (or immediately after), the same data is written to the cache
    - Write-through is a slow overall operation due to the write operation, but subsequent reads of just written data are fast
        - Users are genrally more tolerant of latency when updating data than reading data
        - Data in the cache is not stale in this method
    - Disadvantages:
        - Most data written might never get read, which can be minimized with a TTL
        - May waste memory if a lot of rarely-read data is cached.
        - When a new node is created due to failure or scaling, the new node will not cache entries until the entry is updated in the database. Cache-aside in conjunction with write through can mitigate this issue.

- [Write-behine (write-back)](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#write-behind-write-back)
    - Read:
        - Same as cache-aside or write-through: check cache first, if miss → load from DB, store in cache, return.
    - Write/Update:
        - App updates cache only.
        - Cache eventually (periodically or via a queue) writes changes to the DB asynchronously.
    - Pros:
        - Fast writes
        - Reduces databse load
        - Great for write-heavy workloads where slightly deplayed persistence is acceptable
    - Cons:
        - Risk of data loss if the cache node fails before flushing to DB
        - DB might temporaliy be out of sync(eventual consistency).
        - More complex to implement correctly(requires queues, durability guarantees, retries, etc.).
- [Refresh-ahead](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#refresh-ahead)
    - Refresh-ahead (sometimes called refresh-ahead caching or proactive caching) is a pattern where the cache refreshes entries before they expire, so users don’t experience a cache miss.
    - Instead of waiting for TTL to expire and the next request to reload from the DB, the system refreshes the cache in advance.
    - Configure the cache to automatically refresh recently access cache entry prior to its expirations
    - Can result in reduced latency vs read-through if the caceh can accuratly predict which items are likely to be needed in the future
    - Read:
        - App checks cache
        - If hit -> return data
        - If miss -> load from DB, store in cache
    - Refresh:
        - Each cache entry has a TTL
        - Before expiration, a background job proactively reloads the data fron the DB and updates the cache
        - So when next request comes, the cache is already "warm"
    - Pros:
        - Reduces cache miss penalty (no slow request hitting DB after expiry).
        - Provides consistently low latency for read-heavy workloads.
        - Works well for predictable access patterns (e.g., hot items frequently requested).
    - Cons:
        - Can waste resources if refreshed entries are never accessed again.
        - Adds complexity (needs background refresh jobs, or cache systems with refresh support).
        - Might increase DB load if you refresh aggressively.
        - Need to make application changes such as adding Redis or memcached.