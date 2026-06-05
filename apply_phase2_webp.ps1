# PowerShell script to update HTML files to use <picture> tag with WebP source and PNG fallback

$baseDir = "C:/Users/rajpe/.gemini/antigravity/scratch/era_of_siddhas"

# Process each HTML file
Get-ChildItem -Path $baseDir -Filter "*.html" -File | ForEach-Object {
    $filePath = $_.FullName
    $html = Get-Content -Path $filePath -Raw
    # Normalize line endings
    $html = $html.Replace("`r`n", "`n")

    # Regular expression to match img tags with .png source and wrap them in a picture tag
    # Checks that it isn't already wrapped in a <picture> tag
    # Regex details:
    # (?<!<picture[^>]*>\s*?(?:<source[^>]*>\s*?)*?) matches if not preceded by <picture>...
    # <img([^>]*?)src="([^"]+?)\.png"([^>]*?)> matches <img ... src="name.png" ...>
    $pattern = '(?s)(?<!<picture[^>]*>\s*?(?:<source[^>]*>\s*?)*?)<img([^>]*?)src="([^"]+?)\.png"([^>]*?)>'
    
    # We do a match and replace using regex
    $html = [regex]::Replace($html, $pattern, {
        param($match)
        $attrsBefore = $match.Groups[1].Value
        $imgBaseName = $match.Groups[2].Value
        $attrsAfter = $match.Groups[3].Value
        
        # Build the picture element
        return "<picture><source srcset=""$imgBaseName.webp"" type=""image/webp""><img$attrsBefore`src=""$imgBaseName.png""$attrsAfter></picture>"
    })

    # Restore CRLF line endings
    $html = $html.Replace("`n", "`r`n")

    Set-Content -Path $filePath -Value $html -Encoding UTF8
    Write-Host "WebP serving wrappers applied to $filePath"
}

Write-Host "WebP HTML updates complete."
