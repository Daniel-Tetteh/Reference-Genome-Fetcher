// DOM Elements
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const clearBtn = document.getElementById('clear-btn');
const loader = document.getElementById('loader');
const errorContainer = document.getElementById('error-container');
const errorMessage = document.getElementById('error-message');
const emptyState = document.getElementById('empty-state');
const resultsGrid = document.getElementById('results-grid');

// Modal Elements
const detailsModal = document.getElementById('details-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const modalOrgCommon = document.getElementById('modal-org-common');
const modalOrgScientific = document.getElementById('modal-org-scientific');
const modalStatSize = document.getElementById('modal-stat-size');
const modalStatGc = document.getElementById('modal-stat-gc');
const modalStatChroms = document.getElementById('modal-stat-chroms');
const modalStatTaxid = document.getElementById('modal-stat-taxid');
const modalMetaAssemblyName = document.getElementById('modal-meta-assembly-name');
const modalMetaAccession = document.getElementById('modal-meta-accession');
const modalMetaStatusLevel = document.getElementById('modal-meta-status-level');
const modalMetaReleaseDate = document.getElementById('modal-meta-release-date');
const modalMetaSubmitter = document.getElementById('modal-meta-submitter');
const modalMetaBioproject = document.getElementById('modal-meta-bioproject');
const modalMetaRefseqCat = document.getElementById('modal-meta-refseq-cat');
const modalOrganelleRow = document.getElementById('modal-organelle-row');
const modalMetaOrganelle = document.getElementById('modal-meta-organelle');
const modalActionsButtons = document.getElementById('modal-actions-buttons');

// Global cache for assemblies in the current search
let currentSearchAssemblies = [];

/* ==========================================================================
   Helper Functions
   ========================================================================== */

// Format genome size (bases) into a readable format (Gb, Mb, Kb)
function formatGenomeSize(bases) {
  if (!bases) return 'N/A';
  const num = parseInt(bases, 10);
  if (isNaN(num)) return 'N/A';
  if (num >= 1e9) return `${(num / 1e9).toFixed(2)} Gb`;
  if (num >= 1e6) return `${(num / 1e6).toFixed(2)} Mb`;
  if (num >= 1e3) return `${(num / 1e3).toFixed(2)} Kb`;
  return `${num} bp`;
}

// Format numbers with commas (e.g. 1000 -> 1,000)
function formatNumber(num) {
  if (num === null || num === undefined) return 'N/A';
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Date formatter
function formatDate(dateStr) {
  if (!dateStr) return 'N/A';
  try {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateStr).toLocaleDateString(undefined, options);
  } catch (e) {
    return dateStr;
  }
}

/* ==========================================================================
   Search & API Functions
   ========================================================================== */

// Perform Search
async function performSearch(query) {
  if (!query || !query.trim()) return;
  
  // Show loading state
  showElement(loader);
  hideElement(resultsGrid);
  hideElement(emptyState);
  hideElement(errorContainer);
  clearBtn.style.display = 'flex';
  
  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    if (!res.ok) {
      throw new Error(`NCBI Search failed (HTTP status ${res.status})`);
    }
    
    const data = await res.json();
    currentSearchAssemblies = data.reports || [];
    
    renderResults(currentSearchAssemblies, query);
  } catch (error) {
    console.error('Search error:', error);
    errorMessage.textContent = error.message || 'An error occurred while fetching assembly details.';
    showElement(errorContainer);
    hideElement(loader);
  }
}

// Render Results Grid
function renderResults(assemblies, query) {
  hideElement(loader);
  resultsGrid.innerHTML = '';
  
  if (assemblies.length === 0) {
    // Show empty state with 'no results' message
    emptyState.querySelector('h3').textContent = 'No Reference Genomes Found';
    emptyState.querySelector('p').textContent = `We couldn't find any official reference genomes for "${query}". Try searching a different organism.`;
    emptyState.querySelector('.empty-icon').textContent = '🔍';
    showElement(emptyState);
    return;
  }
  
  // Render cards
  assemblies.forEach(report => {
    const card = createGenomeCard(report);
    resultsGrid.appendChild(card);
  });
  
  showElement(resultsGrid);
}

// Create Card Element for Grid
function createGenomeCard(report) {
  const card = document.createElement('div');
  card.className = 'genome-card';
  
  const commonName = report.organism?.common_name || '';
  const scientificName = report.organism?.organism_name || 'Unknown Species';
  const accession = report.accession;
  const assemblyName = report.assembly_info?.assembly_name || 'N/A';
  const taxId = report.organism?.tax_id || 'N/A';
  
  const size = report.assembly_stats?.total_sequence_length;
  const gcPercent = report.assembly_stats?.gc_percent;
  const chromosomes = report.assembly_stats?.total_number_of_chromosomes;
  const level = report.assembly_info?.assembly_level || 'N/A';
  const releaseDate = report.assembly_info?.release_date;
  
  // Direct Download Link
  const downloadUrl = `https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/${accession}/download?include_annotation_type=GENOME_FASTA`;
  
  card.innerHTML = `
    <div class="card-header">
      <div class="card-org-names">
        <h3 class="card-scientific" title="${scientificName}">${scientificName}</h3>
        ${commonName ? `<span class="card-common">${commonName}</span>` : ''}
      </div>
      <div class="card-badges">
        <span class="badge badge-accession">${accession}</span>
        <span class="badge badge-taxid">TaxID: ${taxId}</span>
        <span class="badge badge-level">${level}</span>
      </div>
    </div>
    
    <div class="card-stats">
      <div class="stat-item">
        <span class="stat-label">Genome Size</span>
        <span class="stat-value">${formatGenomeSize(size)}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">GC Content</span>
        <span class="stat-value">${gcPercent ? gcPercent + '%' : 'N/A'}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Chromosomes</span>
        <span class="stat-value">${chromosomes ? formatNumber(chromosomes) : 'N/A'}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Released</span>
        <span class="stat-value">${formatDate(releaseDate)}</span>
      </div>
    </div>
    
    <div class="card-actions">
      <a href="${downloadUrl}" class="btn btn-primary" download>
        <span>📥 Download Genome ZIP</span>
      </a>
      <button class="btn btn-secondary details-btn" data-accession="${accession}">
        <span>🔬 View Details & Links</span>
      </button>
    </div>
  `;
  
  // Event listener for details modal
  card.querySelector('.details-btn').addEventListener('click', () => {
    openDetailsModal(report);
  });
  
  return card;
}

// Fetch links and populate details modal
async function openDetailsModal(report) {
  const accession = report.accession;
  
  // Setup loading state on actions block
  modalActionsButtons.innerHTML = '<div class="spinner" style="width: 24px; height: 24px; margin: 0 auto;"></div>';
  
  // Basic info population immediately
  modalOrgCommon.textContent = report.organism?.common_name ? report.organism.common_name.toUpperCase() : 'ORGANISM';
  modalOrgScientific.textContent = report.organism?.organism_name || 'Unknown Organism';
  
  modalStatSize.textContent = formatGenomeSize(report.assembly_stats?.total_sequence_length);
  modalStatGc.textContent = report.assembly_stats?.gc_percent ? report.assembly_stats.gc_percent + '%' : 'N/A';
  modalStatChroms.textContent = report.assembly_stats?.total_number_of_chromosomes || 'N/A';
  modalStatTaxid.textContent = report.organism?.tax_id || 'N/A';
  
  modalMetaAssemblyName.textContent = report.assembly_info?.assembly_name || 'N/A';
  modalMetaAccession.textContent = accession;
  modalMetaStatusLevel.textContent = `${report.assembly_info?.assembly_level || 'N/A'} (${report.assembly_info?.assembly_status || 'current'})`;
  modalMetaReleaseDate.textContent = formatDate(report.assembly_info?.release_date);
  modalMetaSubmitter.textContent = report.assembly_info?.submitter || 'N/A';
  modalMetaBioproject.textContent = report.assembly_info?.bioproject_accession || 'N/A';
  modalMetaRefseqCat.textContent = report.assembly_info?.refseq_category || 'N/A';
  
  // Organelle Info handling
  if (report.organelle_info && report.organelle_info.length > 0) {
    modalOrganelleRow.classList.remove('hidden');
    const descriptions = report.organelle_info.map(o => `${o.description || 'Organelle'} (${formatGenomeSize(o.total_seq_length)})`);
    modalMetaOrganelle.textContent = descriptions.join(', ');
  } else {
    modalOrganelleRow.classList.add('hidden');
  }
  
  // Open modal UI
  showModal();

  // Load links asynchronously
  try {
    const res = await fetch(`/api/links?accession=${encodeURIComponent(accession)}`);
    if (!res.ok) throw new Error('Links fetch failed');
    const data = await res.json();
    
    // Parse links
    const links = data.assembly_links || [];
    const ftpLinkObj = links.find(l => l.assembly_link_type === 'FTP_LINK');
    const ftpUrl = ftpLinkObj ? ftpLinkObj.resource_link : null;
    
    // Direct link to assembly db on NCBI
    const ncbiDbUrl = `https://www.ncbi.nlm.nih.gov/assembly/${accession}`;
    const zipDownloadUrl = `https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/${accession}/download?include_annotation_type=GENOME_FASTA`;
    
    let actionButtonsHtml = `
      <a href="${zipDownloadUrl}" class="btn btn-primary">
        <span>📥 Download ZIP (FASTA)</span>
      </a>
    `;
    
    if (ftpUrl) {
      actionButtonsHtml += `
        <a href="${ftpUrl}" class="btn btn-secondary" target="_blank" rel="noopener noreferrer">
          <span>📂 Browse FTP Directory</span>
        </a>
      `;
    }
    
    actionButtonsHtml += `
      <a href="${ncbiDbUrl}" class="btn btn-secondary" target="_blank" rel="noopener noreferrer">
        <span>🌐 NCBI Assembly Page</span>
      </a>
    `;
    
    modalActionsButtons.innerHTML = actionButtonsHtml;
  } catch (err) {
    console.error('Error fetching links:', err);
    // Fallback links if API fails
    const zipDownloadUrl = `https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/${accession}/download?include_annotation_type=GENOME_FASTA`;
    modalActionsButtons.innerHTML = `
      <a href="${zipDownloadUrl}" class="btn btn-primary">
        <span>📥 Download ZIP (FASTA)</span>
      </a>
      <a href="https://www.ncbi.nlm.nih.gov/assembly/${accession}" class="btn btn-secondary" target="_blank" rel="noopener noreferrer">
        <span>🌐 NCBI Assembly Page</span>
      </a>
    `;
  }
}

/* ==========================================================================
   UI Controls
   ========================================================================== */

function showElement(el) {
  el.classList.remove('hidden');
}

function hideElement(el) {
  el.classList.add('hidden');
}

function showModal() {
  detailsModal.classList.remove('hidden');
  detailsModal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden'; // Disable page scrolling
}

function closeModal() {
  detailsModal.classList.add('hidden');
  detailsModal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = ''; // Enable page scrolling
}

/* ==========================================================================
   Event Listeners
   ========================================================================== */

// Search submit
searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const query = searchInput.value.trim();
  performSearch(query);
});

// Clear input
clearBtn.addEventListener('click', () => {
  searchInput.value = '';
  clearBtn.style.display = 'none';
  hideElement(resultsGrid);
  hideElement(errorContainer);
  
  // Reset empty state
  emptyState.querySelector('h3').textContent = 'No Organism Selected';
  emptyState.querySelector('p').textContent = 'Enter an organism\'s name above or click on one of the quick suggestions to explore reference genome assemblies.';
  emptyState.querySelector('.empty-icon').textContent = '🌍';
  showElement(emptyState);
});

// Input field change listener (show clear button)
searchInput.addEventListener('input', () => {
  if (searchInput.value.length > 0) {
    clearBtn.style.display = 'flex';
  } else {
    clearBtn.style.display = 'none';
  }
});

// Suggestion chips
document.querySelectorAll('.chip-btn').forEach(button => {
  button.addEventListener('click', (e) => {
    const query = e.currentTarget.getAttribute('data-query');
    searchInput.value = query;
    performSearch(query);
  });
});

// Modal close button
closeModalBtn.addEventListener('click', closeModal);

// Modal close click outside
detailsModal.addEventListener('click', (e) => {
  if (e.target === detailsModal) {
    closeModal();
  }
});

// Escape key to close modal
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !detailsModal.classList.contains('hidden')) {
    closeModal();
  }
});
