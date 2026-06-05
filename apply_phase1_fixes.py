import os, re

# Directory containing HTML files
BASE_DIR = r"C:/Users/rajpe/.gemini/antigravity/scratch/era_of_siddhas"

# SEO meta templates per file (simple generic values, can be customized)
PAGE_META = {
    "index.html": {
        "description": "Era of Siddhas — A Vedic Gurukula platform integrating ancient Indian knowledge systems with modern STEM education.",
        "keywords": "Siddha, Vedic education, ancient architecture, Vastu Shastra, Nagara Nirmāṇa, Vimāna Śāstra, Astra Vidyā, Rasa Śāstra, Jyotiṣa, STEM",
        "title": "Era of Siddhas — The Architecture of Siddha Vidyā",
    },
    "pillar_hub.html": {
        "description": "Explore the Three Pillars of Siddha Vidyā: Nagara Nirmāṇa, Rājya Palanam, Yuddham — bridging Vedic sciences with modern research.",
        "keywords": "Siddha, Vedic education, Nagara Nirmāṇa, Rājya Palanam, Yuddham, Vastu, Yoga, Upasana, Upanishads, STEM",
        "title": "Era of Siddhas — The Three Pillars",
    },
    "course_hub.html": {
        "description": "Structured Gurukula courses across five Vedic science pillars with graded progression from Mumukṣu to Siddha levels.",
        "keywords": "Siddha, courses, Vedic education, pillars, curriculum, STEM",
        "title": "Era of Siddhas — Courses",
    },
    "wisdom_hub.html": {
        "description": "Wisdom Publications Hub — magazines, research articles, Itihāsa & Purāṇa stories, and modern scientific validations of ancient Indian sciences.",
        "keywords": "Siddha, wisdom, publications, articles, research, Vedic science",
        "title": "Era of Siddhas — Wisdom Hub",
    },
    "interactive_lesson.html": {
        "description": "Interactive Vedic science lessons with scriptural sources, STEM correlations, and guided Socratic reflection exercises.",
        "keywords": "Siddha, lessons, interactive, Vedic science, education",
        "title": "Era of Siddhas — Interactive Lesson",
    },
    "chanting.html": {
        "description": "Sacred mantra chanting practice with audio guidance, transliteration, and meaning for daily sādhana.",
        "keywords": "Siddha, chanting, mantra, audio, practice",
        "title": "Era of Siddhas — Chanting",
    },
    "sangha.html": {
        "description": "The Saṅgha — Community feed for shared reflections, insights, and collective wisdom from seekers on the path.",
        "keywords": "Siddha, sangha, community, reflections",
        "title": "Era of Siddha — The Saṅgha",
    },
    "vicara_sannidhi.html": {
        "description": "Vicāra Sannidhi — The Inner Sanctum of Inquiry. Engage in Socratic dialogue with the Guru AI to deepen your understanding of each pillar.",
        "keywords": "Siddha, AI, dialogue, inquiry, guru AI",
        "title": "Era of Siddha — Vicāra Sannidhi",
    },
    "admin.html": {
        "description": "Gurukula Administration — Manage seekers, publish content, broadcast announcements, and monitor the Saṅgha.",
        "keywords": "Siddha, admin, management, dashboard",
        "title": "Era of Siddha — Admin",
    },
}

# Mapping of Devanagari to IAST for consistency (Phase 1 only IAST displayed)
DEVANAGARI_TO_IAST = {
    "नगर निर्माण": "Nagara Nirmāṇa",
    "राज्य पालनम्": "Rājya Palanam",
    "युद्धम्": "Yuddham",
    "शास्त्र": "Śāstra",
    "विमान शास्त्र": "Vimāna Śāstra",
    "रसायन शास्त्र": "Rasāśāstra",
    # add more as needed
}

def insert_meta_tags(content, filename):
    meta = PAGE_META.get(filename)
    if not meta:
        return content
    tags = []
    tags.append(f'<meta name="description" content="{meta["description"]}">')
    tags.append(f'<meta name="keywords" content="{meta["keywords"]}">')
    tags.append(f'<meta name="author" content="Era of Siddhas Gurukula">')
    tags.append(f'<meta property="og:title" content="{meta["title"]}">')
    tags.append(f'<meta property="og:description" content="{meta["description"]}">')
    tags.append(f'<meta property="og:image" content="sacred_city.png">')
    tags.append(f'<meta property="og:type" content="website">')
    tags.append(f'<meta property="og:url" content="https://vibhasperuri-art.github.io/ERA-OF-SIDDHAS/{filename}">')
    tags.append(f'<meta name="twitter:card" content="summary_large_image">')
    tags.append(f'<meta name="twitter:title" content="{meta["title"]}">')
    tags.append(f'<meta name="twitter:description" content="{meta["description"]}">')
    meta_block = "\n".join(tags)
    # Insert after </title>
    return re.sub(r"(</title>)", r"\1\n" + meta_block, content, count=1, flags=re.IGNORECASE)

def add_skip_link(content):
    return re.sub(r"(<body[^>]*>)", r"\1\n<a href=\"#main-content\" class=\"skip-link\">Skip to main content</a>", content, count=1, flags=re.IGNORECASE)

def add_main_id(content):
    # Add id to the first <div class="hub-container" or <main> if present
    content, count = re.subn(r"(<div[^>]*class=\"[^\"]*hub-container[^\"]*\")(>)", r"\1 id=\"main-content\"\2", content, count=1, flags=re.IGNORECASE)
    if count == 0:
        content, _ = re.subn(r"(<main)([^>]*>)", r"\1 id=\"main-content\"\2", content, count=1, flags=re.IGNORECASE)
    return content

def add_breadcrumb(content, filename, page_title):
    breadcrumb = f'''<nav aria-label="Breadcrumb" class="breadcrumb">
  <ol>
    <li><a href="index.html">Home</a></li>
    <li>{page_title}</li>
  </ol>
</nav>'''
    return re.sub(r"(</header>)", r"\1\n" + breadcrumb, content, count=1, flags=re.IGNORECASE)

def add_citation_block(content):
    citation = '''<details class="citation-block"><summary>📜 Scriptural Sources & References</summary><ol class="footnotes"></ol></details>'''
    return re.sub(r"(<script)", citation + "\n\1", content, count=1, flags=re.IGNORECASE)

def replace_devanagari(content):
    for dev, iast in DEVANAGARI_TO_IAST.items():
        content = content.replace(dev, f'<span lang="sa">{iast}</span>')
    return content

def lazy_load_images(content):
    def repl(match):
        tag = match.group(0)
        if 'loading=' not in tag:
            tag = tag.rstrip('>') + ' loading="lazy" decoding="async"'>
        if 'alt=' not in tag:
            tag = tag.rstrip('>') + ' alt="Image"'>
        return tag
    return re.sub(r"<img\b[^>]*>", repl, content, flags=re.IGNORECASE)

def add_aria_labels(content):
    # Simple heuristic for icon-only links/buttons
    return re.sub(r"<(a|button)([^>]*?)>\s*<i[^>]*></i>\s*</\1>", r"<\1\2 aria-label=\"icon button\"><i></i></\1>", content, flags=re.IGNORECASE)

def process_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = insert_meta_tags(content, filename)
    content = add_skip_link(content)
    content = add_main_id(content)
    page_title = PAGE_META.get(filename, {}).get("title", filename.replace('.html','').replace('_',' ').title())
    content = add_breadcrumb(content, filename, page_title)
    content = add_citation_block(content)
    content = replace_devanagari(content)
    content = lazy_load_images(content)
    content = add_aria_labels(content)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Processed {filename}")

if __name__ == "__main__":
    for entry in os.listdir(BASE_DIR):
        if entry.lower().endswith('.html'):
            process_file(os.path.join(BASE_DIR, entry))
