# PowerShell script to defer api.js script loading in all HTML files

$baseDir = "C:/Users/rajpe/.gemini/antigravity/scratch/era_of_siddhas"

# Process each HTML file
Get-ChildItem -Path $baseDir -Filter "*.html" -File | ForEach-Object {
    $filePath = $_.FullName
    $html = Get-Content -Path $filePath -Raw
    $html = $html.Replace("`r`n", "`n")

    # Defer the js/api.js script
    $html = $html.Replace('<script src="js/api.js"></script>', '<script src="js/api.js" defer></script>')

    $html = $html.Replace("`n", "`r`n")
    Set-Content -Path $filePath -Value $html -Encoding UTF8
    Write-Host "Deferred js/api.js in $filePath"
}

Write-Host "Script deferring complete."
