# SUTD 2021 50.012 Networks Lab 1 Writeup Submission README Document

> James Raphael Tiovalen / 1004555

## Extra Optional Discussion

1. What are the main use cases of Burp Suite, Postman, and NGINX, respectively? What are the benefits a web proxy can offer in the respective use cases?
   - Burp Suite
     - The proxy intercepts and logs requests to the web server and allows the user to modify the request (e.g., modifying the `User-Agent` request header) before sending and forwarding the request on to the web server.
     - The intercepted request can also be repeated back to the server such as in the case of a brute force dictionary attack.
   - Postman
     - An API software platform for building and using APIs.
     - Proxy can be useful for debugging purposes to log and analyze the requests and responses.
   - NGINX
     - A web server that can be used as a reverse proxy.
     - As a reverse proxy, it can be used as a load balancer by distributing client requests across a group of web servers.
     - Caching can help improve response time, especially if the web servers are far away geographically.
     - As a reverse proxy, it will also hide information about the servers and the internal network behind the proxy, and it can act as an additional defensive layer against malicious actors.
     - Modifications to server configurations can be easily done without impacting users.
     - Reverse proxy server handles the encryption and the decryption of the data, freeing up resources on the servers behind the proxy.

2. What are some different approaches that a proxy can take to handle HTTPS connections?

   One possible approach would be to serve as a man-in-the-middle (MITM) proxy (such as Burp Suite).

   - Burp will have to break up the TLS connection, becoming the man-in-the-middle.
   - First, Burp generates its own TLS certificate signed by its CA and the user installs this certificate as a trusted root.
   - Burp then uses this CA certificate to sign the TLS certificate for each host visited by the user.
   - Thus, Burp can decrypt the encrypted data from the client and begin a (separate) TLS session with the server, and then encrypt and send the data forward to the server.
   - After receiving the data from the server, it decrypts the data and we now have the data in plaintext to analyze in Burp.
   - After some analysis/modification in Burp, we can then encrypt the data again in Burp and pass it back to the client.
