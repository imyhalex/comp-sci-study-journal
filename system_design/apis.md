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
            e,g.: a web server delivers web pages to clients, an email server handles sending and receiving emails, and a database server provides clients with access to database services.
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
