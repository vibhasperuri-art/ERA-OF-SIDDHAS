# PowerShell script to apply Phase 1 quick‑win updates to all HTML files in the project

# Directory containing the HTML files
$baseDir = "C:/Users/rajpe/.gemini/antigravity/scratch/era_of_siddhas"

function Ensure-MetaTag {
    param(
        [string]$content,
        [string]$metaTag
    )
    if ($content -notmatch [regex]::Escape($metaTag)) {
        $content = $content -replace "</head>", "$metaTag`n</head>"
    }
    return $content
}

# SEO meta tags (single‑quoted to avoid escaping)
$metaTags = @(
    '<meta name="description" content="Era of Siddhas – A Vedic Gurukula platform integrating ancient Indian knowledge systems with modern STEM education."/>' ,
    '<meta name="keywords" content="Siddha, Vedic education, ancient architecture, Vastu Shastra, Nagara Nirmāṇa, Vimāna Śāstra, Astra Vidyā, Rasa Śāstra, Jyotiṣa, STEM"/>' ,
    '<meta property="og:title" content="Era of Siddhas — The Architecture of Siddha Vidyā"/>' ,
    '<meta property="og:description" content="Explore the Five Pillars of Siddha Vidyā and their integration with modern scientific inquiry."/>' ,
    '<meta property="og:type" content="website"/>' ,
    '<meta property="og:url" content="https://example.com/"/>' ,
    '<meta name="twitter:card" content="summary_large_image"/>' ,
    '<meta name="twitter:title" content="Era of Siddhas — The Architecture of Siddha Vidyā"/>' ,
    '<meta name="twitter:description" content="Explore Vedic sciences and modern STEM in a unified learning platform."/>'
)

Get-ChildItem -Path $baseDir -Filter "*.html" -File | ForEach-Object {
    $filePath = $_.FullName
    $html = Get-Content -Path $filePath -Raw

    # Add SEO meta tags
    foreach ($tag in $metaTags) {
        $html = Ensure-MetaTag -content $html -metaTag $tag
    }

    # Insert skip‑to‑content link after <body>
    if ($html -match '<body[^>]*>') {
        $skip = '<a href="#main-content" class="skip-link" style="position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;">Skip to main content</a>'
        $html = $html -replace '(<body[^>]*>)', "`$1`n$skip"
    }

    # Ensure main‑content landmark
    if ($html -match '<main[^>]*>') {
        $html = $html -replace '<main', '<main id="main-content"'
    } else {
        $html = $html -replace '(<section[^>]*>)', '<div id="main-content">`n$1'
        $html = $html -replace '(</section>)', '$1`n</div>'
    }

    # Breadcrumb navigation after <header> (or after <body> if no header)
    $breadcrumb = "<nav aria-label='Breadcrumb' class='breadcrumb-nav'>
  <ol style='display:flex;gap:0.5rem;list-style:none;padding:0;margin:0;'>
    <li><a href='index.html'>Home</a></li>
    <li aria-current='page'>$(Split-Path -Leaf $filePath)</li>
  </ol>
</nav>"
    if ($html -match '(<header[^>]*>.*?</header>)') {
        $html = $html -replace '(<header[^>]*>.*?</header>)', "`$1`n$breadcrumb"
    } else {
        $html = $html -replace '(<body[^>]*>)', "`$1`n$breadcrumb"
    }

    # Lazy‑load images and ensure alt attribute
    $html = $html -replace '<img([^>]*?)>', {
        $attrs = $args[0].Groups[1].Value
        if ($attrs -notmatch 'loading=') { $attrs += ' loading="lazy"' }
        if ($attrs -notmatch 'decoding=') { $attrs += ' decoding="async"' }
        if ($attrs -notmatch 'alt=') { $attrs += ' alt="Image"' }
        return "<img$attrs>"
    }

    # Replace [citation] placeholder with collapsible details block
    $html = $html -replace '\[citation\]', '<details><summary>Reference</summary><p>Full citation details go here.</p></details>'

    Set-Content -Path $filePath -Value $html -Encoding UTF8
    Write-Host "Updated $filePath"
}

Write-Host "Phase 1 quick‑win updates have been applied to all HTML files."
