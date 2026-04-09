$ErrorActionPreference = "Stop"

function Get-EnvFromFile {
    param(
        [string]$EnvPath
    )
    $envMap = @{}
    $lines = Get-Content -Path $EnvPath
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed) -or $trimmed.StartsWith("#")) {
            continue
        }
        $parts = $trimmed.Split("=", 2)
        if ($parts.Count -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1]
            $envMap[$key] = $value
        } elseif (-not $trimmed.Contains("=") -and -not $envMap.ContainsKey("GROQ_API_KEY")) {
            # Support files containing only raw key value (e.g., tests/env single line).
            $envMap["GROQ_API_KEY"] = $trimmed
        }
    }
    return $envMap
}

$projectRoot = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $projectRoot ".env"
if (-not (Test-Path $envPath)) {
    $fallback = Join-Path $projectRoot "tests\\env"
    if (Test-Path $fallback) {
        $envPath = $fallback
    } else {
        Write-Output "[FAIL] Test 1: .env file not found at project root and tests/env not found"
        exit 1
    }
}

$envMap = Get-EnvFromFile -EnvPath $envPath
$apiKey = $envMap["GROQ_API_KEY"]
$model = $envMap["GROQ_MODEL"]
if ([string]::IsNullOrWhiteSpace($model)) {
    $model = "llama-3.1-8b-instant"
}

# Test 1: API key exists and looks non-empty.
if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Output "[FAIL] Test 1: GROQ_API_KEY missing or empty in .env"
    exit 1
}
Write-Output "[PASS] Test 1: GROQ_API_KEY is present (value masked)"

$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type"  = "application/json"
}

# Test 2: Groq models endpoint authentication.
try {
    $modelsResp = Invoke-RestMethod -Method Get -Uri "https://api.groq.com/openai/v1/models" -Headers $headers -TimeoutSec 30
    if ($null -eq $modelsResp.data -or $modelsResp.data.Count -lt 1) {
        Write-Output "[FAIL] Test 2: Auth succeeded but no models returned"
        exit 1
    }
    Write-Output "[PASS] Test 2: Models endpoint reachable and authenticated"
} catch {
    Write-Output "[FAIL] Test 2: Models endpoint call failed - $($_.Exception.Message)"
    exit 1
}

# Test 3: Chat completion smoke test.
try {
    $body = @{
        model = $model
        messages = @(
            @{
                role = "user"
                content = "Reply with exactly: GROQ_OK"
            }
        )
        temperature = 0
        max_tokens = 10
    } | ConvertTo-Json -Depth 5

    $chatResp = Invoke-RestMethod -Method Post -Uri "https://api.groq.com/openai/v1/chat/completions" -Headers $headers -Body $body -TimeoutSec 60
    $content = $chatResp.choices[0].message.content
    if ([string]::IsNullOrWhiteSpace($content)) {
        Write-Output "[FAIL] Test 3: Chat completion returned empty content"
        exit 1
    }
    Write-Output "[PASS] Test 3: Chat completion received"
    Write-Output "Sample response: $content"
} catch {
    Write-Output "[FAIL] Test 3: Chat completion failed - $($_.Exception.Message)"
    exit 1
}

Write-Output "All Groq connectivity tests passed."
