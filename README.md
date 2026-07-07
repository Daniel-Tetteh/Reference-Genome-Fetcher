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
