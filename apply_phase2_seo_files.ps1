# PowerShell script to generate sitemap.xml and robots.txt for the Era of Siddhas project

$baseDir = "C:/Users/rajpe/.gemini/antigravity/scratch/era_of_siddhas"
$siteUrl = "https://vibhasperuri-art.github.io/ERA-OF-SIDDHAS"
$today = (Get-Date).ToString("yyyy-MM-dd")

# 1. Generate sitemap.xml content
$sitemapXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>$siteUrl/index.html</loc>
    <lastmod>$today</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>$siteUrl/pillar_hub.html</loc>
    <lastmod>$today</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>$siteUrl/course_hub.html</loc>
    <lastmod>$today</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>$siteUrl/wisdom_hub.html</loc>
    <lastmod>$today</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>$siteUrl/sangha.html</loc>
    <lastmod>$today</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>$siteUrl/vicara_sannidhi.html</loc>
    <lastmod>$today</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>$siteUrl/chanting.html</loc>
    <lastmod>$today</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>$siteUrl/begin-journey.html</loc>
    <lastmod>$today</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>$siteUrl/interactive_lesson.html</loc>
    <lastmod>$today</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>
"@

# Write sitemap.xml
$sitemapPath = Join-Path $baseDir "sitemap.xml"
Set-Content -Path $sitemapPath -Value $sitemapXml -Encoding UTF8
Write-Host "Created sitemap.xml at $sitemapPath"

# 2. Generate robots.txt content
$robotsTxt = @"
# robots.txt for Era of Siddhas

User-agent: *
Disallow: /admin.html
Disallow: /js/api.js

# Allow all other content
Allow: /

Sitemap: $siteUrl/sitemap.xml
"@

# Write robots.txt
$robotsPath = Join-Path $baseDir "robots.txt"
Set-Content -Path $robotsPath -Value $robotsTxt -Encoding UTF8
Write-Host "Created robots.txt at $robotsPath"

Write-Host "SEO configuration files generated successfully."
