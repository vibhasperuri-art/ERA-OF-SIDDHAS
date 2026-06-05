# PowerShell script to implement PWA support (manifest.json, sw.js, and HTML updates)

$baseDir = "C:/Users/rajpe/.gemini/antigravity/scratch/era_of_siddhas"

# 1. Create manifest.json
$manifestJson = @'
{
  "name": "Era of Siddhas — The Gurukulam",
  "short_name": "Siddhas",
  "description": "Vedic Gurukula platform integrating ancient Indian knowledge systems with modern STEM education.",
  "start_url": "index.html",
  "display": "standalone",
  "background_color": "#0a0000",
  "theme_color": "#b52a2a",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "sacred_city.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
'@
$manifestPath = Join-Path $baseDir "manifest.json"
Set-Content -Path $manifestPath -Value $manifestJson -Encoding UTF8
Write-Host "Created manifest.json at $manifestPath"

# 2. Create sw.js
$serviceWorkerJs = @'
const CACHE_NAME = 'era-of-siddhas-v1';
const ASSETS = [
  './',
  './index.html',
  './pillar_hub.html',
  './course_hub.html',
  './wisdom_hub.html',
  './sangha.html',
  './vicara_sannidhi.html',
  './chanting.html',
  './begin-journey.html',
  './interactive_lesson.html',
  './admin.html',
  './js/api.js',
  './sacred_city.png',
  './flying_manuscript.png',
  './ancient_weapons.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then(networkResponse => {
        if (networkResponse.status === 200 && event.request.method === 'GET') {
          const cacheCopy = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, cacheCopy);
          });
        }
        return networkResponse;
      }).catch(() => {
        if (event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html')) {
          return caches.match('./index.html');
        }
      });
    })
  );
});
'@
$swPath = Join-Path $baseDir "sw.js"
Set-Content -Path $swPath -Value $serviceWorkerJs -Encoding UTF8
Write-Host "Created sw.js at $swPath"

# 3. Update HTML files to link manifest and register service worker
$swRegistrationScript = @'
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('sw.js')
        .then(reg => console.log('Service Worker registered'))
        .catch(err => console.log('Service Worker registration failed', err));
    });
  }
</script>
'@

Get-ChildItem -Path $baseDir -Filter "*.html" -File | ForEach-Object {
    $filePath = $_.FullName
    $html = Get-Content -Path $filePath -Raw
    $html = $html.Replace("`r`n", "`n")

    # Insert manifest link in <head>
    if ($html -notmatch 'link rel="manifest"') {
        $html = $html -replace '</head>', "<link rel=`"manifest`" href=`"manifest.json`">`n</head>"
    }

    # Insert service worker script just before </body>
    if ($html -notmatch 'navigator.serviceWorker.register') {
        $html = $html -replace '</body>', "$swRegistrationScript`n</body>"
    }

    $html = $html.Replace("`n", "`r`n")
    Set-Content -Path $filePath -Value $html -Encoding UTF8
    Write-Host "Linked PWA manifest & registered sw.js in $filePath"
}

Write-Host "PWA implementation complete."
