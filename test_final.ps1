powershell -Command "
Write-Host '==== FINAL VERIFICATION ===='
Write-Host ''
Write-Host 'Browser Test Instructions:' -ForegroundColor Yellow
Write-Host '1. Open http://localhost:3000'
Write-Host '2. Search: Plasmodium falciparum'
Write-Host '3. Click Reference Genome button'
Write-Host '   -> Expected: 1 card (only 3D7 reference)'
Write-Host '4. Click Other Sequences button'
Write-Host '   -> Expected: 78+ cards (excluding reference)'
Write-Host '5. Toggle back to Reference Genome'
Write-Host '   -> Expected: 1 card again'
Write-Host ''
Write-Host 'Implementation Details:' -ForegroundColor Cyan
Write-Host '- Reference Genome: Uses API ref_only=true'
Write-Host '- Other Sequences: Filters out reference genomes client-side'
Write-Host ''
Write-Host 'Tests ready!' -ForegroundColor Green
"
