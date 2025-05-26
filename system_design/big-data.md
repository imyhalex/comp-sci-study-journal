# Message Queues[[Link](https://neetcode.io/courses/system-design-for-beginners/19)]
- Offers solution where an application server faces a high volume of requests that it can't process simultaneously.
    - why not scale server horizontally or vertically?
        - bcs not always cost-effective or pratical
        - also include instances where immediate processing of these requests isn't necessary, allowing them to be queued for later handling
- Serve to decouple producers (app event) and consumers (application servers), functioning as a buffer for managing surges in data
- Example: Payment processing
    - Handling Peaks in Load
        - During high usage periods, such as a major sale, the number of payment requests typically increases significantly.
            - if requests processed synchronously, it could result in a poor user experience due to prolonged wait times and potential timeouts
            - payments can be stored and processed asynchronously
    - Decoupling Services
        - when a new order is paced, a message can be published to the queue
        - the payment service, acting as a suubscriber, can then process the payment and update the order staus
- __Push/Pull model__
    - Several methods through which a message queue can interact with the application server
        - Pull-Based Model:
            - the application is responsible for monitering the message queue for any new messages
                - if new messages are present and the app server has the capacity, it "pulls" from the queue
            - This approach can be more efficient in terms of managing the server-side load
            - But it introduce latency if the queue is empty
        - Push-Based Model:
            - Queue takes on the responsibility of pushing messages to the server
            - But might overload the server if the rate of incoming messages is excessively high
    - When the message queue dispatches a message to the applicaiton server
        - the consumer or the server sends an acknowledgement after successfully processing a message
        - if not receive an acknowledgement for a message within a specific timeframe
            - it infer the message was not processed, prompting the queue to resend it
    - This approcah ensures message delivery even in the event of temporary server issues
- __Pub/Sub model__
    - Publisher/subsciber model provides decoupling of publisher and subscribers, eliminating the need for either to be aware of each other's existence
        - allows for easy system scalability and ensures messages are not lost if a subscriber is temporarily unable to process them
    - Pub/sub goes through the following steps:
        1. Pub dispatches messages to a specific queue or topic
        2. One or more sub listen to the specific queue or topic
        3. The message broker ensures all message published to a topic successfully delivered to all subscribers of that topic. Subscribers process message independently and their own pace
    - A "topic" is a category or label that serves as a conduit for similar message
    - In the context of pub/sub model:
        - publishers dispatch their messages to specific topics, and subscribers indicate their interest by subscribing to these topics. 
    - Can have multiple subscribers subscribing to the same topic
        ```text
        In our payment example, an "OrderPlaced" topic could have multiple subscribers such as the Inventory Service (updating 
        the stock level) and a Billing Service (which charges the customer). All these subscribers need to be notified when an 
        order is placed.
        ```
    - One more benefit: can introduce a completely different API as a subscriber without needing to alter pub/sub architecture
# MapReduce[[Link](https://neetcode.io/courses/system-design-for-beginners/20)]
- Pertains to big data processing, enabling the handling of extensive amounts of data, perform computation, and produce the result
- A programming model deal with a specific implementation designed specifically for processing and generating large datasets
    - beneficial for distributed computing on vast sets of data soanning terabytes or even petabytes
- Two common methods how to process data
    - __Batch Processing__
        - data is processd in substantial groups
        - all data is accumulated over a specific period and subsequently processed as a unit
        - A practical example would be counting the frequency of each word occurring in a book, or a series of books.
        - dosen't occur in real-time
        - takes place when batch jobs are executed
    - __Stream Processing__
        - involves processing data in real-time as it is received
        - instead of being stored, data is processed individually in it raw, unbatched form
        - example:
            - redacting a customer's credit card expiration date or last name upon payment. This task cannot be performed in a batch and must be done in real-time, since this information needs to be immediately updated for subsequent operations.
- __Function and Implementation__
    - Framework such as Apache Hadoop, the system typically consist of one "master" node and mutliple "worker" nodes
        - `Master Node:`
            - tasked with managing the distribution of the MapReduce job accross the worker nodes
            - keeps an eye on the status of each task and re-assigns task if any failure occur
        - `Worker Node:`
            - nodes that processing data
            - masted node assigns each worker node a portion of the data and a copy of MapReduce program
        - `Map Phase`
            - each worker nodes execute the Map operation on its assigned data portion
            - entail mapping each word to a key-value pair where the key is the word, and the value is frequency of the word
        - `Shuffle and Sort Phase`
            - worker node reorganize the key-value pairs so that all values associated with the same key are grouped together
            - This process is known as the shuffle and sort phase. So, for instance, given the word "The", if worker 1 processed 3 occurrences, worker 2 processed 7, and worker 3 processed 100, these would be grouped together during this phase.
        - `Reduce Phase`
            - is performed on each group of values, producing a final count for each word.
            - this result is then written to some form of sotrage or database
- Note:
    - It does come with limitaions:
        - restrictive data processing model
        - works well with data that fits into the Map and Reduce steps
            - for data processing task that don't align with this model, alternative models may prove to be more suitable