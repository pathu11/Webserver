import socket
from subprocess import Popen, PIPE
import os
import json

PORT = 2728
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = 'localhost'
ADDR = (SERVER, PORT)

# The directory where the web resources are located
RESOURCE_DIRECTORY = "htdocs"

# The list of supported file extensions for PHP execution
PHP_SUPPORTED_EXTENSION_LIST = ["php", "html"]

# Create the socket...socket type (IPv4)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            # Decode the data from bytes to string (utf-8)
            data = conn.recv(4096).decode(FORMAT)
            if not data:
                break

            if data.startswith("GET /"):
                # Get header details from received data
                request_header_details = get_request_header_details(data)
                # Getting the response header details
                status_details = get_status_details(request_header_details["resource_path"])
                # if the resource is available, get the byte version of it. Else it will return the 404.html
                resource = fetch_resource(**request_header_details, **status_details)
                # creating a new response: Basically this combines the response headers with resource data
                response = create_new_response(request_header_details["protocol"], status_details, resource)

                conn.send(response)
                conn.close()
                connected = False

        except Exception as e:
            print(f"[ERROR] An error occurred: {str(e)}")
            break

    print(f"[DISCONNECTED] {addr} disconnected.")

# Read the http request
def get_request_header_details(data):
    request_line = data.split('\r\n')[0]
    method, resource_path, protocol = request_line.split()
    parameters = {}

    if method == "GET":
        resource_path += "?"
        query_string = resource_path.split("?")[1]
        ##if GET request, the parameteres can be derived from the resource path
        resource_path = resource_path.split("?")[0]
    else:
        # if the method is POST, the parameters are stored at the bottom of the received data
        query_string = data.splitlines()[-1]
    # This will return the query_string (I.E : "a=1&b=2") as a dictionary (I.E : {"a":1,"b":2})
    parameters = parse_parameters_from_path(query_string)

    if resource_path.endswith("/"):
        resource_path += "index.php"
    elif not resource_path.count("."):
        resource_path += "/index.php"

    return {
        "method": method,
        # To avoid getting a "/" at the start of the resource path
        "resource_path": resource_path[1:],
        "protocol": protocol,
        "parameters": parameters
    }

def parse_parameters_from_path(path):
    # This will return the query_string (I.E : "a=1&b=2") as a dictionary (I.E : {"a":1,"b":2})
    parameters = {}
    if path.count("="):
        for single_query in path.split("&"):
            variable, value = single_query.split("=")
            parameters[variable] = value

    return parameters

def get_status_details(resource_path):
    status_details_dict = {"status_code": 0, "message": "NULL"}

    if os.path.exists(f"./{RESOURCE_DIRECTORY}/{resource_path}"):
        status_details_dict["status_code"] = 200
        status_details_dict["message"] = "OK"
    else:
        status_details_dict["status_code"] = 404
        status_details_dict["message"] = "Not Found"

    return status_details_dict

# Fetches the requested resource based on the provided arguments.
def fetch_resource(**kwargs):
    method = kwargs["method"] # HTTP request method (GET or POST)
    path = kwargs["resource_path"] # Path to the requested resource
    parameters = kwargs["parameters"]

    if kwargs["status_code"] == 404:
        # If the status code is 404 (Not Found), serve a default 404.html page.
        with open(f"./{RESOURCE_DIRECTORY}/404.html", "rb") as resource:
            return resource.read()

    if path.split(".")[-1] in PHP_SUPPORTED_EXTENSION_LIST:
        # if the resource is a php or html file, we will treat it differently compared to other resources
        output = fetch_php_output(method, path, parameters)
        return output
    else:
        # For other resources (e.g., images, CSS, JavaScript), read and return their content.
        with open(f"./{RESOURCE_DIRECTORY}/{path}", "rb") as resource:
            return resource.read()

# Fetches the PHP output for a PHP script based on provided arguments.

def fetch_php_output(method, path, parameters):
    payload = json.dumps({
        "method": method,
        "path": path,
        "parameters": parameters
    })
    # Execute the PHP script using a separate process and capture its output.
    process = Popen(["./php/php", f"./{RESOURCE_DIRECTORY}/wrapper.php", payload], stdout=PIPE, cwd="./")
    (output, error) = process.communicate()
    process.wait()


    return output
# Create  new HTTP response for the request
def create_new_response(protocol, status_details_dict, resource):
    response = f"{protocol} {status_details_dict['status_code']} {status_details_dict['message']}".encode("utf-8") + b'\r\n'
    response += b"Content-Type: text/html\r\n"
    response += b"\r\n"

    if status_details_dict["status_code"] == 200:
        # If the status code is 200 (OK), include the resource content in the response.
        response += resource
    else:
        response += resource

    return response

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)

print(f"[STARTING] Server is starting in port {PORT}")
start()
