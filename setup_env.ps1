# Securely create a .env file with your OpenWeatherMap API key
# Usage: run this from the project root in PowerShell:
#   .\setup_env.ps1

$pwdPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path $pwdPath

Write-Host "This will create a .env file in: " (Get-Location)

# Read as secure string and convert to plain text temporarily
$secure = Read-Host "Enter OPENWEATHER_API_KEY (input hidden)" -AsSecureString
$ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try {
    $key = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
} finally {
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
}

if (-not $key) {
    Write-Host "No key entered; aborting." -ForegroundColor Yellow
    exit 1
}

$envText = "OPENWEATHER_API_KEY=$key"
$envFile = Join-Path (Get-Location) ".env"

if (Test-Path $envFile) {
    $confirm = Read-Host ".env already exists. Overwrite? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Host "Aborted. .env not changed." -ForegroundColor Yellow
        exit 0
    }
}

$envText | Out-File -Encoding utf8 -FilePath $envFile
Write-Host ".env created at $envFile" -ForegroundColor Green
Write-Host "Note: .env is in .gitignore by default; don't commit your API key to git." -ForegroundColor Cyan
