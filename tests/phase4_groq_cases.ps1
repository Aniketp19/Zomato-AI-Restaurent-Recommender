$ErrorActionPreference = "Stop"

function Read-EnvMap {
    param([string]$Path)
    $map = @{}
    if (-not (Test-Path $Path)) { return $map }
    foreach ($line in (Get-Content $Path)) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed) -or $trimmed.StartsWith("#")) { continue }
        if ($trimmed.Contains("=")) {
            $parts = $trimmed.Split("=", 2)
            $map[$parts[0].Trim()] = $parts[1]
        }
    }
    return $map
}

function Invoke-GroqRankCase {
    param(
        [hashtable]$Headers,
        [string]$Model,
        [string]$CaseName,
        [hashtable]$Profile,
        [array]$Candidates,
        [int]$TopK
    )

    $promptPayload = @{
        user_profile = $Profile
        candidates = $Candidates
        instructions = @{
            task = "Rank restaurants and explain suitability for user."
            strict_rules = @(
                "Use ONLY restaurants listed in candidates.",
                "Do not invent restaurants, ratings, cuisines, or costs.",
                "Return valid JSON only."
            )
            output_schema = @{
                recommendations = @(
                    @{
                        restaurant_id = "string"
                        name = "string"
                        cuisine = "string"
                        rating = "number"
                        estimated_cost = "number"
                        explanation = "string"
                    }
                )
                summary = "string"
            }
        }
    } | ConvertTo-Json -Depth 8

    $body = @{
        model = $Model
        messages = @(
            @{ role = "system"; content = "Return strict JSON only." },
            @{ role = "user"; content = $promptPayload }
        )
        temperature = 0.2
        max_tokens = 800
        response_format = @{ type = "json_object" }
    } | ConvertTo-Json -Depth 8

    $resp = Invoke-RestMethod -Method Post -Uri "https://api.groq.com/openai/v1/chat/completions" -Headers $Headers -Body $body -TimeoutSec 60
    $content = $resp.choices[0].message.content
    $parsed = $content | ConvertFrom-Json

    if ($null -eq $parsed.recommendations) { throw "[$CaseName] Missing recommendations array" }
    if ($parsed.recommendations.Count -lt 1) { throw "[$CaseName] Empty recommendations" }

    $allowedIds = @{}
    foreach ($c in $Candidates) { $allowedIds[$c.restaurant_id] = $true }
    $count = 0
    foreach ($rec in $parsed.recommendations) {
        $count += 1
        if ($count -gt $TopK) { break }
        if (-not $allowedIds.ContainsKey([string]$rec.restaurant_id)) {
            throw "[$CaseName] Grounding failed: hallucinated id $($rec.restaurant_id)"
        }
        if ([string]::IsNullOrWhiteSpace([string]$rec.explanation)) {
            throw "[$CaseName] Missing explanation for $($rec.restaurant_id)"
        }
    }
    Write-Output "[PASS] $CaseName"
}

$root = Split-Path -Parent $PSScriptRoot
$envMap = Read-EnvMap -Path (Join-Path $root ".env")
if (-not $envMap.ContainsKey("GROQ_API_KEY")) {
    throw "GROQ_API_KEY not found in .env"
}
$model = if ($envMap.ContainsKey("GROQ_MODEL") -and -not [string]::IsNullOrWhiteSpace($envMap["GROQ_MODEL"])) { $envMap["GROQ_MODEL"] } else { "llama-3.1-8b-instant" }
$headers = @{
    "Authorization" = "Bearer $($envMap["GROQ_API_KEY"])"
    "Content-Type" = "application/json"
}

# Case 1: Italian, medium budget
$candidates1 = @(
    @{ restaurant_id="r1"; name="Pasta Hub"; city="Bangalore"; cuisines=@("Italian"); rating=4.6; estimated_cost=1200; budget_bucket="medium"; tags=@("family-friendly") },
    @{ restaurant_id="r2"; name="Slice Town"; city="Bangalore"; cuisines=@("Italian","Pizza"); rating=4.4; estimated_cost=1000; budget_bucket="medium"; tags=@("quick service") },
    @{ restaurant_id="r3"; name="Dragon Bowl"; city="Bangalore"; cuisines=@("Chinese"); rating=4.5; estimated_cost=1100; budget_bucket="medium"; tags=@() }
)
Invoke-GroqRankCase -Headers $headers -Model $model -CaseName "Case 1 Italian medium budget" -Profile @{ preferred_city="Bangalore"; budget_bucket="medium"; cuisine_tokens=@("Italian"); rating_floor=4.0; extra_tags=@("family-friendly") } -Candidates $candidates1 -TopK 2

# Case 2: Low budget Chinese
$candidates2 = @(
    @{ restaurant_id="r10"; name="Noodle Spot"; city="Delhi"; cuisines=@("Chinese"); rating=4.2; estimated_cost=600; budget_bucket="low"; tags=@("quick service") },
    @{ restaurant_id="r11"; name="Rice Wok"; city="Delhi"; cuisines=@("Chinese","Thai"); rating=4.0; estimated_cost=550; budget_bucket="low"; tags=@() },
    @{ restaurant_id="r12"; name="Urban Grill"; city="Delhi"; cuisines=@("BBQ"); rating=4.7; estimated_cost=1700; budget_bucket="high"; tags=@("family-friendly") }
)
Invoke-GroqRankCase -Headers $headers -Model $model -CaseName "Case 2 Chinese low budget" -Profile @{ preferred_city="Delhi"; budget_bucket="low"; cuisine_tokens=@("Chinese"); rating_floor=3.8; extra_tags=@("quick service") } -Candidates $candidates2 -TopK 2

# Case 3: High budget mixed cuisine
$candidates3 = @(
    @{ restaurant_id="r20"; name="Royal Feast"; city="Mumbai"; cuisines=@("North Indian","Mughlai"); rating=4.8; estimated_cost=2400; budget_bucket="high"; tags=@("family-friendly") },
    @{ restaurant_id="r21"; name="Sea Pearl"; city="Mumbai"; cuisines=@("Seafood"); rating=4.7; estimated_cost=2600; budget_bucket="high"; tags=@("fine dining") },
    @{ restaurant_id="r22"; name="Cafe Lite"; city="Mumbai"; cuisines=@("Cafe"); rating=4.3; estimated_cost=900; budget_bucket="medium"; tags=@("quick service") }
)
Invoke-GroqRankCase -Headers $headers -Model $model -CaseName "Case 3 high budget premium" -Profile @{ preferred_city="Mumbai"; budget_bucket="high"; cuisine_tokens=@("Seafood","Mughlai"); rating_floor=4.2; extra_tags=@("family-friendly") } -Candidates $candidates3 -TopK 2

Write-Output "All 3 Phase 4 Groq test cases passed."
