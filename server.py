import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os

PORT = 3000

# ==========================================================================
# Offline Mock Database (Fallback for dns/network failure)
# ==========================================================================
LOCAL_DB = {
    "homo sapiens": [
        # Reference genome
        {
            "accession": "GCF_000001405.40",
            "current_accession": "GCF_000001405.40",
            "source_database": "SOURCE_DATABASE_REFSEQ",
            "organism": {
                "tax_id": 9606,
                "organism_name": "Homo sapiens",
                "common_name": "human"
            },
            "assembly_info": {
                "assembly_level": "Chromosome",
                "assembly_status": "current",
                "assembly_name": "GRCh38.p14",
                "bioproject_accession": "PRJNA31257",
                "release_date": "2022-02-03",
                "submitter": "Genome Reference Consortium",
                "refseq_category": "reference genome"
            },
            "assembly_stats": {
                "total_number_of_chromosomes": 24,
                "total_sequence_length": 3099441038,
                "total_ungapped_length": 2948318359,
                "number_of_contigs": 996,
                "contig_n50": 57879411,
                "number_of_scaffolds": 470,
                "scaffold_n50": 67794873,
                "gc_percent": 41
            },
            "organelle_info": [
                {"description": "Mitochondrion", "total_seq_length": "16569"}
            ],
            "ensembl_metadata": {
                "assembly_name": "GRCh38.p14",
                "assembly_date": "2022-02-03",
                "genebuild_method": "Annotation of NCBI RefSeq assembly",
                "genebuild_last_geneset_update": "2025-08-01",
                "assembly_authority": "Genome Reference Consortium"
            }
        },
        # Alternative cancer genome
        {
            "accession": "GCA_000001405.29",
            "current_accession": "GCA_000001405.29",
            "source_database": "GenBank",
            "organism": {
                "tax_id": 9606,
                "organism_name": "Homo sapiens (Cancer Cell Line)",
                "common_name": "human cancer strain"
            },
            "assembly_info": {
                "assembly_level": "Chromosome",
                "assembly_status": "current",
                "assembly_name": "GRCh38_alternative",
                "bioproject_accession": "PRJNA31257",
                "release_date": "2023-05-12",
                "submitter": "Genome Reference Consortium",
                "refseq_category": "alternative assembly"
            },
            "assembly_stats": {
                "total_number_of_chromosomes": 24,
                "total_sequence_length": 3105000000,
                "total_ungapped_length": 2950000000,
                "number_of_contigs": 1200,
                "contig_n50": 54000000,
                "number_of_scaffolds": 510,
                "scaffold_n50": 62000000,
                "gc_percent": 41
            }
        }
    ],
    "saccharomyces cerevisiae": [
        {
            "accession": "GCF_000146045.2",
            "current_accession": "GCF_000146045.2",
            "source_database": "SOURCE_DATABASE_REFSEQ",
            "organism": {
                "tax_id": 4932,
                "organism_name": "Saccharomyces cerevisiae",
                "common_name": "baker's yeast"
            },
            "assembly_info": {
                "assembly_level": "Chromosome",
                "assembly_status": "current",
                "assembly_name": "R64",
                "bioproject_accession": "PRJNA128",
                "release_date": "2011-02-03",
                "submitter": "Saccharomyces Genome Database",
                "refseq_category": "reference genome"
            },
            "assembly_stats": {
                "total_number_of_chromosomes": 17,
                "total_sequence_length": 12157105,
                "total_ungapped_length": 12071326,
                "number_of_contigs": 17,
                "contig_n50": 925763,
                "number_of_scaffolds": 17,
                "scaffold_n50": 925763,
                "gc_percent": 38
            },
            "ensembl_metadata": {
                "assembly_name": "R64",
                "assembly_date": "2011-02-03",
                "genebuild_method": "Imported from SGD",
                "genebuild_last_geneset_update": "2024-01-01",
                "assembly_authority": "Saccharomyces Genome Database"
            }
        }
    ],
    "escherichia coli": [
        {
            "accession": "GCF_000005845.2",
            "current_accession": "GCF_000005845.2",
            "source_database": "SOURCE_DATABASE_REFSEQ",
            "organism": {
                "tax_id": 511145,
                "organism_name": "Escherichia coli str. K-12 substr. MG1655",
                "common_name": "E. coli"
            },
            "assembly_info": {
                "assembly_level": "Complete Genome",
                "assembly_status": "current",
                "assembly_name": "ASM584v2",
                "bioproject_accession": "PRJNA57659",
                "release_date": "2013-12-09",
                "submitter": "University of Wisconsin-Madison",
                "refseq_category": "reference genome"
            },
            "assembly_stats": {
                "total_number_of_chromosomes": 1,
                "total_sequence_length": 4641652,
                "total_ungapped_length": 4641652,
                "number_of_contigs": 1,
                "contig_n50": 4641652,
                "number_of_scaffolds": 1,
                "scaffold_n50": 4641652,
                "gc_percent": 50.8
            }
        }
    ],
    "mus musculus": [
        {
            "accession": "GCF_000001635.27",
            "current_accession": "GCF_000001635.27",
            "source_database": "SOURCE_DATABASE_REFSEQ",
            "organism": {
                "tax_id": 10090,
                "organism_name": "Mus musculus",
                "common_name": "house mouse"
            },
            "assembly_info": {
                "assembly_level": "Chromosome",
                "assembly_status": "current",
                "assembly_name": "GRCm39",
                "bioproject_accession": "PRJNA20689",
                "release_date": "2020-09-22",
                "submitter": "Genome Reference Consortium",
                "refseq_category": "reference genome"
            },
            "assembly_stats": {
                "total_number_of_chromosomes": 21,
                "total_sequence_length": 2728222451,
                "total_ungapped_length": 2650785102,
                "number_of_contigs": 998,
                "contig_n50": 32000000,
                "number_of_scaffolds": 450,
                "scaffold_n50": 58000000,
                "gc_percent": 41.5
            },
            "ensembl_metadata": {
                "assembly_name": "GRCm39",
                "assembly_date": "2020-09-22",
                "genebuild_method": "Annotation of NCBI RefSeq",
                "genebuild_last_geneset_update": "2025-01-01",
                "assembly_authority": "Genome Reference Consortium"
            }
        }
    ],
    "arabidopsis thaliana": [
        {
            "accession": "GCF_000001735.4",
            "current_accession": "GCF_000001735.4",
            "source_database": "SOURCE_DATABASE_REFSEQ",
            "organism": {
                "tax_id": 3702,
                "organism_name": "Arabidopsis thaliana",
                "common_name": "thale cress"
            },
            "assembly_info": {
                "assembly_level": "Chromosome",
                "assembly_status": "current",
                "assembly_name": "TAIR10.1",
                "bioproject_accession": "PRJNA117",
                "release_date": "2018-05-18",
                "submitter": "The Arabidopsis Information Resource",
                "refseq_category": "reference genome"
            },
            "assembly_stats": {
                "total_number_of_chromosomes": 5,
                "total_sequence_length": 119668634,
                "total_ungapped_length": 119146348,
                "number_of_contigs": 5,
                "contig_n50": 30427671,
                "number_of_scaffolds": 5,
                "scaffold_n50": 30427671,
                "gc_percent": 36
            }
        }
    ],
    "plasmodium falciparum": [
        # Reference (3D7 strain)
        {
            "accession": "GCF_000002765.6",
            "current_accession": "GCF_000002765.6",
            "source_database": "SOURCE_DATABASE_REFSEQ",
            "organism": {
                "tax_id": 5833,
                "organism_name": "Plasmodium falciparum 3D7",
                "common_name": "malaria parasite reference"
            },
            "assembly_info": {
                "assembly_level": "Chromosome",
                "assembly_status": "current",
                "assembly_name": "ASM276v2",
                "bioproject_accession": "PRJNA148",
                "release_date": "2019-10-15",
                "submitter": "Wellcome Sanger Institute",
                "refseq_category": "reference genome"
            },
            "assembly_stats": {
                "total_number_of_chromosomes": 14,
                "total_sequence_length": 23292622,
                "total_ungapped_length": 22853240,
                "number_of_contigs": 14,
                "contig_n50": 1683411,
                "number_of_scaffolds": 14,
                "scaffold_n50": 1683411,
                "gc_percent": 19.4
            }
        },
        # Isolate Dd2 (drug-resistant)
        {
            "accession": "GCA_000002765.1",
            "current_accession": "GCA_000002765.1",
            "source_database": "GenBank",
            "organism": {
                "tax_id": 5833,
                "organism_name": "Plasmodium falciparum Dd2 (Chloroquine-resistant)",
                "common_name": "malaria parasite strain Dd2"
            },
            "assembly_info": {
                "assembly_level": "Chromosome",
                "assembly_status": "current",
                "assembly_name": "ASM276v1_Dd2",
                "bioproject_accession": "PRJNA148",
                "release_date": "2020-04-10",
                "submitter": "Wellcome Sanger Institute",
                "refseq_category": "alternative assembly"
            },
            "assembly_stats": {
                "total_number_of_chromosomes": 14,
                "total_sequence_length": 23310000,
                "total_ungapped_length": 22890000,
                "number_of_contigs": 35,
                "contig_n50": 1200000,
                "number_of_scaffolds": 22,
                "scaffold_n50": 1500000,
                "gc_percent": 19.4
            }
        }
    ],
    "severe acute respiratory syndrome coronavirus 2": [
        {
            "accession": "NC_045512.2",
            "is_virus": True,
            "completeness": "COMPLETE",
            "release_date": "2020-01-13",
            "source_database": "RefSeq",
            "length": 29903,
            "virus": {
                "tax_id": 2697049,
                "organism_name": "Severe acute respiratory syndrome coronavirus 2",
                "pangolin_classification": "B"
            }
        }
    ],
    "hepatitis b virus": [
        {
            "accession": "NC_003977.2",
            "is_virus": True,
            "completeness": "COMPLETE",
            "release_date": "2002-05-15",
            "source_database": "RefSeq",
            "length": 3215,
            "virus": {
                "tax_id": 10407,
                "organism_name": "Hepatitis B virus",
                "pangolin_classification": "N/A"
            }
        }
    ]
}

ALIASES = {
    "human": "homo sapiens",
    "homo sapiens": "homo sapiens",
    "yeast": "saccharomyces cerevisiae",
    "saccharomyces cerevisiae": "saccharomyces cerevisiae",
    "e. coli": "escherichia coli",
    "escherichia coli": "escherichia coli",
    "mouse": "mus musculus",
    "mus musculus": "mus musculus",
    "arabidopsis": "arabidopsis thaliana",
    "arabidopsis thaliana": "arabidopsis thaliana",
    "malaria": "plasmodium falciparum",
    "plasmodium falciparum": "plasmodium falciparum",
    "coronavirus": "severe acute respiratory syndrome coronavirus 2",
    "sars-cov-2": "severe acute respiratory syndrome coronavirus 2",
    "severe acute respiratory syndrome coronavirus 2": "severe acute respiratory syndrome coronavirus 2",
    "hepatitis": "hepatitis b virus",
    "hepatitis b virus": "hepatitis b virus"
}

def fetch_ensembl_metadata(scientific_name):
    formatted_name = scientific_name.strip().replace(' ', '_').lower()
    url = f"https://rest.ensembl.org/info/assembly/{formatted_name}"
    try:
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        # Set a short timeout so Ensembl query doesn't hang the search
        with urllib.request.urlopen(req, timeout=3) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Ensembl fetch error for {formatted_name}: {e}")
        return None

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
        elif path == '/api/autocomplete':
            self.handle_autocomplete(query_params)
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

    def serve_offline_search(self, query, ref_only):
        normalized_q = query.strip().lower()
        matched_key = None
        
        # Match in ALIASES
        if normalized_q in ALIASES:
            matched_key = ALIASES[normalized_q]
        else:
            for alias in ALIASES:
                if normalized_q in alias or alias in normalized_q:
                    matched_key = ALIASES[alias]
                    break
        
        reports = []
        if matched_key and matched_key in LOCAL_DB:
            raw_reports = LOCAL_DB[matched_key]
            for r in raw_reports:
                r_copy = json.loads(json.dumps(r))
                r_copy['is_offline'] = True
                
                if ref_only:
                    if r_copy.get('is_virus'):
                        if r_copy.get('source_database') == 'RefSeq':
                            reports.append(r_copy)
                    else:
                        if r_copy.get('assembly_info', {}).get('refseq_category') == 'reference genome':
                            reports.append(r_copy)
                else:
                    reports.append(r_copy)

        res_data = {
            'reports': reports,
            'total_count': len(reports),
            'is_offline': True
        }
        self.send_response_json(200, json.dumps(res_data).encode('utf-8'))

    def serve_offline_autocomplete(self, query):
        normalized_q = query.strip().lower()
        matches = []
        seen = set()
        for alias, db_key in ALIASES.items():
            if normalized_q in alias:
                sci_name = db_key.title()
                if db_key == "homo sapiens":
                    sci_name = "Homo sapiens"
                elif db_key == "saccharomyces cerevisiae":
                    sci_name = "Saccharomyces cerevisiae"
                elif db_key == "escherichia coli":
                    sci_name = "Escherichia coli"
                elif db_key == "mus musculus":
                    sci_name = "Mus musculus"
                elif db_key == "arabidopsis thaliana":
                    sci_name = "Arabidopsis thaliana"
                elif db_key == "plasmodium falciparum":
                    sci_name = "Plasmodium falciparum"
                elif db_key == "severe acute respiratory syndrome coronavirus 2":
                    sci_name = "Severe acute respiratory syndrome coronavirus 2"
                elif db_key == "hepatitis b virus":
                    sci_name = "Hepatitis B virus"
                
                if sci_name not in seen:
                    matches.append(sci_name)
                    seen.add(sci_name)
        
        res_data = {
            'dictionary_terms': {
                'taxonomy': matches[:10]
            },
            'is_offline': True
        }
        self.send_response_json(200, json.dumps(res_data).encode('utf-8'))

    def handle_search(self, params):
        q_list = params.get('q')
        if not q_list:
            self.send_error_json(400, 'Search query is required')
            return

        query = q_list[0].strip()
        encoded_query = urllib.parse.quote(query)
        
        # Check ref_only flag (default to True)
        ref_only_list = params.get('ref_only')
        ref_only = True
        if ref_only_list and ref_only_list[0].lower() == 'false':
            ref_only = False

        # Build genomic search URL
        genomic_url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/{encoded_query}/dataset_report"
        if ref_only:
            genomic_url += "?filters.reference_only=true"

        print(f"[NCBI Search] Fetching Genomic: {genomic_url}")

        reports = []
        total_count = 0

        # 1. Try genomic search first
        try:
            req = urllib.request.Request(genomic_url)
            req.add_header('Accept', 'application/json')
            api_key = os.environ.get('NCBI_API_KEY')
            if api_key:
                req.add_header('api-key', api_key)

            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                reports = data.get('reports', [])
                total_count = data.get('total_count', 0)
                
                # Fetch Ensembl metadata
                for report in reports[:5]:
                    sci_name = report.get('organism', {}).get('organism_name')
                    if sci_name:
                        ensembl_data = fetch_ensembl_metadata(sci_name)
                        if ensembl_data:
                            report['ensembl_metadata'] = ensembl_data
        except urllib.error.URLError as e:
            # Network issue (like DNS failed or offline)
            print(f"[Offline Fallback] Network error: {e}. Serving from local cache.")
            self.serve_offline_search(query, ref_only)
            return
        except urllib.error.HTTPError as e:
            # 404 is acceptable, it means no genomic data found, we will try virus fallback
            if e.code != 404:
                print(f"Genomic Search API HTTP Error {e.code}: {e.reason}")
        except Exception as error:
            print("Genomic Search API error:", error)

        # 2. If no reports found from genomic search, try virus search fallback
        if not reports:
            virus_url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/{encoded_query}/dataset_report"
            if ref_only:
                virus_url += "?filter.refseq_only=true"
            
            print(f"[NCBI Search] Falling back to Virus: {virus_url}")
            
            try:
                req = urllib.request.Request(virus_url)
                req.add_header('Accept', 'application/json')
                api_key = os.environ.get('NCBI_API_KEY')
                if api_key:
                    req.add_header('api-key', api_key)

                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    virus_reports = data.get('reports', [])
                    
                    # Annotate virus reports
                    for r in virus_reports:
                        r['is_virus'] = True
                    
                    reports = virus_reports
                    total_count = data.get('total_count', 0)
            except urllib.error.URLError as e:
                print(f"[Offline Fallback Virus] Network error: {e}. Serving from local cache.")
                self.serve_offline_search(query, ref_only)
                return
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    print(f"Virus Search API HTTP Error {e.code}: {e.reason}")
            except Exception as error:
                print("Virus Search API error:", error)

        # Return results to client
        res_data = {
            'reports': reports,
            'total_count': total_count
        }
        self.send_response_json(200, json.dumps(res_data).encode('utf-8'))

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
            api_key = os.environ.get('NCBI_API_KEY')
            if api_key:
                req.add_header('api-key', api_key)

            with urllib.request.urlopen(req) as response:
                data = response.read()
                self.send_response_json(200, data)
        except Exception as error:
            print("Links API error:", error)
            # Send empty links JSON instead of 500 error to keep frontend happy
            self.send_response_json(200, json.dumps({'assembly_links': []}).encode('utf-8'))

    def handle_autocomplete(self, params):
        q_list = params.get('q')
        if not q_list:
            self.send_error_json(400, 'Query is required')
            return

        query = q_list[0].strip()
        encoded_query = urllib.parse.quote(query)
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/taxonomy/{encoded_query}/json?limit=10"

        try:
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/json')
            with urllib.request.urlopen(req, timeout=3) as response:
                data = response.read()
                self.send_response_json(200, data)
        except urllib.error.URLError as error:
            print(f"[Offline Autocomplete] Network error: {error}. Serving local terms.")
            self.serve_offline_autocomplete(query)
        except Exception as error:
            print("Autocomplete API error:", error)
            self.serve_offline_autocomplete(query)

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
