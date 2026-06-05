$BaseDir = "C:/Users/rajpe/.gemini/antigravity/scratch/era_of_siddhas"

# SEO meta definitions per file (using single quotes for safety)
$PageMeta = @{
    "index.html" = @{
        description = 'Era of Siddhas — A Vedic Gurukula platform integrating ancient Indian knowledge systems with modern STEM education.'
        keywords    = 'Siddha, Vedic education, ancient architecture, Vastu Shastra, Nagara Nirmāṇa, Vimāna Śāstra, Astra Vidyā, Rasa Śāstra, Jyotiṣa, STEM'
        title       = 'Era of Siddhas — The Architecture of Siddha Vidyā'
    }
    "pillar_hub.html" = @{
        description = 'Explore the Three Pillars of Siddha Vidyā: Nagara Nirmāṇa, Rājya Palanam, Yuddham — bridging Vedic sciences with modern research.'
        keywords    = 'Siddha, Vedic education, Nagara Nirmāṇa, Rājya Palanam, Yuddham, Vastu, Yoga, Upasana, Upanishads, STEM'
        title       = 'Era of Siddhas — The Three Pillars'
    }
    "course_hub.html" = @{
        description = 'Structured Gurukula courses across five Vedic science pillars with graded progression from Mumukṣu to Siddha levels.'
        keywords    = 'Siddha, courses, Vedic education, pillars, curriculum, STEM'
        title       = 'Era of Siddhas — Courses'
    }
    "wisdom_hub.html" = @{
        description = 'Wisdom Publications Hub — magazines, research articles, Itihāsa & Purāṇa stories, and modern scientific validations of ancient Indian sciences.'
        keywords    = 'Siddha, wisdom, publications, articles, research, Vedic science'
        title       = 'Era of Siddhas — Wisdom Hub'
    }
    "interactive_lesson.html" = @{
        description = 'Interactive Vedic science lessons with scriptural sources, STEM correlations, and guided Socratic reflection exercises.'
        keywords    = 'Siddha, lessons, interactive, Vedic science, education'
        title       = 'Era of Siddhas — Interactive Lesson'
    }
    "chanting.html" = @{
        description = 'Sacred mantra chanting practice with audio guidance, transliteration, and meaning for daily sādhana.'
        keywords    = 'Siddha, chanting, mantra, audio, practice'
        title       = 'Era of Siddhas — Chanting'
    }
    "sangha.html" = @{
        description = 'The Saṅgha — Community feed for shared reflections, insights, and collective wisdom from seekers on the path.'
        keywords    = 'Siddha, sangha, community, reflections'
        title       = 'Era of Siddhas — The Saṅgha'
    }
    "vicara_sannidhi.html" = @{
        description = 'Vicāra Sannidhi — The Inner Sanctum of Inquiry. Engage in Socratic dialogue with the Guru AI to deepen your understanding of each pillar.'
        keywords    = 'Siddha, AI, dialogue, inquiry, guru AI'
        title       = 'Era of Siddhas — Vicāra Sannidhi'
    }
    "admin.html" = @{
        description = 'Gurukula Administration — Manage seekers, publish content, broadcast announcements, and monitor the Saṅgha.'
        keywords    = 'Siddha, admin, management, dashboard'
        title       = 'Era of Siddhas — Admin'
    }
}

# Devanagari to IAST mapping (Phase 1 – IAST shown only)
$DevanagariToIAST = @{
    "नगर निर्माण" = 'Nagara Nirmāṇa'
    "राज्य पालनम्" = 'Rājya Palanam'
    "युद्धम्"   = 'Yuddham'
    "शास्त्र"    = 'Śāstra'
    "विमान शास्त्र" = 'Vimāna Śāstra'
    "रसायन शास्त्र" = 'Rasāśāstra'
}

function Insert-MetaTags {
    param($Content, $FileName)
    if (-not $PageMeta.ContainsKey($FileName)) { return $Content }
    $meta = $PageMeta[$FileName]
    $tags = @(
        "<meta name=`"description`" content=`"$($meta.description)`">",
        "<meta name=`"keywords`" content=`"$($meta.keywords)`">",
        "<meta name=`"author`" content=`"Era of Siddhas Gurukula`">",
        "<meta property=`"og:title`" content=`"$($meta.title)`">",
        "<meta property=`"og:description`" content=`"$($meta.description)`">",
        "<meta property=`"og:image`" content=`"sacred_city.png`">",
        "<meta property=`"og:type`" content=`"website`">",
        "<meta property=`"og:url`" content=`"https://vibhasperuri-art.github.io/ERA-OF-SIDDHAS/$FileName`">",
        "<meta name=`"twitter:card`" content=`"summary_large_image`">",
        "<meta name=`"twitter:title`" content=`"$($meta.title)`">",
        "<meta name=`"twitter:description`" content=`"$($meta.description)`">"
    )
    $metaBlock = $tags -join "`n"
    # Insert after </title>
    return $Content -replace '(?i)(</title>)', "`$1`n$metaBlock"
}

function Add-SkipLink {
    param($Content)
    return $Content -replace '(?i)(<body[^>]*>)', "`$1`n<a href=`"#main-content`" class=`"skip-link`">Skip to main content</a>"
}

function Add-MainId {
    param($Content)
    # Prefer div with class hub-container
    if ($Content -match '(?i)(<div[^>]*class=`"[^"]*hub-container[^"]*`" )') {
        return $Content -replace '(?i)(<div[^>]*class=`"[^"]*hub-container[^"]*`" )(>)', "`$1 id=`"main-content`"`$2"
    } elseif ($Content -match '(?i)(<main)([^>]*>)') {
        return $Content -replace '(?i)(<main)([^>]*>)', "`$1 id=`"main-content`"`$2"
    }
    return $Content
}

function Add-Breadcrumb {
    param($Content, $Title)
    $breadcrumb = @"
<nav aria-label=`"Breadcrumb`" class=`"breadcrumb`">
  <ol>
    <li><a href=`"index.html`">Home</a></li>
    <li>$Title</li>
  </ol>
</nav>
"@.Trim()
    return $Content -replace '(?i)(</header>)', "`$1`n$breadcrumb"
}

function Add-CitationBlock {
    param($Content)
    $citation = '<details class=`"citation-block`"><summary>📜 Scriptural Sources &amp; References</summary><ol class=`"footnotes`"></ol></details>'
    return $Content -replace '(?i)(<script)', "$citation`n`$1"
}

function Replace-Devanagari {
    param($Content)
    foreach ($pair in $DevanagariToIAST.GetEnumerator()) {
        $dev = [regex]::Escape($pair.Key)
        $iast = "<span lang=`"sa`">$($pair.Value)</span>"
        $Content = $Content -replace $dev, $iast
    }
    return $Content
}

function Lazy-Load-Images {
    param($Content)
    return $Content -replace '(?i)<img([^>]*?)>', {
        param($m)
        $attrs = $m.Groups[1].Value
        if ($attrs -notmatch 'loading=') { $attrs += ' loading=`"lazy`"' }
        if ($attrs -notmatch 'decoding=') { $attrs += ' decoding=`"async`"' }
        if ($attrs -notmatch 'alt=') { $attrs += ' alt=`"Image`"' }
        return "<img$attrs>"
    }
}

function Add-AriaLabels {
    param($Content)
    return $Content -replace '(?i)<(a|button)([^>]*?)>\s*<i[^>]*></i>\s*</\1>', '<$1$2 aria-label=`"icon button`"><i></i></$1>'
}

Get-ChildItem -Path $BaseDir -Filter *.html | ForEach-Object {
    $filePath = $_.FullName
    $fileName = $_.Name
    $content = Get-Content -Path $filePath -Raw -Encoding UTF8
    $content = Insert-MetaTags -Content $content -FileName $fileName
    $content = Add-SkipLink -Content $content
    $content = Add-MainId -Content $content
    $title = if ($PageMeta.ContainsKey($fileName)) { $PageMeta[$fileName].title } else { ($fileName -replace '.html','').Replace('_',' ') }
    $content = Add-Breadcrumb -Content $content -Title $title
    $content = Add-CitationBlock -Content $content
    $content = Replace-Devanagari -Content $content
    $content = Lazy-Load-Images -Content $content
    $content = Add-AriaLabels -Content $content
    Set-Content -Path $filePath -Value $content -Encoding UTF8
    Write-Host "Processed $fileName"
}
