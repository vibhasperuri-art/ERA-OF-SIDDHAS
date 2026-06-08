// js/api.js - Client side API wrapper & real-time WebSocket connection

// ─── Smart API URL: auto-detect local vs cloud ───
// When running locally (localhost / 127.0.0.1 / file://), use local server.
// When on GitHub Pages or any other host, use the Render cloud API.
const RENDER_API_URL = "https://era-of-siddhas.onrender.com";
const isLocal = (
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1" ||
  window.location.protocol === "file:"
);
const API_BASE = isLocal
  ? (window.location.protocol === "file:" ? "http://127.0.0.1:8080/api" : window.location.origin + "/api")
  : RENDER_API_URL + "/api";
const WS_URL = isLocal
  ? "ws://127.0.0.1:8080/ws"
  : RENDER_API_URL.replace("https://", "wss://").replace("http://", "ws://") + "/ws";


window.EOS_API = {
  async onboardAdmin(name, username, password, inviteCode) {
    try {
      const res = await fetch(`${API_BASE}/admin/onboard`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, username, password, invite_code: inviteCode })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error onboarding admin:", e);
      return null;
    }
  },

  async loginAdmin(username, password) {
    try {
      const res = await fetch(`${API_BASE}/admin/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });
      const resData = await res.json();
      if (res.ok && resData.status === "success") {
        localStorage.setItem('eos_user_name', resData.username);
        localStorage.setItem('eos_role', 'admin');
      }
      return resData;
    } catch (e) {
      console.error("API Error logging in admin:", e);
      return null;
    }
  },

  async onboardSeeker(data) {
    try {
      const res = await fetch(`${API_BASE}/onboard`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      const resData = await res.json();
      if (res.ok) {
        localStorage.setItem('eos_user_name', resData.username);
        localStorage.setItem('eos_role', resData.username === 'admin' ? 'admin' : 'seeker');
      }
      return resData;
    } catch (e) {
      console.error("API Error onboarding seeker:", e);
      return null;
    }
  },
  
  async getSeeker(username) {
    try {
      const res = await fetch(`${API_BASE}/seeker/${encodeURIComponent(username)}`);
      if (res.ok) return await res.json();
    } catch (e) {
      console.error("API Error fetching seeker:", e);
    }
    return null;
  },

  async completeCourseLesson(pillar, course, grade) {
    const seeker = localStorage.getItem('eos_user_name');
    if (!seeker) return null;
    try {
      const res = await fetch(`${API_BASE}/progress/complete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ seeker_username: seeker, pillar, course, grade })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error completing lesson:", e);
      return null;
    }
  },

  async saveReflection(pillar, course, content, status = "private") {
    const seeker = localStorage.getItem('eos_user_name');
    if (!seeker) return null;
    try {
      const res = await fetch(`${API_BASE}/reflections`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ seeker_username: seeker, pillar, course, content, status })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error saving reflection:", e);
      return null;
    }
  },

  async sendGuruChatMessage(pillar, message, history) {
    try {
      const res = await fetch(`${API_BASE}/guru/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pillar, message, history })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error in Socratic Guru chat:", e);
      return null;
    }
  },


  async shareReflection(reflectionId) {
    try {
      const res = await fetch(`${API_BASE}/reflections/share`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: parseInt(reflectionId) })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error sharing reflection:", e);
      return null;
    }
  },

  async getSanghaFeed() {
    try {
      const res = await fetch(`${API_BASE}/sangha/feed`);
      return await res.json();
    } catch (e) {
      console.error("API Error fetching Sangha feed:", e);
      return [];
    }
  },

  async adminGetSeekers() {
    try {
      const res = await fetch(`${API_BASE}/admin/seekers`);
      return await res.json();
    } catch (e) {
      console.error("API Error fetching admin seekers:", e);
      return [];
    }
  },

  async adminGetAlerts() {
    try {
      const res = await fetch(`${API_BASE}/admin/alerts`);
      return await res.json();
    } catch (e) {
      console.error("API Error fetching admin alerts:", e);
      return [];
    }
  },

  async adminCreateAlert(title, body, type = "alert-gold") {
    try {
      const res = await fetch(`${API_BASE}/admin/alerts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, body, type })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error creating admin alert:", e);
      return null;
    }
  },

  async adminBroadcast(message, type = "warning") {
    try {
      const res = await fetch(`${API_BASE}/admin/broadcast`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, type })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error posting admin broadcast:", e);
      return null;
    }
  },

  async addAdminStory(pillar, title, desc, content) {
    try {
      const res = await fetch(`${API_BASE}/admin/stories`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pillar, title, desc, content })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error adding admin story:", e);
      return null;
    }
  },

  async addAdminActivity(pillar, title, desc, actionLink) {
    try {
      const res = await fetch(`${API_BASE}/admin/activities`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pillar, title, desc, action_link: actionLink })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error adding admin activity:", e);
      return null;
    }
  },

  async addAdminSimulation(pillar, title, desc, actionLink) {
    try {
      const res = await fetch(`${API_BASE}/admin/simulations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pillar, title, desc, action_link: actionLink })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error adding admin simulation:", e);
      return null;
    }
  },

  async getAllCustomContent() {
    try {
      const res = await fetch(`${API_BASE}/content/all`);
      return await res.json();
    } catch (e) {
      console.error("API Error fetching custom content:", e);
      return { stories: [], activities: [], simulations: [] };
    }
  },

  async addAdminArticle(category, title, author, summary, content, imageUrl) {
    try {
      const res = await fetch(`${API_BASE}/admin/articles`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category, title, author, summary, content, image_url: imageUrl })
      });
      return await res.json();
    } catch (e) {
      console.error("API Error adding admin article:", e);
      return null;
    }
  },

  async getPublicArticles() {
    try {
      const res = await fetch(`${API_BASE}/public/articles`);
      return await res.json();
    } catch (e) {
      console.error("API Error fetching public articles:", e);
      return [];
    }
  }
};

// WebSocket connection management with auto-reconnect
let ws = null;
let reconnectTimer = null;

function connectWS() {
  if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
    return;
  }
  
  ws = new WebSocket(WS_URL);
  
  ws.onopen = () => {
    console.log("WebSocket connected to Sangha Hub.");
    updateIndicator(true);
    if (reconnectTimer) {
      clearInterval(reconnectTimer);
      reconnectTimer = null;
    }
  };
  
  ws.onclose = () => {
    console.log("WebSocket closed. Reconnecting in 5s...");
    updateIndicator(false);
    if (!reconnectTimer) {
      reconnectTimer = setInterval(connectWS, 5000);
    }
  };
  
  ws.onerror = (e) => {
    console.error("WebSocket error:", e);
    updateIndicator(false);
  };
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      handleWSMessage(data);
    } catch (e) {
      console.error("Error parsing WebSocket message:", e);
    }
  };
}

function updateIndicator(isOnline) {
  const dots = document.querySelectorAll(".eos-connection-indicator");
  dots.forEach(dot => {
    if (isOnline) {
      dot.classList.add("online");
      dot.title = "Connected to Sangha Hub (Real-time syncing active)";
      dot.style.background = "#2eb8a6";
      dot.style.boxShadow = "0 0 8px #4df5e2";
    } else {
      dot.classList.remove("online");
      dot.title = "Offline Mode (Reconnecting...)";
      dot.style.background = "#7a8288";
      dot.style.boxShadow = "none";
    }
  });
}

function handleWSMessage(data) {
  // 1. Dispatch custom event for page listeners (e.g. Sangha Feed UI updates)
  window.dispatchEvent(new CustomEvent("eos-ws-message", { detail: data }));
  
  // 2. Universal handle for alerts or broadcasts showing popup notifications
  if (data.type === "broadcast" || data.type === "alert") {
    showSystemNotificationModal(data);
  }
}

function showSystemNotificationModal(data) {
  // Remove existing modals if any
  const oldModal = document.getElementById("eos-system-broadcast-modal");
  if (oldModal) oldModal.remove();
  
  const modal = document.createElement("div");
  modal.id = "eos-system-broadcast-modal";
  modal.style.position = "fixed";
  modal.style.top = "0";
  modal.style.left = "0";
  modal.style.width = "100vw";
  modal.style.height = "100vh";
  modal.style.background = "rgba(0, 0, 0, 0.75)";
  modal.style.display = "flex";
  modal.style.justifyContent = "center";
  modal.style.alignItems = "center";
  modal.style.zIndex = "99999";
  modal.style.backdropFilter = "blur(6px)";
  
  const isAlert = data.type === "alert";
  const title = isAlert ? data.title : "🔱 Gurukula Broadcast Announcement";
  const content = isAlert ? data.body : data.content;
  const border = data.alertType === "alert-ember" ? "2px solid #ff4d4d" : "2px solid var(--gold, #c8922a)";
  const glow = data.alertType === "alert-ember" ? "rgba(255, 77, 77, 0.2)" : "rgba(200, 146, 42, 0.2)";
  
  modal.innerHTML = `
    <div style="background: var(--bg-secondary, #0a0000); border: ${border}; box-shadow: 0 0 30px ${glow}; border-radius: 8px; width: 90%; max-width: 480px; padding: 2rem; text-align: center; position: relative; animation: modalPop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);">
      <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔔</div>
      <h3 style="font-family: 'Cinzel', serif; color: var(--gold-bright, #ff4d4d); margin-bottom: 1rem; font-size: 1.3rem; letter-spacing: 0.05em;">${title}</h3>
      <p style="font-size: 1.05rem; line-height: 1.6; color: var(--text-primary, #ffffff); margin-bottom: 2rem;">${content}</p>
      <button onclick="document.getElementById('eos-system-broadcast-modal').remove()" class="action-btn" style="padding: 8px 24px; font-family: 'Cinzel', serif; font-size: 1rem; background: rgba(200, 146, 42, 0.15); border: 1.5px solid var(--gold-bright); color: var(--gold-bright); cursor: pointer; border-radius: 4px;">
        Acknowledge Wisdom
      </button>
    </div>
  `;
  
  // Inject keyframe if not present
  if (!document.getElementById("eos-modal-anim-style")) {
    const style = document.createElement("style");
    style.id = "eos-modal-anim-style";
    style.innerHTML = `
      @keyframes modalPop {
        from { transform: scale(0.85); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
      }
    `;
    document.head.appendChild(style);
  }
  
  document.body.appendChild(modal);
}

// Automatically connect WebSocket on page load and initialize connection indicator
document.addEventListener("DOMContentLoaded", () => {
  // Inject CSS for indicator and profile elements in navbar
  const role = localStorage.getItem('eos_role');
  const style = document.createElement("style");
  style.innerHTML = `
    .eos-connection-indicator {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #7a8288;
      display: inline-block;
      margin-left: 8px;
      cursor: help;
      transition: all 0.3s;
    }
    /* Profile tab special hover styles */
    .profile-nav-btn {
      border-color: var(--accent) !important;
      color: var(--text-primary) !important;
    }
    .profile-nav-btn:hover {
      box-shadow: 0 0 12px var(--accent-glow) !important;
    }
    ${role !== 'admin' ? '.admin-tab { display: none !important; }' : ''}
  `;
  document.head.appendChild(style);
  
  // Connect to WS
  connectWS();
  
  // Try to append indicator dot next to brand name if nav-brand is found
  const navBrand = document.querySelector(".nav-brand");
  if (navBrand && !document.querySelector(".eos-connection-indicator")) {
    const dot = document.createElement("span");
    dot.className = "eos-connection-indicator";
    navBrand.appendChild(dot);
    updateIndicator(ws && ws.readyState === WebSocket.OPEN);
  }

  // Check and append Seeker Profile tab if onboarded
  const baseBtn = document.querySelector('.nav-btn');
  if (baseBtn) {
    const navContainer = baseBtn.parentElement;
    if (!document.querySelector('.profile-nav-btn') && localStorage.getItem('eos_user_name')) {
      const profileBtn = document.createElement('a');
      profileBtn.href = '#';
      profileBtn.className = 'nav-btn profile-nav-btn';
      profileBtn.innerHTML = '👤 Profile';
      profileBtn.onclick = (e) => {
        e.preventDefault();
        window.openProfileModal();
      };
      
      // Insert before admin-tab (Admin) if it exists, or insert before theme buttons, or append at end
      const adminTab = navContainer.querySelector('.admin-tab');
      if (adminTab) {
        navContainer.insertBefore(profileBtn, adminTab);
      } else {
        const firstThemeBtn = navContainer.querySelector('.theme-btn');
        if (firstThemeBtn) {
          const themeContainer = firstThemeBtn.parentElement;
          if (themeContainer && themeContainer.parentElement === navContainer) {
            navContainer.insertBefore(profileBtn, themeContainer);
          } else {
            navContainer.insertBefore(profileBtn, firstThemeBtn);
          }
        } else {
          navContainer.appendChild(profileBtn);
        }
      }
    }
  }
});

// Profile modal global control methods
window.openProfileModal = function() {
  let modal = document.getElementById('eos-profile-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'eos-profile-modal';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.background = 'rgba(0, 0, 0, 0.75)';
    modal.style.display = 'none';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.zIndex = '999999';
    modal.style.backdropFilter = 'blur(10px)';
    
    modal.onclick = (e) => {
      if (e.target === modal) window.closeProfileModal();
    };
    
    document.body.appendChild(modal);
  }
  
  const username = localStorage.getItem('eos_user_name') || 'Seeker';
  const role = localStorage.getItem('eos_role') || 'seeker';
  const grade = localStorage.getItem('eos_user_grade') || localStorage.getItem('era_of_siddhas_grade') || 'Mumukshu';
  const age = localStorage.getItem('eos_user_age') || 'N/A';
  const interests = localStorage.getItem('eos_user_interests') || 'N/A';
  const discovery = localStorage.getItem('eos_user_discovery') || 'N/A';
  const ideology = localStorage.getItem('eos_user_ideology') || 'N/A';
  const wake = localStorage.getItem('eos_user_schedule_wake') || 'N/A';
  const study = localStorage.getItem('eos_user_schedule_study') || 'N/A';
  const sleep = localStorage.getItem('eos_user_schedule_sleep') || 'N/A';
  const onboardTime = localStorage.getItem('eos_onboarded_time') 
    ? new Date(localStorage.getItem('eos_onboarded_time')).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })
    : 'N/A';
  
  let avatarChar = username.charAt(0).toUpperCase();
  if (username.toLowerCase() === 'admin') avatarChar = '👁';
  
  let levelColor = '#7a8288';
  let levelBg = 'rgba(122, 130, 136, 0.1)';
  if (grade.toLowerCase() === 'shishya') {
    levelColor = '#c4892a';
    levelBg = 'rgba(196, 137, 42, 0.15)';
  } else if (grade.toLowerCase() === 'sadhaka') {
    levelColor = '#ffb020';
    levelBg = 'rgba(255, 176, 32, 0.15)';
  } else if (grade.toLowerCase() === 'siddha') {
    levelColor = '#2eb8a6';
    levelBg = 'rgba(46, 184, 166, 0.15)';
  }
  
  modal.innerHTML = `
    <div class="profile-card-modal" style="background: var(--bg-secondary, #0a0000); border: 2px solid var(--border-glass, rgba(200,146,42,0.2)); box-shadow: 0 8px 32px var(--glow, rgba(200,146,42,0.15)); border-radius: 12px; width: 90%; max-width: 460px; padding: 2rem; position: relative; color: var(--text-primary, #fff); font-family: 'Outfit', sans-serif; animation: modalPop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);">
      <button onclick="window.closeProfileModal()" style="position: absolute; top: 15px; right: 15px; background: none; border: none; color: var(--text-muted, #7a8288); font-size: 1.5rem; cursor: pointer; transition: color 0.2s;" onmouseover="this.style.color='var(--accent, #c8922a)'" onmouseout="this.style.color='var(--text-muted)'">×</button>
      
      <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 1.5rem;">
        <div style="width: 70px; height: 70px; border-radius: 50%; background: var(--accent-glow, rgba(200,146,42,0.1)); border: 2px solid var(--accent, #c8922a); display: flex; justify-content: center; align-items: center; font-size: 2.2rem; font-family: 'Cinzel', serif; color: var(--gold-bright, #c8922a); margin-bottom: 0.8rem; box-shadow: 0 0 15px var(--accent-glow);">
          ${avatarChar}
        </div>
        <h3 style="font-family: 'Cinzel', serif; font-size: 1.4rem; letter-spacing: 0.05em; margin: 0; color: var(--text-primary, #fff);">${username}</h3>
        <span style="font-family: 'Cinzel', serif; font-size: 0.8rem; letter-spacing: 0.15em; font-weight: 600; text-transform: uppercase; color: ${levelColor}; background: ${levelBg}; border: 1px solid ${levelColor}; padding: 3px 10px; border-radius: 20px; margin-top: 0.5rem; display: inline-block;">
          ${grade}
        </span>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 0.8rem; font-size: 0.95rem; border-top: 1px solid var(--border-glass, rgba(255,255,255,0.08)); padding-top: 1.2rem; margin-bottom: 1.8rem;">
        <div style="display: flex; justify-content: space-between;"><span style="color: var(--text-muted, #7a8288);">Age:</span><span style="font-weight: 500;">${age}</span></div>
        <div style="display: flex; justify-content: space-between;"><span style="color: var(--text-muted, #7a8288);">Interests:</span><span style="font-weight: 500; text-align: right; max-width: 250px;">${interests}</span></div>
        <div style="display: flex; justify-content: space-between;"><span style="color: var(--text-muted, #7a8288);">Ideology:</span><span style="font-weight: 500; text-align: right; max-width: 250px;">${ideology}</span></div>
        <div style="display: flex; justify-content: space-between; border-top: 1px dashed var(--border-glass, rgba(255,255,255,0.04)); padding-top: 0.5rem;"><span style="color: var(--text-muted, #7a8288);">Agamic Clock Routine:</span><span style="font-weight: 500; font-family: monospace;">🌅 ${wake} | 📚 ${study} | 🌌 ${sleep}</span></div>
        <div style="display: flex; justify-content: space-between; border-top: 1px dashed var(--border-glass, rgba(255,255,255,0.04)); padding-top: 0.5rem;"><span style="color: var(--text-muted, #7a8288);">Onboarded:</span><span style="font-weight: 500;">${onboardTime}</span></div>
      </div>
      
      <div style="display: flex; gap: 10px; justify-content: stretch;">
        <button onclick="window.logoutSeeker()" style="flex: 1; padding: 10px; background: rgba(181, 42, 42, 0.1); border: 1.5px solid #ff4d4d; color: #ff4d4d; font-family: 'Cinzel', serif; font-size: 0.9rem; cursor: pointer; border-radius: 4px; transition: all 0.2s;" onmouseover="this.style.background='rgba(181, 42, 42, 0.2)'" onmouseout="this.style.background='rgba(181, 42, 42, 0.1)'">
          Reset Journey
        </button>
        <button onclick="window.closeProfileModal()" style="flex: 1; padding: 10px; background: rgba(200, 146, 42, 0.1); border: 1.5px solid var(--accent, #c8922a); color: var(--gold-bright, #c8922a); font-family: 'Cinzel', serif; font-size: 0.9rem; cursor: pointer; border-radius: 4px; transition: all 0.2s;" onmouseover="this.style.background='rgba(200, 146, 42, 0.2)'" onmouseout="this.style.background='rgba(200, 146, 42, 0.1)'">
          Acknowledge
        </button>
      </div>
    </div>
  `;
  
  modal.style.display = 'flex';
};

window.closeProfileModal = function() {
  const modal = document.getElementById('eos-profile-modal');
  if (modal) modal.style.display = 'none';
};

window.logoutSeeker = function() {
  if (confirm("Are you sure you want to reset your Gurukulam journey? All your answers and local progress will be cleared.")) {
    localStorage.clear();
    window.location.href = 'index.html';
  }
};
