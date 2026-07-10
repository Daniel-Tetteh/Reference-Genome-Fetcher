powershell -Command "
Start-Sleep -Seconds 2
try {
  `$response = Invoke-WebRequest -Uri 'http://localhost:3000/api/search?q=human&ref_only=true' -TimeoutSec 5
  Write-Host 'API Response: OK'
  Write-Host `$response.Content | ConvertFrom-Json | ConvertTo-Json
} catch {
  Write-Host 'API Error: ' `$_.Exception.Message
}
"
