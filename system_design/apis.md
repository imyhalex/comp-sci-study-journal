# HTTP(Hypertext Transfer Protocol)[[Link](https://neetcode.io/courses/system-design-for-beginners/6)]
- __Client-Server Model__:
    - `Client`:
        - Is an application or system that access a service made available by a server
        - It can be:
            - a web browser
            - an emai software
            - an app on phone
            - any other software that needs to access some service
        - The term "client" also refer to the device running this application
    - `Server`:
        - A computer, device, or software that provide resources, data, services, or functionality to the client or other servers on a network
        - Wait for incoming request from clients and respond by fufilling those requests
            ```text
            e,g.: a web server delivers web pages to clients, an email server handles sending and receiving emails, and a database server provides clients with access 
            to database services.
            ```
    - The role of client and server can interchange
- __PRCs(Remote Procedure Call)__
    - Provides the ability for a program to perform functions on a separate machine
        - making it a simple and efficient solution for task management in distributed systems
            ```text
            Consider a practical scenario: suppose we input "NeetCode" into the YouTube search bar, upon which the browser displays a 
            list of all the NeetCode videos. The code responsible for this listing operation doesn't reside within our browser. This is 
            because the browser isn't where the videos are stored; instead, this code is situated on YouTube's servers. The 
            operation may utilize a function such as listVideos('neetcode'). Even though it may seem as if the code is 
            executing on the client side, it is actually making a call to YouTube's servers in the background to retrieve the relevant 
            information.
            ```
- __HTTP__
    - Built on top of IP and TCP
    - TCP built on top if IP, and HTTP sits on top of TCP
    - It is a request/response protocol
    - It is a set of rules for how data should be formatted and transmitted over the web
    - Is used every time when make a call through the browser
    - `Anatomy of an HTTP request`:
        - Request Method: 
            - Indicates the desired action to be performed on the provided resource, for example:
                - GET: retrive
                - POST: submite data to be processed by the resource
                - PUT: update
                - DELTE
        - Request URL/URI:
            - The URL which specifies where the request should be made
                - As notice, it also contains the path `/result` with a parameter using `?search_query=neetcode`
                    - `?search_query=neetcode`: reflects what we typed into the search box
        - Headers:
            - Provide additional information about the request, these can be:
                - HTTP Request Headers:
                    - Provide the requisite information about the request indicating the method, the scheme, and the types of data the client can accept
                - HTTP Response Headers:
                    - Supplies additional information about the response or the server
                    - Also set cookies, specific caching behavior, and content-type
        - Body:
            - Not every HTTP request contains a body
                - GET request don't because they are not sending any data over
                - POST or PUT, the body contains data
            
    - `HTTP Methods`:
        - GET
            - retrives a resource
            - idempotent:
                - making same request multiple times should always return the same result
        - POST
            - send data to the server to create new resource
            - will have a request body (playload) which indicates the data being sent over the internet
                - this playload not passed as part of the URL to prevent Man in the middle attacks
            - this method is not idempotent 
        - PUT
            - updatea a resource
            - an important charateristic of PUT: if the same update operation is performed muiltiple times using the same data, the sate of the resource will remain unchanged
                - which is idempotent, updating same data repeatly would result the same state
        - DELTE
            - delete specific data
            - it is idempotent
            - the first call may return 200 status code (OK), and any additional delete calls will return 404 (not found)
                - response might different but there is not change of state
    - `HTTP Status Code`:
        - Informatoin responses (100-199):
            - Are utilized to acknowledge the client's reqeust has been received and is currently being processed
                - 100 Continue: everything is inorder so far
                - 101 Switch Protocols: the server is switching to a different protocol as specified in the upgrade request header received from the client.
        - Successful responses (200-299):
            - 200 OK: indicates that the request has succeeded. 
            - 201 Created: This response code indicates that the request has succeeded, resulting in the creation of a new resource. 
                - Typically sent after POST or PUT request
        - Redirection Messages (300-399):
            - Are used when the requested resource has been assigned a new permanet URL or is temporaily available at a different URL
                - 300 Multiple Choices: he request has more than one possible response. The client should choose one of them.
                - 301 Moved Permanently: means that the requested resource has been permanently moved to a new location, and the server is redirecting the client to this new location.
        - Client error responses (400-499):
            - 400 Bad Request:This response code is used when the server encounters a client request that is invalid or cannot be understood. It often occurs when incorrect parameters are passed in the request, leading to a bad request.
            - 401 Unauthorized: This response code is returned when a client attempts to access a protected resource without proper authentication or authorization.  For example, if you try to delete a video that you are not authorized to delete, the server will respond with a 401 Unauthorized status code.
        - Server error responses (500 - 599)
            - indicates an error has occurred on the server side while processing the client's request.
            - generally indicates issues or failures within the server that prevented it from fulfilling the request.
- __SSL/SLT__
    - Conjucates with HTTPS
    - The reason we need SSL and TLS is because HTTP on its own is vulnerable to man-in-the-middle (MITM) attacks.
    - 'Normal' HTTP requests are analagous to a bag of money in a transparent box
    - Together, TLS and SSL ensure that web data remains inaccessible and unalterable by unauthorized parties.
    - HTTPS is essentially the combination of HTTP with TLS.
    - While SSL is often used interchangeably with TLS, it's worth noting that SSL is technically an outdated term, superseded by TLS.

# WebSockets[[Link](https://neetcode.io/courses/system-design-for-beginners/7)]
- There are multiple application protocol:
    - Those build on top of the TCP:
        - HTTP
        - WebSocket
        - FTP
        - SMTP
        - SSH
    - Those build on top of the UDP
        - WebRTC (for web streaming)

- The problem
    - Consider: building a chat application
        - What if using HTTP?
            - works best when dealing stateless data
                - follows a request-response protocol
            - but: unidirectional and lack real-time communication capabilities
            - client must continually make requests to the server, resulting in significant overhead
                - fetchs messages from server every minute is far from ideal
            - it presents limitaion when it comes to real-time applications
        - What if using WebSocket
            - is a distinct protocol that facilitates two-way commnunication between client and server
                - enabling back-and-forth data transmission
            - this capability highly valuable in scenarios that demand real-time updates, such as:
                - chat application
                - live streaming apps
                - real-time gaming apps
- __Establishing a WebSocket Connection__
    - WebSocket can be seen as an "upgrade" from HTTP in sense that it starts with a standard HTTP request and then transitions to a WebSocket connection if both the client and server support the protocol
    - Major web browswers that have built-in support of WebSocket:
        - Google Chrome
        - Firefox
        - Edge
    - Popular server-side web application frameworks also offer support for WebSocket, such as:
        - Node.js
        - Django
        - ASP.NET
    - Overview for establishing a WebSocket connection
        1. Client Sends a WebSocket Handshake Request:
            - The client will establish a WS connected by initiating a WS handshake
            - This is an HTTP Upgrade request with a few special headers
        2. Server Response (Handshake Response):
            - Return status code 101 if server supports the WS protocol and is willing to accept the connection 
                - 101 indicates the server understands the upgrade header field request and indicates which protocol it is switching to
        3. Data Transfer:
            - The client and server send data between each other in real time after the handshake
            - This is more efficient than constantly opening and closing new HTTP connections
            - WS is truly bidirectional, and this way the client will not have to keep checking the browser
    - By default:
        - WS connections use port 80, similar to HTTP
        - WebSocket Secure (WSS) connections use port 443, similar to HTTPS
    - Important:
        - While devices and browsers may support WebSocket, the network they're connected to must also allow WebSocket connections
        - Some restrictive firewalls might block WebSocket connections but because it so ubiquitous and compatible with existing web infrastructure, it is generally well-supported
        - HTTP/2 allows multiplexing, meaning multiple requests in parallel can be initiated over a single TCP connection
            - But this is not a perfect replacement to WebSocket as they are still very prevalent to this day
    - HTTP/1 -> HTTP/2 -> HTTP/3
        - HTTP/1 & 1.1
            - Released in 1999
            - For multiple requets, queued and requested one at a time
            - Head-of-line blocking
                - can only handle one request at a time, leads to inefficient use of network resource
            - Lack of prioritization
                - did not offer a way to prioritize requests, leads to less critical reources blocking more important ones
            - Plain text headers being sent are large, especially cookies are in use etc...
        - HTTP/2
            - Released in 2015
            - Multiplexing:
                - requests the assets together
            - Header Compression
                - uses HPACK algo to compress request and response headers, reduceing the amout of data transmission
            - Server Push
                - servers can proactively push rerouces to the client's cache before they are requests, reducing latency
            - Stream Prioritiation
                - enables client to proritize request
            - Binary Framing
                - use binary framing leayer to encapsulate messages, make protocol more efficient and less error-prone compared to plain-text approach in HTTP/1.x
        - HTTP/3
            - Does away with TCP, instead utilize a flavor of UDP called Quick UDP Internet Connection (QUIC), which includes benefits:
                - Built-in encrytion
                    - incoporates TLS (transport layer security) 1.3 by default
                    - ensure a secure connection without the need for a separate TLS handshake
                        - reduce latency
                - Reduce head-of-line blocking
                    - QUIC handle packet loss at the individual stream level, means loss a single packet does not block the entire connection
                - Connection migration
                    - Better connection migration allows clients to change IP address without losing connectivity in incurring additional latency
                - 0-RTT (zero round trip time) establishment
                    - can significantly reduce latency when connecting to a previously visited server
                - Improved congestion control
                    - offers more advanced congestion control mechanisms
                    - better adapt to varying network conditions and improve overall performance

# API (application programming interface) Paradigms[[Link](https://neetcode.io/courses/system-design-for-beginners/8)]
- Provide a say for clients to perform actions with server over the network
- Consist of a set of rules and protocols for building and interacting with software applications
- __Three Paradigms__
    - `REST APIs`
        - An API adheres to design principle and standard of the `Representation State Transfer` 
        - Utilize straightforward HTTP for communication between machine, specifically the client and server
        - Constriants:
            - REST APIs require a client-server architecture
                - client and server are distinct entities commnuicating over a network.
                - this separation enables independent development and updates for both the client and server
            - REST APIs are Stateless
                - each client request to the server must include all necessary information for understanding and processing the request
                - the server should not retain any details about the previous client requests
                    - client must always send all needed info per request
                    - server does not "remember" the client
                - does not need to manage or update session states or cookies, facilitaes horizontal scaling
        - Consider:
            ```text
            In the context of a client sending a request to a REST API to retrieve a specific resource (GET request), the request 
            includes all the necessary information, eliminating the need for the server to remember previous requests. Now, 
            let's delve into the concept of state.

            Consider the example of a URL such as https://youtube.com/videos where we want to display a list of 10 videos on a 
            page, and display more videos as the user scrolls. The constraint is that the server should not persist any 
            state, such as how many videos have already been displayed.
            
            Instead, data stored on the client can be sent to the server with each request. This principle is particularly 
            relevant in pagination scenarios. When a page loads the initial 10 videos, and the user keeps scrolling down to 
            the second page, the server does not remember that the user was already shown 10 videos.

            So, the client sends this information to the server by including parameters in the GET URL. For instance, the client might send a request like:

            https://youtube.com/videos?offset=0&limit=10,

            which fetches the first 10 videos, followed by

            https://youtube.com/videos?offset=10&limit=10,

            which fetches the next 10 videos.
            ```
        - `JSON` (JavaScript Object Notation)
            - REST APIs accept data in JSON format and respond with data encapsulate in the same format
        - Issues with REST APIs
            - over-fetching: client receives more data than necessary
                ```text
                Let's consider an example where we need to fetch data to display comments on a website. The required data 
                includes the user's profile picture, username, and the comment itself. However, the /user endpoint might 
                provide additional, unnecessary information such as country or date joined. In this case we are required 
                to over-fetch data and subsequently filter out the irrelevant fields.
                ```
            - under-fetching: 
                - when endpoints are narrowly defined, resulting in the delivery of only a single field per request
                - this situation requires making multiple calls to fetch required property separately.

    - `GraphQL`
        - Address limitations of REST APIs in mitigating issues related to over-fetching and under-fetching
        - Client gains the ability to precisely specify the required data within a single request
            - the server take on the responsibility of gathering all the necessary data and formatting it accordingly after the client's specification
        - Two Primary type of operations:
            - queries: retrive data
            - mutations: modify data on the server
        - Operate through a single endpoint, typically HTTP POST endpoint, where all queries are sent
    
    - `gRPC`: Google Remote Procedure Call
        - Building on top of HTTP/2
        - A framework for executing RPC: allows a program to execute a procedure in another address space
        - Provides bidirectional commnunication, or multiplexing for multiple messages over a single TCP connection and server push
        - Typically used for server-server communication
            - much faster than REST APIs
            - send data using protocol buffers
                - language-neutral, platform-neutral extensible mechanism for serializng structure data (less size of data to transfer than REST APIs)
            - provide streaming
                - push data from the client to the server
        - Does not ake use of the error cide provided by HTTP

# API Design[[Link](https://neetcode.io/courses/system-design-for-beginners/9)]
__Example: Twritter REST APIs__
- APIs typcially provide general CRUD, in case of Twitter:
    - `createTweet()`
    - `getTweets()`
    - `editTweet()`
    - `deleteTweet()`
        - These operatoins are performed on entities
- __Why bother desiging good APIs?__
    - Need to consider their public-facing nature
    - Relied upon many application, and they use it by their own function call
        - This restriction limits API developers from making excessive change to avoid potential crashes in the apps that rely on Twitter API
    - `Create a Tweet: createTweet(userId, content)`
        ```text
        Suppose we want to introduce a reply feature. Modifying the original method signature to include a parentId parameter, 
        like createTweet(userId, content, parentId), would potentially disrupt a large number of applications. To address this, a 
        better approach would be to make the parentId parameter optional.
        ```
        - Design choice should be backward compatibility
            - helps maintain a smooth transition and avoid breaking existing functionality for applications that rely on the original method
        - A tweet object, url: `https://api.twitter.com/v1.0/tweet`
            ```text
            userId: string, // The creator of the tweet, passed by the client
            tweetId: string, // Uniquely identifies each tweet, created server side
            content: string, // Passed in by the client
            createdAt: date, // The timestamp, handled server side
            likes: int, // handled by the server side
            ```
    - `Retriving Tweets`
        - Endpoint like: `https://api.twitter.com/v1.0/tweet/:userId`
            - this fetch all tweet for a specific creator
        - Example:
            ```text
            However, when it comes to retrieving a list of tweets, a different approach is needed. This situation often arises 
            in Higher Education institutions' websites, where a segment on the homepage displays their Twitter activity. 
            Using the same endpoint for retrieving a single tweet is not suitable in this case.

            To address this, let's recall the concept of pagination discussed in the previous chapter. To fetch only 10 
            tweets, we can structure our URL as follows: https://api.twitter.com/v1.0/users/:id/tweets?limit=10&offset=0. Here, 
            the limit parameter indicates the number of tweets to be fetched per page, while the offset parameter determines 
            the starting point. It's important to recall that GET requests are idempotent, meaning that regardless of how 
            many times we call this URL, it should consistently return the same data without side effects. (Though, in twitter's 
            case the homefeed data itself may change over time.)

            By incorporating limit and offset parameters in the URL, we can implement pagination effectively, enabling the 
            retrieval of a specific number of tweets at a time while maintaining consistency in the returned data.
            ```
    - `API Versions`
        - Companies typically update the API version when significant changes are made such as adding new parameters, method, or completely changing how things work
        - Easier to distinguish between different iterations and helps developers adapt their code to accomodate any changes or improvement
- Take a look for some API docs
    - [Stripe](https://docs.stripe.com/api)
    - [Reddit](https://www.reddit.com/dev/api/)
    - [Instagram](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login)
    - [Facebook](https://developers.facebook.com/docs/)