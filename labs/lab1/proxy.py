#!/usr/bin/env python3
# SUTD 50.012 Networks Lab 1
# James Raphael Tiovalen (1004555)

from socket import *
import sys, os
import _thread as thread

proxy_port = 8079
cache_directory = "./cache/"
buf_size = 2 ** 30
socket_timeout = 10.0


def client_thread(client_facing_socket):
    client_facing_socket.settimeout(socket_timeout)

    try:
        message = client_facing_socket.recv(buf_size).decode()
        msg_elements = message.split()

        if (
            len(msg_elements) < 5
            or msg_elements[0].upper() != "GET"
            or "Range:" in msg_elements
        ):
            # print("Non-supported request: ", msg_elements)
            client_facing_socket.close()
            return

        # Extract the following info from the received message:
        # - web_server: the web server's host name
        # - resource: the web resource requested
        # - file_to_use: a valid file name to cache the requested resource
        # - Assume the HTTP request is in the format of:
        #      GET http://www.mit.edu/ HTTP/1.1\r\n
        #      Host: www.mit.edu\r\n
        #      User-Agent: .....
        #      Accept:  ......

        # Remove query parameters and trailing slashes from URL to create valid and safe/secure filenames
        resource = (
            msg_elements[1].replace("http://", "", 1).split("?", 1)[0].rstrip("/")
        )

        host_header_index = msg_elements.index("Host:")
        web_server = msg_elements[host_header_index + 1]

        http_port = 80

        print("web_server: ", web_server)
        print("resource: ", resource)

        message = message.replace("Connection: keep-alive", "Connection: close")

        website_directory = cache_directory + web_server.replace("/", ".") + "/"

        if not os.path.exists(website_directory):
            os.makedirs(website_directory)

        file_to_use = website_directory + resource.replace("/", ".")

    except:
        print(str(sys.exc_info()[0]))
        client_facing_socket.close()
        return

    # Check whether the file exists in the cache
    try:
        with open(file_to_use, "rb") as f:
            # Proxy Server finds a cache hit and generates a response message
            print("served from the cache")
            while True:
                buff = f.read(buf_size)
                if buff:
                    # Fill in start
                    client_facing_socket.send(buff)
                    # Fill in end
                else:
                    break

    except FileNotFoundError as e:
        try:
            # Create a socket on the proxy server
            server_facing_socket = socket(
                AF_INET, SOCK_STREAM
            )  # Fill in start             # Fill in end
            # Connect to the socket to port 80
            # Fill in start
            server_facing_socket.settimeout(socket_timeout)
            server_facing_socket.connect((web_server, http_port))
            server_facing_socket.send(message.encode())

            # Fill in end

            with open(file_to_use, "wb") as cache_file:
                try:
                    while True:
                        buff = server_facing_socket.recv(
                            buf_size
                        )  # Fill in start             # Fill in end
                        if buff:
                            # Fill in start
                            cache_file.write(buff)
                            client_facing_socket.send(buff)
                            # Fill in end
                        else:
                            break
                except:
                    print(str(sys.exc_info()[0]))

        except:
            print(str(sys.exc_info()[0]))

        finally:
            # Fill in start
            server_facing_socket.close()
            # Fill in end

    except:
        print(str(sys.exc_info()[0]))

    finally:
        # Fill in start
        client_facing_socket.close()
        # Fill in end


def main():
    if len(sys.argv) > 2:
        print('Usage: "python proxy.py port_number"\n')
        sys.exit(2)
    if len(sys.argv) == 2:
        proxy_port = int(sys.argv[1])

    if not os.path.exists(cache_directory):
        os.makedirs(cache_directory)

    # Create a server socket, bind it to a port and start listening
    welcome_socket = socket(
        AF_INET, SOCK_STREAM
    )  # Fill in start             # Fill in end

    # Fill in start
    welcome_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    welcome_socket.bind(("localhost", proxy_port))
    welcome_socket.listen(1)
    # Fill in end

    print("Proxy ready to serve at port", proxy_port)

    try:
        while True:
            # Start receiving data from the client
            (
                client_facing_socket,
                addr,
            ) = welcome_socket.accept()  # Fill in start             # Fill in end
            print("Received a connection from: ", addr)

            # The following function starts a new thread, taking the function name as the first argument, and a tuple of arguments to the function as its second argument
            thread.start_new_thread(client_thread, (client_facing_socket,))

    except KeyboardInterrupt:
        print("Bye...")

    finally:
        # Fill in start
        welcome_socket.close()
        # Fill in end


if __name__ == "__main__":
    main()
