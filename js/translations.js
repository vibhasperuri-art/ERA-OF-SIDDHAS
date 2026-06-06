// js/translations.js - Multi-language translation engine for Era of Siddhas (Offline capable)

const TRANSLATIONS = {
  en: {
    "Home": "Home",
    "Pillars": "Pillars",
    "Course Hub": "Course Hub",
    "Wisdom Hub": "Wisdom Hub",
    "Mantra Chanting": "Chanting",
    "Sannidhi (AI)": "Sannidhi (AI)",
    "Saṅgha": "Saṅgha",
    "Glossary": "Glossary",
    "About": "About",
    "Admin": "Admin",
    "👤 Profile": "👤 Profile",
    "Reset Journey": "Reset Journey",
    "Acknowledge": "Acknowledge",
    "Acknowledge Wisdom": "Acknowledge Wisdom",
    "Vastu Maṇḍala Room Planner": "Vastu Maṇḍala Room Planner",
    "Ayadi Resonant Calculator": "Ayadi Resonant Calculator",
    "Aya (Income)": "Aya (Income)",
    "Vyaya (Expense)": "Vyaya (Expense)",
    "Yoni (Energy)": "Yoni (Energy)",
    "Harmony Rating": "Harmony Rating",
    "Width (Hasta)": "Width (Hasta)",
    "Length (Hasta)": "Length (Hasta)",
    "Resonant": "Resonant",
    "Conflict": "Conflict",
    "Neutral": "Neutral",
    "Mumukṣu": "Mumukṣu",
    "Śiṣya": "Śiṣya",
    "Sādhaka": "Sādhaka",
    "Siddha": "Siddha",
    "The Inner Sanctum of Inquiry": "The Inner Sanctum of Inquiry",
    "About the Guru AI": "About the Guru AI",
    "Vedic Wisdom Publications": "Vedic Wisdom Publications",
    "Harmony Index:": "Harmony Index:",
    "Select a room chip above, then click a grid cell to place it. Match elements for maximum thermodynamic harmony!": "Select a room chip above, then click a grid cell to place it. Match elements for maximum thermodynamic harmony!"
  },
  sa: {
    "Home": "गृहम् (Gṛham)",
    "Pillars": "स्तम्भाः (Stambhāḥ)",
    "Course Hub": "विद्यापीठम् (Vidyāpīṭham)",
    "Wisdom Hub": "ज्ञानमन्दिरम् (Jñānamandiram)",
    "Mantra Chanting": "सङ्कीर्तनम् (Saṅkīrtanam)",
    "Sannidhi (AI)": "गुरुसन्निधिः (Gurusannidhiḥ)",
    "Saṅgha": "सङ्घः (Saṅghaḥ)",
    "Glossary": "शब्दकोशः (Śabdakośaḥ)",
    "About": "विषये (Viṣaye)",
    "Admin": "प्रबन्धनम् (Prabandhanam)",
    "👤 Profile": "👤 परिचयपत्रम्",
    "Reset Journey": "यात्रा पुनःप्रारम्भः",
    "Acknowledge": "स्वीकृतम्",
    "Acknowledge Wisdom": "ज्ञानस्वीकारः",
    "Vastu Maṇḍala Room Planner": "वास्तुमण्डल-नियोजकः",
    "Ayadi Resonant Calculator": "आयादि-सङ्गणकः",
    "Aya (Income)": "आयः (Ayaḥ)",
    "Vyaya (Expense)": "व्ययः (Vyayaḥ)",
    "Yoni (Energy)": "योनिः (Yoniḥ)",
    "Harmony Rating": "तादात्म्य-मूल्याङ्कनम्",
    "Width (Hasta)": "विस्तारः (हस्तः)",
    "Length (Hasta)": "दैर्घ्यम् (हस्तः)",
    "Resonant": "अनुरणितम्",
    "Conflict": "विरोधः",
    "Neutral": "तटस्थम्",
    "Mumukṣu": "मुमुक्षुः (Mumukṣuḥ)",
    "Śiṣya": "शिष्यः (Śiṣyaḥ)",
    "Sādhaka": "साधकः (Sādhakaḥ)",
    "Siddha": "सिद्धः (Siddhaḥ)",
    "The Inner Sanctum of Inquiry": "जिज्ञासा-सभामन्दिरम्",
    "About the Guru AI": "गुरु-कृत्रिमबुद्धि-विषये",
    "Vedic Wisdom Publications": "वैदिकज्ञान-प्रकाशनानि",
    "Harmony Index:": "तादात्म्यसूचकः:",
    "Select a room chip above, then click a grid cell to place it. Match elements for maximum thermodynamic harmony!": "उपरि प्रकोष्ठचिपं चित्वा स्थापनाय ग्रिडकोष्ठं नुदन्तु। गभीर-तापगतिक-तादात्म्याय तत्त्वानि मेलयन्तु!"
  },
  hi: {
    "Home": "मुख्य पृष्ठ",
    "Pillars": "विद्या स्तम्भ",
    "Course Hub": "पाठ्यक्रम",
    "Wisdom Hub": "ज्ञानकोश",
    "Mantra Chanting": "मंत्र साधना",
    "Sannidhi (AI)": "गुरु सन्निधि",
    "Saṅgha": "संघ",
    "Glossary": "शब्दावली",
    "About": "परिचय",
    "Admin": "प्रशासन",
    "👤 Profile": "👤 प्रोफाइल",
    "Reset Journey": "यात्रा रीसेट करें",
    "Acknowledge": "स्वीकार करें",
    "Acknowledge Wisdom": "ज्ञान स्वीकार करें",
    "Vastu Maṇḍala Room Planner": "वास्तु मंडल कक्ष नियोजक",
    "Ayadi Resonant Calculator": "आयादि गणित गणक",
    "Aya (Income)": "आय (Aya)",
    "Vyaya (Expense)": "व्यय (Vyaya)",
    "Yoni (Energy)": "योनि (Yoni)",
    "Harmony Rating": "सामंजस्य रेटिंग",
    "Width (Hasta)": "चौड़ाई (हस्त)",
    "Length (Hasta)": "लंबाई (हस्त)",
    "Resonant": "सामंजस्यपूर्ण",
    "Conflict": "विरोध",
    "Neutral": "तटस्थ",
    "Mumukṣu": "मुमुक्षु",
    "Śiṣya": "शिष्य",
    "Sādhaka": "साधक",
    "Siddha": "सिद्ध",
    "The Inner Sanctum of Inquiry": "जिज्ञासा का गर्भगृह",
    "About the Guru AI": "गुरु एआई के बारे में",
    "Vedic Wisdom Publications": "वैदिक ज्ञान प्रकाशन",
    "Harmony Index:": "सामंजस्य सूचकांक:",
    "Select a room chip above, then click a grid cell to place it. Match elements for maximum thermodynamic harmony!": "ऊपर से एक कमरा चुनें, फिर उसे ग्रिड सेल में रखने के लिए क्लिक करें। अधिकतम थर्मोडायनामिक सामंजस्य के लिए तत्वों का मिलान करें!"
  },
  ta: {
    "Home": "முகப்பு",
    "Pillars": "தூண்கள்",
    "Course Hub": "பாடநெறி",
    "Wisdom Hub": "ஞான மையம்",
    "Mantra Chanting": "உச்சாடனம்",
    "Sannidhi (AI)": "சந்நிதி (AI)",
    "Saṅgha": "சங்கம்",
    "Glossary": "கலைச்சொற்கள்",
    "About": "எங்களைப் பற்றி",
    "Admin": "நிர்வாகம்",
    "👤 Profile": "👤 சுயவிவரம்",
    "Reset Journey": "பயணத்தை மீட்டமை",
    "Acknowledge": "ஏற்றுக்கொள்",
    "Acknowledge Wisdom": "ஞானம் ஏற்றுக்கொள்",
    "Vastu Maṇḍala Room Planner": "வாஸ்து மண்டல அறை அமைப்பாளர்",
    "Ayadi Resonant Calculator": "ஆயாதி கணிப்பான்",
    "Aya (Income)": "ஆதாயம் (ஆயம்)",
    "Vyaya (Expense)": "விரயம் (வியயம்)",
    "Yoni (Energy)": "யோனி (யோனி)",
    "Harmony Rating": "இணக்க மதிப்பீடு",
    "Width (Hasta)": "அகலம் (முழம்/ஹஸ்தம்)",
    "Length (Hasta)": "நீளம் (முழம்/ஹஸ்தம்)",
    "Resonant": "இணக்கமானது",
    "Conflict": "முரண்பாடு",
    "Neutral": "நடுநிலை",
    "Mumukṣu": "முமுக்ஷு",
    "Śiṣya": "சிஷ்யன்",
    "Sādhaka": "சாதகன்",
    "Siddha": "சித்தர்",
    "The Inner Sanctum of Inquiry": "கேள்வி ஞான சந்நிதி",
    "About the Guru AI": "குரு AI பற்றி",
    "Vedic Wisdom Publications": "வேத ஞான வெளியீடுகள்",
    "Harmony Index:": "இணக்கக் குறியீடு:",
    "Select a room chip above, then click a grid cell to place it. Match elements for maximum thermodynamic harmony!": "மேலே உள்ள அறை சிப்பைத் தேர்ந்தெடுத்து, அதை வைக்க கட்டத்தில் கிளிக் செய்யவும். வெப்பவியக்கவியல் இணக்கத்திற்கு பஞ்சபூதங்களை பொருத்தவும்!"
  }
};

window.changeLanguage = function(lang) {
  if (!TRANSLATIONS[lang]) return;
  localStorage.setItem('eos_lang', lang);
  applyTranslations(lang);
  
  // Custom event trigger for pages to perform extra translations (e.g. canvas elements, charts)
  window.dispatchEvent(new CustomEvent("eos-language-changed", { detail: { language: lang } }));
};

function applyTranslations(lang) {
  document.documentElement.lang = lang;
  translateNode(document.body, lang);
  
  const selector = document.getElementById('eos-lang-select');
  if (selector) {
    selector.value = lang;
  }
}

function translateNode(node, lang) {
  if (node.nodeType === Node.ELEMENT_NODE) {
    if (['SCRIPT', 'STYLE', 'CANVAS', 'TEXTAREA', 'INPUT', 'NOSCRIPT'].includes(node.tagName)) {
      return;
    }
    if (node.id === 'eos-lang-select') {
      return;
    }
    
    // If it's a leaf node with text and no element children
    if (node.children.length === 0) {
      const text = node.innerText.trim();
      if (text) {
        if (!node.dataset.i18nOrig) {
          node.dataset.i18nOrig = text;
        }
        const origKey = node.dataset.i18nOrig;
        if (TRANSLATIONS[lang] && TRANSLATIONS[lang][origKey] !== undefined) {
          node.innerText = TRANSLATIONS[lang][origKey];
        } else if (TRANSLATIONS['en'][origKey] !== undefined) {
          node.innerText = TRANSLATIONS['en'][origKey];
        }
      }
      return;
    }
    
    // Recurse
    for (let i = 0; i < node.children.length; i++) {
      translateNode(node.children[i], lang);
    }
  }
}

function injectLanguageSelector() {
  const navActions = document.querySelector('.nav-actions') || document.querySelector('.glass-nav') || document.querySelector('header');
  if (navActions && !document.getElementById('eos-lang-select')) {
    const selector = document.createElement('select');
    selector.id = 'eos-lang-select';
    selector.className = 'lang-selector';
    selector.setAttribute('aria-label', 'Select Language');
    selector.innerHTML = `
      <option value="en">🌐 EN</option>
      <option value="sa">🌐 SA</option>
      <option value="hi">🌐 HI</option>
      <option value="ta">🌐 TA</option>
    `;
    
    // Match glassmorphism styling
    selector.style.background = 'rgba(255, 255, 255, 0.07)';
    selector.style.color = 'var(--text-primary, #ffffff)';
    selector.style.border = '1px solid var(--border-glass, rgba(255, 255, 255, 0.15))';
    selector.style.borderRadius = '20px';
    selector.style.padding = '4px 10px';
    selector.style.fontFamily = "'Outfit', sans-serif";
    selector.style.fontSize = '0.85rem';
    selector.style.fontWeight = '500';
    selector.style.cursor = 'pointer';
    selector.style.marginRight = '12px';
    selector.style.outline = 'none';
    selector.style.backdropFilter = 'blur(10px)';
    selector.style.webkitBackdropFilter = 'blur(10px)';
    selector.style.transition = 'all 0.3s ease';
    
    selector.addEventListener('change', (e) => window.changeLanguage(e.target.value));
    
    selector.addEventListener('mouseenter', () => {
      selector.style.background = 'rgba(255, 255, 255, 0.15)';
      selector.style.borderColor = 'var(--accent, #c8922a)';
      selector.style.boxShadow = '0 0 10px rgba(200, 146, 42, 0.3)';
    });
    selector.addEventListener('mouseleave', () => {
      selector.style.background = 'rgba(255, 255, 255, 0.07)';
      selector.style.borderColor = 'var(--border-glass, rgba(255, 255, 255, 0.15))';
      selector.style.boxShadow = 'none';
    });

    const themeBtn = document.getElementById('theme-btn');
    if (themeBtn && themeBtn.parentElement === navActions) {
      navActions.insertBefore(selector, themeBtn);
    } else {
      // If theme-btn is nested, find the nesting structure or just append
      const nestedBtn = navActions.querySelector('#theme-btn');
      if (nestedBtn && nestedBtn.parentElement) {
        nestedBtn.parentElement.insertBefore(selector, nestedBtn);
      } else {
        navActions.appendChild(selector);
      }
    }
  }
}

// Run engine on page load
document.addEventListener('DOMContentLoaded', () => {
  injectLanguageSelector();
  const savedLang = localStorage.getItem('eos_lang') || 'en';
  applyTranslations(savedLang);
});
