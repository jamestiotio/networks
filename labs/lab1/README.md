# Lab 1: A Simple Web Proxy Server

## Objectives

In this lab, you will learn how web proxy servers work and one of their basic functionalities — caching. You will also familiarize yourself with socket programming and basic of HTTP protocol.

Your task is to develop a highly simplified web proxy server which is able to cache web pages. It is a very basic proxy that only understands HTTP GET requests. In particular, it does not support HTTPS and does not support other types of HTTP methods (e.g., PUT, POST...)

Generally, when a client makes an HTTP request, the request is sent to a web server. The web server then processes the request and sends back a response message to the requesting client. If we put a proxy server between the client and the web server, both the request message sent by the client and the response message delivered by the web server pass through the proxy server. In other words, the client requests the objects via the proxy server. The proxy server will forward the client’s request to the web server. The web server will then generate a response message and deliver it to the proxy server, which in turn sends it to the client.

## Usage

You can pass the port number you want your proxy to listen to as an optional argument. In the supplied code, it will listen to 8079 by default.

From a terminal, you can use sudo lsof -i :8079 to checkout the process that is listening on that port.

You can then configure your web browser to use your proxy. How to set this up depends on your browser. A snapshot of the configuration for chrome is given in the figure above (this may vary with your OS too). In general, you need to specify the IP address of the host that you run your proxy and its port number there. If you run your proxy and your web browser on the same computer, you can simply use 127.0.0.1 or localhost for the proxy’s address. If you run them in different computers, make sure the two computers can reach each other, and you need to find out the IP address of the computer that runs the proxy server, and use that address to configure your browser’s proxy setup. After you start your proxy server and configure your browser, to get a web page, you simply provide the URL of the page you want in the browser, e.g.,

- [http://httpforever.com/](http://httpforever.com/)
- [http://www.neverssl.com/](http://www.neverssl.com/)
- [http://www.httpvshttps.com/](http://www.httpvshttps.com/)
- [http://www.webscantest.com/](http://www.webscantest.com/)

As our simple proxy only supports HTTP sites, above list give you a few stable HTTP websites that you can test against.

After you visit a website, your browser likely also keeps its own local cache. To force your browser to ignore its local cache and always contact the server, you can use Chrome’s DevTools (press F12 to launch it), and from there you can select Disable Cache (under the Network tab), and then you can use Ctrl + R to refresh.

## Further Exploration

Note that after you put in the minimum code to make our simple proxy run, the proxy still lacks many important features, e.g., the understanding of various header fields received in a request from the client. Your are encouraged to read [RFC7234](https://tools.ietf.org/html/rfc7234) to learn more about some complexity involved in implementing a proxy.

Here are some questions you can think about when reading the RFC:

- How the proxy should use the If-None-Match and ETag headers in the HTTP Request and Response respectively to decide its response to the client?
- How to support HTTP Requests with the Range header?

You are encouraged to think about how to add these features into our simple proxy code.

In addition, you are encouraged to try out the following software. They all provide web proxy functionality as part of their feature offerings:

- Burp Suite
  - [https://portswigger.net/burp/communitydownload](https://portswigger.net/burp/communitydownload)
  - [https://portswigger.net/burp/documentation/desktop/tools/proxy/using](https://portswigger.net/burp/documentation/desktop/tools/proxy/using)
- POSTMAN
  - [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
  - [https://learning.postman.com/docs/sending-requests/capturing-request-data/capturing-http-requests/#built-in-proxy](https://learning.postman.com/docs/sending-requests/capturing-request-data/capturing-http-requests/#built-in-proxy)
- NGINX
  - [https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)

Some questions you can think about when trying the software: What are the main use cases of them, respectively? What are the benefits a web proxy can offer in the respective use cases? What are some different approaches that a proxy can take to handle HTTPS connections?

If you explore some of the software listed above or implement any advanced features in your proxy, you are encouraged to summarize your findings in a separate write-up and submit that together with your proxy code. We will share selected submissions with your classmates.
