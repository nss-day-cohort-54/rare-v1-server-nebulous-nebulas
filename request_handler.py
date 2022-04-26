from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
from views import delete_category, get_all_categories, get_single_category, update_category
from views import get_all_posts, get_single_post
from views import create_user, login_user
from views.tag_request import create_new_tag, delete_tag, get_all_tags, get_single_tag


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        
        self._set_headers(200)
        
        parsed = self.parse_url()
        
        response = {}
        
        if len(parsed) == 2:
            (resource, id) = parsed
            
            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
                    
            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
                    
            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"        
        
        self.wfile.write(f'{response}'.encode())
        


    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = None
        (resource, id) = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
        elif resource == 'register':
            response = create_user(post_body)
        elif resource == 'tags':
            response = create_new_tag(post_body)

        self.wfile.write(response.encode())

    def do_PUT(self):
        
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        success = False
        
        
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url()
        
        if resource == "categories":
            success = update_category(id, post_body)
        if resource == "tags":
            success = update_category(id, post_body)
            
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        
        self.wfile.write("".encode())
        

    def do_DELETE(self):
        
        (resource, id) = self.parse_url()
        
        if resource == "categories":
            response = delete_category(id)
        if resource =="tags":
            response = delete_tag(id)
        
        if response == False:
            self._set_headers(404)
        else:
            self._set_headers(204)
            
            
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
