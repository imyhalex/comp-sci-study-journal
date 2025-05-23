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