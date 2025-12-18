# setup_gemini_mcp.ps1
# PowerShell script to set up Gemini MCP server on Windows

Write-Host "=== Gemini MCP Server Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.9+ first." -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install fastmcp google-genai

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "Dependencies installed successfully" -ForegroundColor Green

# Get API key
Write-Host ""
Write-Host "=== API Key Setup ===" -ForegroundColor Cyan
Write-Host "Get your API key from: https://aistudio.google.com/apikey"
Write-Host ""
$apiKey = Read-Host "Enter your Gemini API key"

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host "No API key provided. You'll need to add it manually to settings." -ForegroundColor Yellow
    $apiKey = "YOUR_API_KEY_HERE"
}

# Get script path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverPath = Join-Path $scriptDir "gemini_mcp_server.py"

# Generate Claude settings snippet
Write-Host ""
Write-Host "=== Claude Code Configuration ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Add this to your ~/.claude/settings.json (or %USERPROFILE%\.claude\settings.json):" -ForegroundColor Yellow
Write-Host ""

$settingsJson = @"
{
  "mcpServers": {
    "gemini": {
      "command": "python",
      "args": ["$($serverPath -replace '\\', '\\\\')"],
      "env": {
        "GEMINI_API_KEY": "$apiKey"
      }
    }
  }
}
"@

Write-Host $settingsJson -ForegroundColor White
Write-Host ""

# Test the server
Write-Host "=== Testing Server ===" -ForegroundColor Cyan
Write-Host "Testing Gemini connection..." -ForegroundColor Yellow

$env:GEMINI_API_KEY = $apiKey
$testResult = python -c "from google import genai; c = genai.Client(api_key='$apiKey'); print('Connection successful!')" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Gemini API connection successful!" -ForegroundColor Green
} else {
    Write-Host "Warning: Could not verify API connection. Error: $testResult" -ForegroundColor Yellow
    Write-Host "The server may still work - try it in Claude Code." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Add the JSON config above to ~/.claude/settings.json"
Write-Host "2. Restart Claude Code"
Write-Host "3. The gemini tools will be available as mcp__gemini__*"
Write-Host ""
