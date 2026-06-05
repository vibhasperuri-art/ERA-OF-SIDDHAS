import os
import re

BASE_DIR = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas"

# 1. Create manifest.json
manifest_json = """{
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
}"""

with open(os.path.join(BASE_DIR, "manifest.json"), "w", encoding="utf-8", newline="") as f:
    f.write(manifest_json)

# 2. Create sw.js
sw_js = """const CACHE_NAME = 'era-of-siddhas-v1';
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
});"""

with open(os.path.join(BASE_DIR, "sw.js"), "w", encoding="utf-8", newline="") as f:
    f.write(sw_js)


def process_html_file(filepath):
    filename = os.path.basename(filepath)
    print(f"Applying upgrades to {filename}...")
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        html = f.read()

    # 1. SEO Meta Tags
    meta_tags = """  <meta name="description" content="Era of Siddhas – A Vedic Gurukula platform integrating ancient Indian knowledge systems with modern STEM education."/>
  <meta name="keywords" content="Siddha, Vedic education, ancient architecture, Vastu Shastra, Nagara Nirmāṇa, Vimāna Śāstra, Astra Vidyā, Rasa Śāstra, Jyotiṣa, STEM"/>
  <meta property="og:title" content="Era of Siddhas — The Architecture of Siddha Vidyā"/>
  <meta property="og:description" content="Explore the Five Pillars of Siddha Vidyā and their integration with modern scientific inquiry."/>
  <meta property="og:type" content="website"/>
  <meta property="og:url" content="https://vibhasperuri-art.github.io/ERA-OF-SIDDHAS/"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="Era of Siddhas — The Architecture of Siddha Vidyā"/>
  <meta name="twitter:description" content="Explore Vedic sciences and modern STEM in a unified learning platform."/>"""
  
    if 'name="description"' not in html:
        html = html.replace('</head>', f'{meta_tags}\n</head>')

    # 2. Skip to main content link & landmark
    if 'class="skip-link"' not in html:
        skip_link = '<a href="#main-content" class="skip-link" style="position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;">Skip to main content</a>'
        html = re.sub(r'(<body[^>]*>)', r'\1\n' + skip_link, html)
        
    if '<main' in html:
        html = html.replace('<main', '<main id="main-content"')
    elif 'id="main-content"' not in html:
        # Wrap first section
        html = re.sub(r'(<section[^>]*>)', r'<div id="main-content">\n\1', html, count=1)
        html = re.sub(r'(</section>)', r'\1\n</div>', html, count=1)

    # 3. Breadcrumbs
    breadcrumb = f"""<nav aria-label="Breadcrumb" class="breadcrumb-nav">
  <ol style="display:flex;gap:0.5rem;list-style:none;padding:0;margin:0;">
    <li><a href="index.html">Home</a></li>
    <li aria-current="page">{filename}</li>
  </ol>
</nav>"""
    if 'class="breadcrumb-nav"' not in html:
        if '</header>' in html:
            html = html.replace('</header>', f'</header>\n{breadcrumb}')
        else:
            html = re.sub(r'(<body[^>]*>)', r'\1\n' + breadcrumb, html, count=1)

    # 4. WebP Image serving & lazy-loading
    def wrap_img(match):
        attrs_before = match.group(1)
        img_src_base = match.group(2)
        attrs_after = match.group(3)
        
        # Add lazy loading if not present
        attrs = attrs_before + attrs_after
        if 'loading=' not in attrs:
            attrs += ' loading="lazy"'
        if 'decoding=' not in attrs:
            attrs += ' decoding="async"'
        if 'alt=' not in attrs:
            attrs += ' alt="Image"'
            
        return f'<picture><source srcset="{img_src_base}.webp" type="image/webp"><img src="{img_src_base}.png"{attrs}></picture>'

    # Match <img> tags and process them
    # Pattern looks for: <img ... src="base.png" ...>
    pattern_img = r'<img([^>]*?)src="([^"]+?)\.png"([^>]*?)>'
    html = re.sub(pattern_img, wrap_img, html)

    # 5. Collapsible citations
    html = html.replace('[citation]', '<details><summary>Reference</summary><p>Full citation details go here.</p></details>')

    # 6. Accessibility & ARIA tags
    # Theme buttons
    html = html.replace('<button class="theme-btn active" onclick="setTheme(this, \'theme-light\')">Parchment</button>',
                        '<button class="theme-btn active" onclick="setTheme(this, \'theme-light\')" aria-pressed="true" aria-label="Switch theme to Parchment">Parchment</button>')
    html = html.replace('<button class="theme-btn active" onclick="setTheme(this, \'theme-light\')">Parchment &amp; Veda</button>',
                        '<button class="theme-btn active" onclick="setTheme(this, \'theme-light\')" aria-pressed="true" aria-label="Switch theme to Parchment">Parchment</button>')

    html = html.replace('<button class="theme-btn" onclick="setTheme(this, \'theme-fierce\')">Fierce</button>',
                        '<button class="theme-btn" onclick="setTheme(this, \'theme-fierce\')" aria-pressed="false" aria-label="Switch theme to Fierce">Fierce</button>')
    html = html.replace('<button class="theme-btn" onclick="setTheme(this, \'theme-fierce\')">Fierce &amp; Martial</button>',
                        '<button class="theme-btn" onclick="setTheme(this, \'theme-fierce\')" aria-pressed="false" aria-label="Switch theme to Fierce">Fierce</button>')

    html = html.replace('<button class="theme-btn" onclick="setTheme(this, \'theme-earthy\')">Earthy</button>',
                        '<button class="theme-btn" onclick="setTheme(this, \'theme-earthy\')" aria-pressed="false" aria-label="Switch theme to Earthy">Earthy</button>')
    html = html.replace('<button class="theme-btn" onclick="setTheme(this, \'theme-earthy\')">Earthy &amp; Ancient</button>',
                        '<button class="theme-btn" onclick="setTheme(this, \'theme-earthy\')" aria-pressed="false" aria-label="Switch theme to Earthy">Earthy</button>')

    html = html.replace('<button class="theme-btn" onclick="setTheme(this, \'theme-mystical\')">Mystical</button>',
                        '<button class="theme-btn" onclick="setTheme(this, \'theme-mystical\')" aria-pressed="false" aria-label="Switch theme to Mystical">Mystical</button>')
    html = html.replace('<button class="theme-btn" onclick="setTheme(this, \'theme-mystical\')">Mystical &amp; Ethereal</button>',
                        '<button class="theme-btn" onclick="setTheme(this, \'theme-mystical\')" aria-pressed="false" aria-label="Switch theme to Mystical">Mystical</button>')

    # Update setTheme JS
    old_set_theme_1 = """  document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
  if (btnElement) {
    btnElement.classList.add('active');
  } else {
    document.querySelectorAll('.theme-btn').forEach(btn => {
      if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(themeName)) {
        btn.classList.add('active');
      }
    });
  }"""
  
    new_set_theme_1 = """  document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.classList.remove('active');
    btn.setAttribute('aria-pressed', 'false');
  });
  if (btnElement) {
    btnElement.classList.add('active');
    btnElement.setAttribute('aria-pressed', 'true');
  } else {
    document.querySelectorAll('.theme-btn').forEach(btn => {
      if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(themeName)) {
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
      }
    });
  }"""
  
    old_set_theme_2 = """    document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
    if (btnElement) {
      btnElement.classList.add('active');
    } else {
      document.querySelectorAll('.theme-btn').forEach(btn => {
        if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(themeName)) {
          btn.classList.add('active');
        }
      });
    }"""
    
    new_set_theme_2 = """    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.classList.remove('active');
      btn.setAttribute('aria-pressed', 'false');
    });
    if (btnElement) {
      btnElement.classList.add('active');
      btnElement.setAttribute('aria-pressed', 'true');
    } else {
      document.querySelectorAll('.theme-btn').forEach(btn => {
        if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(themeName)) {
          btn.classList.add('active');
          btn.setAttribute('aria-pressed', 'true');
        }
      });
    }"""

    html = html.replace(old_set_theme_1, new_set_theme_1)
    html = html.replace(old_set_theme_2, new_set_theme_2)

    # Add aria-current="page"
    html = html.replace('class="nav-btn active"', 'class="nav-btn active" aria-current="page"')

    # Hide decorative SVGs
    html = re.sub(r'<svg(?!([^>]*?aria-hidden=))([^>]*?)>', r'<svg aria-hidden="true"\1\2>', html)

    # Skip-link focus styling
    skip_link_styles = """
  /* Accessible Skip-Link styling */
  .skip-link:focus {
    position: fixed !important;
    top: 10px;
    left: 10px;
    z-index: 10000;
    background: var(--bg-1, #1a0505);
    color: var(--gold-bright, #ff4d4d);
    padding: 10px 20px;
    border: 2px solid var(--gold, #b52a2a);
    outline: none;
    width: auto !important;
    height: auto !important;
    overflow: visible !important;
    clip: auto !important;
  }
</style>"""
    if "Accessible Skip-Link styling" not in html:
        html = html.replace("</style>", skip_link_styles)

    # 7. begin-journey.html specialized updates
    if filename == "begin-journey.html":
        html = html.replace('<div class="step-dots" id="stepDots">', 
                            '<div class="step-dots" id="stepDots" role="progressbar" aria-valuenow="1" aria-valuemin="1" aria-valuemax="5" aria-valuetext="Step 1 of 5: Awakening">')
        
        old_goto = """  function goTo(n) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById('screen' + n).classList.add('active');
    document.querySelectorAll('.step-dot').forEach((d, i) => {
      d.classList.remove('active', 'done');
      if (i < n) d.classList.add('done');
      if (i === n) d.classList.add('active');
    });
    document.getElementById('stepLabel').textContent = stepLabels[n];
    window.scrollTo(0, 0);
  }"""
  
        new_goto = """  function goTo(n) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById('screen' + n).classList.add('active');
    document.querySelectorAll('.step-dot').forEach((d, i) => {
      d.classList.remove('active', 'done');
      if (i < n) d.classList.add('done');
      if (i === n) d.classList.add('active');
    });
    document.getElementById('stepLabel').textContent = stepLabels[n];
    const dotsEl = document.getElementById('stepDots');
    if (dotsEl) {
      dotsEl.setAttribute('aria-valuenow', n + 1);
      dotsEl.setAttribute('aria-valuetext', 'Step ' + (n + 1) + ' of 5: ' + stepLabels[n]);
    }
    window.scrollTo(0, 0);
  }"""
        html = html.replace(old_goto, new_goto)

    # 8. course_hub.html specialized updates
    if filename == "course_hub.html":
        html = html.replace('<div class="tabs-container" id="tabs-section">',
                            '<div class="tabs-container" id="tabs-section" role="tablist" aria-label="Course Sections">')
        html = html.replace('<div class="content-grid" id="course-grid">',
                            '<div class="content-grid" id="course-grid" role="tabpanel" aria-label="Course Items">')

        old_tabs_render = """  tabsSection.innerHTML = `
    <button class="tab active" onclick="switchTab(this, 'learn')">Learn (Sub-topics)</button>
    <button class="tab" onclick="switchTab(this, 'stories')">Stories</button>
    <button class="tab" onclick="switchTab(this, 'games')">Games & Quiz</button>
    <button class="tab" onclick="switchTab(this, 'simulations')">Simulations</button>
    <button class="tab" onclick="switchTab(this, 'nano')">Nano Courses</button>
  `;"""

        new_tabs_render = """  tabsSection.innerHTML = `
    <button class="tab active" role="tab" aria-selected="true" aria-controls="course-grid" onclick="switchTab(this, 'learn')">Learn (Sub-topics)</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="course-grid" onclick="switchTab(this, 'stories')">Stories</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="course-grid" onclick="switchTab(this, 'games')">Games & Quiz</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="course-grid" onclick="switchTab(this, 'simulations')">Simulations</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="course-grid" onclick="switchTab(this, 'nano')">Nano Courses</button>
  `;"""
        html = html.replace(old_tabs_render, new_tabs_render)

        old_switch_tab = """function switchTab(btn, tabKey) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  renderTabContent(tabKey);
}"""
        new_switch_tab = """function switchTab(btn, tabKey) {
  document.querySelectorAll('.tab').forEach(t => {
    t.classList.remove('active');
    t.setAttribute('aria-selected', 'false');
  });
  btn.classList.add('active');
  btn.setAttribute('aria-selected', 'true');
  renderTabContent(tabKey);
}"""
        html = html.replace(old_switch_tab, new_switch_tab)

    # 9. PWA registration & manifest link
    if 'link rel="manifest"' not in html:
        html = html.replace('</head>', '<link rel="manifest" href="manifest.json">\n</head>')
        
    sw_reg = """<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('sw.js')
        .then(reg => console.log('Service Worker registered'))
        .catch(err => console.log('Service Worker registration failed', err));
    });
  }
</script>"""
    if 'navigator.serviceWorker.register' not in html:
        html = html.replace('</body>', f'{sw_reg}\n</body>')

    # 10. Defer api.js
    html = html.replace('<script src="js/api.js"></script>', '<script src="js/api.js" defer></script>')

    # Save cleanly as UTF-8 (no BOM)
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(html)
    print(f"  [UPGRADED] {filename}")


def main():
    for file in os.listdir(BASE_DIR):
        if file.endswith(".html"):
            process_html_file(os.path.join(BASE_DIR, file))

if __name__ == "__main__":
    main()
