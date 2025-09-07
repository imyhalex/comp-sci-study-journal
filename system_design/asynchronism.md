# Asynchronism[[Link](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#asynchronism)]

![img](./img/Screenshot%202025-09-07%20114900.png)

Asynchronous workflows help reduce request time for expensive operations taht would otherwise be performed in-line. They can also help by doing time-consuming work in advance, such as periodic aggregation of data.

__Message Queues__
- Receive, hold, and deliver messages. If an operation is too slow to perform inline, we can use message queue with the following workflow
    - An application publishes a job to the queue, then notifies the user of job status
    - A worker picks up the job from the queue, processes it, then signals the job is complete
- The user is not blocked and the job is processed in the background
- During this time, the client might optionally do a small amount of processing to make it seems like the task has completed.
    - example: posting a tweet, the tweet could be instantly posted to your timeline, but it could take some time before you tweet is actually delivered to all your followers.
- `Redis` is useful as a simle message broker (A message broker is software that helps different applications or services communicate with each other by exchanging messages in a reliable, decoupled way.) but message can be lost
- `RabbitMQ`: is popular but requires you to adapt to the 'AMQP' protocol and manage your own nodes.
- `Amazon SQS`: is hosted but can have high latency and has the possibility of messages being delivered twice.

__Task Queue__
- Receives taks and their related data, run them, then delivers their results
- Can support scheduling and can be used computationally-intensive jobs in the background.
- `Celery` has support for scheduling and primarily has python support

__Back Pressure__
- If queues start to grow significantly, the queue size can become larger than memory, resulting in cache misses, disk reads, and even slower performance.
    - Back pressure can help by limiting the queue size, thereby maintaining a high throughput rate and good response times for jobs already in the queue.
    - Once the queue fills up, clients get a server busy or HTTP 503 status code to try again later. 
    -  Clients can retry the request at a later time, perhaps with exponential backoff.

__Cons for asynchronism__
- Use cases such as inexpensive calculations and realtime workflows might be better suited for synchronous operations, as introducing queues can add delays and complexity.