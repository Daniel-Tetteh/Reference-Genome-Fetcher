import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os

PORT = 3000

class GenomeFetcherHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Route API requests
        if path == '/api/search':
            self.handle_search(query_params)
        elif path == '/api/links':
            self.handle_links(query_params)
        else:
            # Serve static files from the 'public' folder
            clean_path = path.lstrip('/')
            if not clean_path:
                clean_path = 'index.html'

            local_path = os.path.join(os.getcwd(), 'public', clean_path)

            if os.path.isfile(local_path):
                self.path = f'/public/{clean_path}'
            else:
                self.path = '/public/index.html'

            # Let the parent SimpleHTTPRequestHandler handle standard file serving
            super().do_GET()

    def handle_search(self, params):
        q_list = params.get('q')
        if not q_list:
            self.send_error_json(400, 'Search query is required')
            return

        query = q_list[0].strip()
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/{encoded_query}/dataset_report?filters.reference_only=true"

        print(f"[NCBI Search] Fetching: {url}")

        try:
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/json')
            
            # Use NCBI_API_KEY from environment variables if present
            api_key = os.environ.get('NCBI_API_KEY')
            if api_key:
                req.add_header('api-key', api_key)

            with urllib.request.urlopen(req) as response:
                data = response.read()
                self.send_response_json(200, data)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # 404 means no genomes found for this taxon, return empty report list
                empty_res = json.dumps({'reports': [], 'total_count': 0}).encode('utf-8')
                self.send_response_json(200, empty_res)
            else:
                self.send_error_json(e.code, f"NCBI API returned error: {e.reason}")
        except Exception as error:
            print("Search API error:", error)
            self.send_error_json(500, f"Failed to fetch genome data from NCBI: {str(error)}")

    def handle_links(self, params):
        acc_list = params.get('accession')
        if not acc_list:
            self.send_error_json(400, 'Accession is required')
            return

        accession = acc_list[0].strip()
        encoded_acc = urllib.parse.quote(accession)
        url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/{encoded_acc}/links"

        print(f"[NCBI Links] Fetching: {url}")

        try:
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/json')
            
            # Use NCBI_API_KEY from environment variables if present
            api_key = os.environ.get('NCBI_API_KEY')
            if api_key:
                req.add_header('api-key', api_key)

            with urllib.request.urlopen(req) as response:
                data = response.read()
                self.send_response_json(200, data)
        except Exception as error:
            print("Links API error:", error)
            self.send_error_json(500, f"Failed to fetch assembly links from NCBI: {str(error)}")

    def send_response_json(self, status, json_bytes):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(json_bytes))
        self.end_headers()
        self.wfile.write(json_bytes)

    def send_error_json(self, status, message):
        err_dict = {'error': message}
        err_bytes = json.dumps(err_dict).encode('utf-8')
        self.send_response_json(status, err_bytes)

def run():
    # Ensure public folder exists
    os.makedirs('public', exist_ok=True)

    # Enable address reuse to avoid port already in use errors on restarts
    socketserver.TCPServer.allow_reuse_address = True

    handler = GenomeFetcherHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"=================================================")
        print(f"  Genome Fetcher Server Running on Port {PORT}")
        print(f"  Local URL: http://localhost:{PORT}")
        print(f"=================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == '__main__':
    run()
