# Reference Genome Fetcher - Web Application

A high-fidelity, zero-dependency bioinformatics web application built with a Python backend and a modern glassmorphic web interface. It allows researchers and students to query, explore, and download official reference genomes and alternative sequenced assemblies (clinical isolates, strains, and cancer cell lines) from the **National Center for Biotechnology Information (NCBI)** and **Ensembl** databases.

---

## 🔬 Scientific Context & Project Scope

In modern genomics and bioinformatics, analyzing genomic variation is critical to understanding disease, mutation rates, and evolutionary pathways. This application is designed to support two main areas of genomic research:

### 1. Reference Genomes vs. Variant Isolates
* **Reference Genomes**: A reference genome (e.g., GRCh38 for humans) is a representative digital sequence of an organism's genome. It acts as a standard coordinate system and gold standard for sequence alignment, annotation, and mapping.
* **Alternative Isolates & Strains**: To study mutations, drug resistance, or pathogenicity, researchers must compare sequence data against the reference genome.
  * *Example (Plasmodium falciparum)*: Malaria research relies on comparing different sequenced strains (like `3D7` vs. chloroquine-resistant `Dd2` or `W2`) to map mutations in the *pfcrt* gene that cause drug resistance.
  * *Example (Cancer Genomics)*: Comparing reference genomes to the sequenced genomes of cancer cell lines (or tumors) reveals somatic mutations, insertions/deletions (indels), and structural variants driving cancer progression.
  * *Toggle functionality*: By turning off the **"Reference Genomes Only"** filter, this application fetches all recorded assemblies for a taxon, giving researchers access to these clinical isolates and mutated strains.

### 2. Eukaryotes, Prokaryotes, and Viruses
NCBI structures genome data differently depending on the domain of life:
* **Eukaryotes & Prokaryotes** are cataloged in the NCBI Assembly database (accessed via `/genome` API routes), which tracks karyotypes, chromosomes, contigs, and assembly levels (chromosome, complete genome, scaffold, contig).
* **Viruses** (e.g., *Coronavirus*, *Hepatitis B virus*) have compact genomes that are tracked in the NCBI Nucleotide database (accessed via `/virus` API routes). They lack traditional eukaryotic "assemblies" but are categorized by completeness, source databases, and Pangolin lineages.
* *Fallback logic*: This application automatically queries the genome database first. If no records are found, it queries the virus database, normalizing the results into a single, cohesive user interface.

---

## ✅ Implementation Status: All Four Features Complete

### 1. ✅ PubChem Taxonomy Autocomplete Search
**Status**: Fully Implemented
- **What it does**: As you type in the search bar, the application queries the PubChem Taxonomy Autocomplete API in real-time
- **Why it matters**: Generic terms like "hepatitis" or "coronavirus" don't map directly to NCBI assemblies. Autocomplete resolves them to canonical species names (e.g., "Hepatitis B virus", "Severe acute respiratory syndrome coronavirus 2")
- **Technical details**:
  - Debounced API calls (250ms) to minimize server load
  - Keyboard navigation: Arrow keys + Enter to select
  - Mouse support: Click suggestions to auto-populate
  - Offline fallback: Local alias database if network fails
  - Dropdown styled with glassmorphic theme matching UI

### 2. ✅ Genome Assembly Quality Metrics (Contig & Scaffold N50)
**Status**: Fully Implemented
- **What it does**: Details modal displays bioinformatic gold-standard quality metrics
- **Metrics displayed**:
  - **Contig N50**: Length of shortest contig covering 50% of genome (higher = more complete)
  - **Scaffold N50**: Same, but for scaffolds (which can span gaps)
  - **Contig/Scaffold Counts**: Fewer components = higher quality, chromosome-level assembly
  - **Ungapped Length**: Total sequenced bases excluding gap spacers
- **Why it matters**: Researchers instantly evaluate assembly completeness without checking NCBI reports separately
- **Example (Human GRCh38.p14)**: Contig N50 = 57.88 Mb, Scaffold N50 = 67.79 Mb (very high quality)

### 3. ✅ Ensembl Database Cross-Reference
**Status**: Fully Implemented
- **What it does**: For eukaryotic genomes, the server queries the Ensembl REST API in parallel with NCBI and displays comparative metadata
- **Metadata displayed**:
  - Ensembl Assembly Name (e.g., `GRCh38.p14`)
  - Assembly Release Date
  - Genebuild Version & Method
  - Last Genebuild Update Date
  - Assembly Authority
- **Why it matters**: Researchers cross-reference annotations across NCBI and Ensembl in a single view
- **Technical details**:
  - 3-second timeout per Ensembl query (non-blocking)
  - Graceful fallback if Ensembl unreachable
  - Only displayed for eukaryotic genomes (not viruses/prokaryotes)

### 4. ✅ Reactive Reference Genome Filter Toggle
**Status**: Fully Implemented
- **What it does**: Toggle "Reference Genomes Only" switch to dynamically re-run searches without manual resubmission
- **Behavior**:
  - **ON (checked)**: Filters to reference assemblies only (gold-standard)
  - **OFF (unchecked)**: Shows all sequenced strains, isolates, clinical specimens
- **Why it matters**: Researchers pivot between reference-based alignment and comparative strain analysis in real-time
- **Example (Plasmodium falciparum)**:
  - **ON**: 1 result (3D7 reference)
  - **OFF**: 70+ results (Dd2, W2, clinical isolates for drug resistance mapping)

---

## 🏗️ System Architecture

The application is structured as a lightweight, single-page application (SPA) backed by a custom proxy server. 

```mermaid
graph TD
    User([User / Researcher]) -->|1. Types Query| UI[Frontend Web UI]
    UI -->|2. Debounced Autocomplete| Autocomplete[PubChem Autocomplete API]
    Autocomplete -->|3. Suggest Species Names| UI
    UI -->|4. Selects Suggestion| LocalServer[Local Python Server]
    LocalServer -->|5. Query Genome API| NCBI_Genome[NCBI Datasets Genome API v2]
    LocalServer -->|6. Query Virus API Fallback| NCBI_Virus[NCBI Datasets Virus API v2]
    LocalServer -->|7. Parallel Cross-Ref| Ensembl[Ensembl REST API]
    NCBI_Genome -->|Genome Report| LocalServer
    NCBI_Virus -->|Virus Report| LocalServer
    Ensembl -->|Comparative Metadata| LocalServer
    LocalServer -->|8. Unified Normalization| UI
    UI -->|9. Render Cards & Modal Stats| User
    
    UI -->|Click Download| NCBIServers[NCBI Servers]
    NCBIServers -->|Direct ZIP Download| User
```

---

## 🛠️ Technology Stack

1. **Backend**:
   - **Python (3.x)**: Uses only Python's built-in standard libraries (`http.server`, `urllib.request`, `urllib.parse`, and `json`).
   - **Zero-Dependency**: No virtual environments (`venv`) or package installations (`pip install`) are required, bypassing dependency issues or network firewalls.
2. **Frontend**:
   - **HTML5**: Structured semantic layout with custom modal overlay containers.
   - **CSS3 (Vanilla)**: Centered layout with glassmorphic elements, glowing visual accents, and subtle animations. Incorporates Google Fonts ("Outfit" and "Fira Code").
   - **JavaScript (Vanilla)**: Handles async API calls, coordinates debounced autocomplete, keyboard selections (Arrow Up/Down + Enter), and normalizes genome statistics.

---

## 🚀 Running the Application

### Prerequisites
* Python 3.10 or higher installed.

### Step-by-Step Launch
1. Clone or download the repository to your local workspace.
2. Open a terminal in the root project folder and run the server:
   ```bash
   python server.py
   ```
3. Open your browser and navigate to:
   [http://localhost:3000](http://localhost:3000)

### (Optional) Adding an NCBI API Key
By default, the NCBI Datasets API limits requests to 5 per second. You can increase this to 10 per second by setting your NCBI API key as an environment variable before starting the server.

* **On Windows (PowerShell)**:
  ```powershell
  $env:NCBI_API_KEY="your_api_key_here"
  python server.py
  ```
* **On macOS / Linux**:
  ```bash
  export NCBI_API_KEY="your_api_key_here"
  python server.py
  ```

---

## 🧬 Scientific Queries to Demonstrate to Your Professor

To demonstrate the application's capabilities, try the following queries:

### 1. **Querying a Reference Eukaryotic Genome with Quality Metrics**:
   * *Search*: `Homo sapiens` (Reference Genomes Only: Checked)
   * *Outcome*: Retrieves the official reference genome (GRCh38.p14) with a size of `3.10 Gb` and 24 chromosomes. In the details modal, check the **Assembly Quality Metrics** section, which displays:
     - **Contig N50**: `57.88 Mb` (measure of assembly continuity)
     - **Scaffold N50**: `67.79 Mb`
     - **Contig Count**: `996` (fewer = higher quality)
   * *Ensembl Cross-Reference*: View the **Ensembl Database Cross-Reference** section showing comparative metadata (GRCh38.p14, assembly date 2013-12, genebuild method, authority, etc.).

### 2. **Autocomplete Search for Ambiguous Terms**:
   * *Search*: Type `hepatitis` in the search bar. The autocomplete dropdown will suggest `Hepatitis B virus`.
   * *Select* the suggestion to automatically fetch the viral genome record.
   * *Outcome*: Returns the complete Hepatitis B virus genome (NC_003977.2) with 3,215 bp.

### 3. **Comparative Genomics (Non-Reference Strains)**:
   * *Search*: `Plasmodium falciparum` (Reference Genomes Only: **Unchecked**)
   * *Outcome*: Retrieves over 70 sequenced strains, including:
     - Reference strain: `Plasmodium falciparum 3D7` (reference assembly)
     - Alternative strains: `Plasmodium falciparum Dd2` (chloroquine-resistant)
     - Alternative strains: `Plasmodium falciparum W2`
   * Researchers can compare Contig/Scaffold N50 metrics across strains to identify which isolates are most suitable for mutation mapping studies.

### 4. **Toggle Reactivity (Reference Genomes Only Filter)**:
   * *Search*: `Mus musculus` (Reference Genomes Only: **Checked** → **Unchecked**)
   * *Outcome*: Toggling the switch dynamically re-runs the search without manual resubmission, showing:
     - **With filter ON**: Only the GRCm39 reference genome
     - **With filter OFF**: All available mouse assemblies (alternative strains, mutant lines, etc.)
   * This enables rapid pivoting between reference-based work and comparative strain analysis.

### 5. **Viral Pathogen Search with Automatic Fallback**:
   * *Search*: `coronavirus` or type and select `Severe acute respiratory syndrome coronavirus 2` from the autocomplete.
   * *Outcome*: The system automatically detects no NCBI genome records exist, falls back to the virus database, and returns SARS-CoV-2 records with:
     - Completeness status (`COMPLETE`)
     - Sequence length (29,903 bp)
     - Direct link to NCBI Nucleotide (`nuccore`) record for mutation tracking

---
