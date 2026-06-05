# PowerShell script to add JSON‑LD structured data (EducationalContent) to all HTML pages

$baseDir = "C:/Users/rajpe/.gemini/antigravity/scratch/era_of_siddhas"

function Ensure-JsonLd {
    param([string]$html, [string]$jsonLd)
    if ($html -notmatch [regex]::Escape($jsonLd)) {
        # Insert before closing </head>
        $html = $html -replace "</head>", "$jsonLd`n</head>"
    }
    return $html
}

Get-ChildItem -Path $baseDir -Filter "*.html" -File | ForEach-Object {
    $filePath = $_.FullName
    $html = Get-Content -Path $filePath -Raw

    # Extract page title for schema (fallback to file name)
    if ($html -match "<title>([^<]+)</title>") {
        $title = $matches[1].Trim()
    } else {
        $title = [System.IO.Path]::GetFileNameWithoutExtension($filePath)
    }

    $json = @"
<script type=\"application/ld+json\">
{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"CreativeWork\",\n  \"name\": \"$title\",\n  \"description\": \"Educational content about the Vedic Siddha tradition and its integration with modern science.\",\n  \"url\": \"https://example.com/$(Split-Path -Leaf $filePath)\"\n}\n</script>
"@

    $html = Ensure-JsonLd -html $html -jsonLd $json
    Set-Content -Path $filePath -Value $html -Encoding UTF8
    Write-Host "Added JSON‑LD to $filePath"
}

Write-Host "JSON‑LD insertion complete."
