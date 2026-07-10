powershell -Command "
Write-Host '==== TESTING REFERENCE GENOME FETCHER ===='
Write-Host ''

# Test 1: Search with reference genome filter
Write-Host '[TEST 1] Search Plasmodium falciparum (Reference Genomes Only)' -ForegroundColor Cyan
try {
  `$r1 = Invoke-WebRequest -Uri 'http://localhost:3000/api/search?q=plasmodium%20falciparum&ref_only=true' -TimeoutSec 10
  `$data1 = `$r1.Content | ConvertFrom-Json
  Write-Host 'Result: ' `$data1.total_count ' records' -ForegroundColor Green
  if (`$data1.reports -and `$data1.reports[0]) {
    Write-Host 'First: ' `$data1.reports[0].organism.organism_name
  }
} catch {
  Write-Host 'FAILED: ' `$_.Exception.Message -ForegroundColor Red
}

Write-Host ''

# Test 2: Search all sequences
Write-Host '[TEST 2] Search Plasmodium falciparum (All Sequences)' -ForegroundColor Cyan
try {
  `$r2 = Invoke-WebRequest -Uri 'http://localhost:3000/api/search?q=plasmodium%20falciparum&ref_only=false' -TimeoutSec 10
  `$data2 = `$r2.Content | ConvertFrom-Json
  Write-Host 'Result: ' `$data2.total_count ' records' -ForegroundColor Green
} catch {
  Write-Host 'FAILED: ' `$_.Exception.Message -ForegroundColor Red
}

Write-Host ''

# Test 3: Autocomplete
Write-Host '[TEST 3] Autocomplete Query (hepatitis)' -ForegroundColor Cyan
try {
  `$r3 = Invoke-WebRequest -Uri 'http://localhost:3000/api/autocomplete?q=hepatitis' -TimeoutSec 5
  `$data3 = `$r3.Content | ConvertFrom-Json
  `$terms = `$data3.dictionary_terms.taxonomy
  Write-Host 'Result: ' `$terms.Count ' suggestions' -ForegroundColor Green
  Write-Host 'Top 3:'
  `$terms | Select-Object -First 3 | ForEach-Object { Write-Host '  - ' `$_ }
} catch {
  Write-Host 'FAILED: ' `$_.Exception.Message -ForegroundColor Red
}

Write-Host ''
Write-Host '==== ALL TESTS COMPLETE ====' -ForegroundColor Green
"
