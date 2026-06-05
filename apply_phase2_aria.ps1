# PowerShell script to apply Phase 2 ARIA and Accessibility improvements to all HTML files

$baseDir = "C:/Users/rajpe/.gemini/antigravity/scratch/era_of_siddhas"

# Process each HTML file
Get-ChildItem -Path $baseDir -Filter "*.html" -File | ForEach-Object {
    $filePath = $_.FullName
    $html = Get-Content -Path $filePath -Raw
    # Normalize line endings to LF only for consistent string matching
    $html = $html.Replace("`r`n", "`n")

    # 1. Update theme buttons HTML markup to include initial aria-pressed and aria-label
    $html = $html.Replace('<button class="theme-btn active" onclick="setTheme(this, ''theme-light'')">Parchment</button>',
                          '<button class="theme-btn active" onclick="setTheme(this, ''theme-light'')" aria-pressed="true" aria-label="Switch theme to Parchment">Parchment</button>')
    
    $html = $html.Replace('<button class="theme-btn" onclick="setTheme(this, ''theme-fierce'')">Fierce</button>',
                          '<button class="theme-btn" onclick="setTheme(this, ''theme-fierce'')" aria-pressed="false" aria-label="Switch theme to Fierce">Fierce</button>')
    $html = $html.Replace('<button class="theme-btn" onclick="setTheme(this, ''theme-fierce'')">Fierce & Martial</button>',
                          '<button class="theme-btn" onclick="setTheme(this, ''theme-fierce'')" aria-pressed="false" aria-label="Switch theme to Fierce">Fierce</button>')

    $html = $html.Replace('<button class="theme-btn" onclick="setTheme(this, ''theme-earthy'')">Earthy</button>',
                          '<button class="theme-btn" onclick="setTheme(this, ''theme-earthy'')" aria-pressed="false" aria-label="Switch theme to Earthy">Earthy</button>')
    $html = $html.Replace('<button class="theme-btn" onclick="setTheme(this, ''theme-earthy'')">Earthy & Ancient</button>',
                          '<button class="theme-btn" onclick="setTheme(this, ''theme-earthy'')" aria-pressed="false" aria-label="Switch theme to Earthy">Earthy</button>')

    $html = $html.Replace('<button class="theme-btn" onclick="setTheme(this, ''theme-mystical'')">Mystical</button>',
                          '<button class="theme-btn" onclick="setTheme(this, ''theme-mystical'')" aria-pressed="false" aria-label="Switch theme to Mystical">Mystical</button>')
    $html = $html.Replace('<button class="theme-btn" onclick="setTheme(this, ''theme-mystical'')">Mystical & Ethereal</button>',
                          '<button class="theme-btn" onclick="setTheme(this, ''theme-mystical'')" aria-pressed="false" aria-label="Switch theme to Mystical">Mystical</button>')

    # 2. Update setTheme JS function to toggle aria-pressed
    $oldSetThemeJs = @'
  document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
  if (btnElement) {
    btnElement.classList.add('active');
  } else {
    document.querySelectorAll('.theme-btn').forEach(btn => {
      if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(themeName)) {
        btn.classList.add('active');
      }
    });
  }
'@
    
    $newSetThemeJs = @'
  document.querySelectorAll('.theme-btn').forEach(btn => {
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
  }
'@
    
    $html = $html.Replace($oldSetThemeJs.Replace("`r`n", "`n"), $newSetThemeJs.Replace("`r`n", "`n"))

    $oldSetThemeJsAlt = @'
    document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
    if (btnElement) {
      btnElement.classList.add('active');
    } else {
      document.querySelectorAll('.theme-btn').forEach(btn => {
        if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(themeName)) {
          btn.classList.add('active');
        }
      });
    }
'@
    
    $newSetThemeJsAlt = @'
    document.querySelectorAll('.theme-btn').forEach(btn => {
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
    }
'@
    
    $html = $html.Replace($oldSetThemeJsAlt.Replace("`r`n", "`n"), $newSetThemeJsAlt.Replace("`r`n", "`n"))

    # 3. Add aria-current="page" to active navigation links
    $html = $html.Replace('class="nav-btn active"', 'class="nav-btn active" aria-current="page"')

    # 4. Hide decorative SVGs from screen readers by default
    # Matches <svg ...> that doesn't already have aria-hidden
    $html = $html -replace '<svg(?!([^>]*?aria-hidden=))([^>]*?)>', '<svg aria-hidden="true"$1$2>'

    # 5. Append skip-link focus styles to the stylesheet/style block
    $skipLinkFocusStyles = @'

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
</style>
'@
    if ($html -notmatch "Accessible Skip-Link styling") {
        $html = $html.Replace("</style>", $skipLinkFocusStyles.Replace("`r`n", "`n"))
    }

    # 6. Specialized updates for begin-journey.html
    if ($filePath -match "begin-journey.html") {
        $html = $html.Replace('<div class="step-dots" id="stepDots">', 
                              '<div class="step-dots" id="stepDots" role="progressbar" aria-valuenow="1" aria-valuemin="1" aria-valuemax="5" aria-valuetext="Step 1 of 5: Awakening">')
        
        $oldGoTo = @'
  function goTo(n) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById('screen' + n).classList.add('active');
    document.querySelectorAll('.step-dot').forEach((d, i) => {
      d.classList.remove('active', 'done');
      if (i < n) d.classList.add('done');
      if (i === n) d.classList.add('active');
    });
    document.getElementById('stepLabel').textContent = stepLabels[n];
    window.scrollTo(0, 0);
  }
'@
        
        $newGoTo = @'
  function goTo(n) {
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
  }
'@
        
        $html = $html.Replace($oldGoTo.Replace("`r`n", "`n"), $newGoTo.Replace("`r`n", "`n"))
    }

    # 7. Specialized updates for course_hub.html
    if ($filePath -match "course_hub.html") {
        $html = $html.Replace('<div class="tabs-container" id="tabs-section">',
                              '<div class="tabs-container" id="tabs-section" role="tablist" aria-label="Course Sections">')
        
        $html = $html.Replace('<div class="content-grid" id="course-grid">',
                              '<div class="content-grid" id="course-grid" role="tabpanel" aria-label="Course Items">')

        $oldTabsRenderLiteral = @'
  tabsSection.innerHTML = `
    <button class="tab active" onclick="switchTab(this, 'learn')">Learn (Sub-topics)</button>
    <button class="tab" onclick="switchTab(this, 'stories')">Stories</button>
    <button class="tab" onclick="switchTab(this, 'games')">Games & Quiz</button>
    <button class="tab" onclick="switchTab(this, 'simulations')">Simulations</button>
    <button class="tab" onclick="switchTab(this, 'nano')">Nano Courses</button>
  `;
'@

        $newTabsRenderLiteral = @'
  tabsSection.innerHTML = `
    <button class="tab active" role="tab" aria-selected="true" aria-controls="course-grid" onclick="switchTab(this, 'learn')">Learn (Sub-topics)</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="course-grid" onclick="switchTab(this, 'stories')">Stories</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="course-grid" onclick="switchTab(this, 'games')">Games & Quiz</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="course-grid" onclick="switchTab(this, 'simulations')">Simulations</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="course-grid" onclick="switchTab(this, 'nano')">Nano Courses</button>
  `;
'@
        
        $html = $html.Replace($oldTabsRenderLiteral.Replace("`r`n", "`n"), $newTabsRenderLiteral.Replace("`r`n", "`n"))

        $oldSwitchTab = @'
function switchTab(btn, tabKey) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  renderTabContent(tabKey);
}
'@
        $newSwitchTab = @'
function switchTab(btn, tabKey) {
  document.querySelectorAll('.tab').forEach(t => {
    t.classList.remove('active');
    t.setAttribute('aria-selected', 'false');
  });
  btn.classList.add('active');
  btn.setAttribute('aria-selected', 'true');
  renderTabContent(tabKey);
}
'@
        $html = $html.Replace($oldSwitchTab.Replace("`r`n", "`n"), $newSwitchTab.Replace("`r`n", "`n"))
    }

    # Restore CRLF (Windows standard)
    $html = $html.Replace("`n", "`r`n")

    # Write back the modified HTML file
    Set-Content -Path $filePath -Value $html -Encoding UTF8
    Write-Host "Accessibility & ARIA tags applied to $filePath"
}

Write-Host "Phase 2 ARIA updates complete."
