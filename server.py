import os
import json
import sqlite3
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Era of Siddhas API & WebSocket Server")

# Enable CORS for local testing flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "database.db"

# Initialize SQLite Database Tables
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS seekers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        name TEXT,
        age INTEGER,
        grade TEXT,
        interest TEXT,
        discovery TEXT,
        ideology TEXT,
        wake_schedule TEXT,
        study_schedule TEXT,
        sleep_schedule TEXT,
        created_at TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seeker_username TEXT,
        course_id TEXT,
        pillar TEXT,
        grade TEXT,
        completed INTEGER DEFAULT 0,
        completed_at TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reflections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seeker_username TEXT,
        course_id TEXT,
        pillar TEXT,
        content TEXT,
        status TEXT DEFAULT 'private',
        created_at TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        body TEXT,
        type TEXT DEFAULT 'alert-gold',
        resolved INTEGER DEFAULT 0,
        created_at TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pillar TEXT,
        title TEXT,
        desc TEXT,
        content TEXT,
        created_at TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pillar TEXT,
        title TEXT,
        desc TEXT,
        action_link TEXT,
        created_at TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pillar TEXT,
        title TEXT,
        desc TEXT,
        action_link TEXT,
        created_at TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        title TEXT,
        author TEXT,
        summary TEXT,
        content TEXT,
        image_url TEXT,
        created_at TEXT
    )
    """)
    
    
    # Seed default articles if empty
    cursor.execute("SELECT COUNT(*) FROM articles")
    if cursor.fetchone()[0] == 0:
        now_str = datetime.now().isoformat()
        default_articles = [
            (
                "research",
                "The Atharvaveda of City Planning: Prana, Protection, and the Blueprint of Madurai",
                "Siddha Council",
                "Explore how the Atharvaveda provides the spiritual prana (life force) and energetic shield for sacred city planning, working in tandem with the Mayamatam and Agamas.",
                "<h3>The Energetic Soul of Nagara Nirmana</h3><p>While the Shilpa Shastras (like the <i>Manasara</i>) and the Agamas provide the structural and geometric blueprint (the physical anatomy and measurements), the <b>Atharvaveda</b> provides the <i>prana</i> (life force), the ritual execution, and the protective wisdom required to make that physical structure actually \"alive\" and divine. Without the energetic rituals of the Atharvaveda, a city built using only the Agamas would just be a mathematically perfect, but ultimately \"dead\" pile of stones.</p><h3>The Wisdom (The Knowing): Earth as a Living Organism</h3><p>The Atharvaveda (housing the Sthapatya Veda) teaches that land is not dead dirt, but a living, breathing organism with energy meridians (Nad\u012bs), similar to the human body. It gives the wisdom to identify the <i>marma sthanas</i> (vital energy points) of a geographical site so that the central temple (Brahmasthana) can be placed exactly on the earth\'s spiritual nerve center. Furthermore, by balancing the five elements (Pancha Bhoota) in the physical geography of the city, it prevents societal decay, poverty, and discord. Deep philosophical hymns are dedicated to <b>Vastospati</b> (the deity of physical spaces), showing that a city is a shared dwelling for humans, nature, and divine forces.</p><h3>The Execution (The Doing): Shielding and Hydrology</h3><p>The Atharvaveda guides the practical execution of consecration and protection. Before building, the land must be pacified and healed using specific purification rituals (Bhoomi Pujan and Vastu Shanti), utilizing hymns like <b>Book 3, Hymn 12</b> to invoke the creator Tvastar for foundation-raising. Border protection is established through <i>Nagara Raksha</i>, utilizing Rakshoghna and Krivinashana hymns to project energetic shields at the outer walls and the four cardinal gates. Water hydrology, invoking the rain deity Parjanya, guides the digging of temple tanks (like the Potramarai Kulam in Madurai) and river alignments to ensure prosperity. Class zoning is structured under Atharvanic principles of statecraft to maintain social harmony.</p><h3>The limits & Hand-off: The Anesthetic vs the Scalpel</h3><p>To understand the Atharvaveda\'s effectiveness, one must also recognize its limits. It will not detail the exact width of streets, the proportions of Gopurams, or which stone to carve. For these structural measurements, it hands off to the Agamas (Kamikagama) and Shilpa Shastras (Mayamatam). Thus, the Atharvaveda behaves like the <b>anesthetic, life-support, and blessing</b> (spiritual execution) to the <b>scalpel and anatomical charts</b> (structural execution) of the Shastras. Both are mandatory to construct a living temple city.</p>",
                "flying_manuscript.png",
                now_str
            ),
            (
                "research",
                "The Sacred Geometry of Nagara Nirmana: How the Divine Reality is Built",
                "Siddha Council",
                "A deep dive into the Vastu Purusha Mandala, the 9x9 Paramasayika grid, and the living lotus geometry of Madurai Sthalam.",
                "<h3>The Sacred Texts of Nagara Nirmana</h3><p>While the term 'Samhita' broadly refers to compendiums or collections of knowledge, the rules for building a divine city are found across Shilpa Shastras (architectural manuals), Agamas (temple and societal codes), and Puranic Samhitas.</p><h4>A. The Shilpa Shastras (The Architectural Manuals)</h4><ul><li><b>Manasara (Manasara Shilpa Shastra):</b> This is the ultimate encyclopedia of Vastu. It contains a specific section called Nagara Vidhana (Rules for Towns). It categorizes settlements into eight types (from a small village to a massive capital city) and explains how to lay out the Vastu Purusha Mandala (the cosmic grid) to ensure the city aligns with solar and magnetic energies.</li><li><b>Mayamatam (Mayamata):</b> Attributed to the divine architect Maya Danava, this text is the absolute authority on Dravidian (South Indian) architecture. It meticulously details how to build temple cities, the exact dimensions of streets, and the zoning of different castes and professions around the central temple.</li><li><b>Samarangana Sutradhara:</b> Written by King Bhoja (11th century), this text deals extensively with Nagara (city) planning, focusing on royal capitals, the layout of the central palace/temple, and the aesthetic geometry of the city.</li><li><b>Aparajita Priccha:</b> A 12th-century text formatted as a dialogue. It contains exhaustive details on town planning, street widths (Rajamarga), drainage, and the placement of markets and guilds.</li></ul><h4>B. The Samhitas and Puranas</h4><ul><li><b>Brihat Samhita (by Varahamihira):</b> Chapter 53 (Vastu-vidya) provides rules for selecting land, testing soil, and laying out the grid for a city. It dictates that a city should be shaped like a square, rectangle, or circle, with the primary deity at the exact center.</li><li><b>Vishnudharmottara Purana:</b> Contains chapters dedicated to Nagara Nirmana, emphasizing that a city must be protected by water bodies (moats/rivers) and walls, with the temple acting as the spiritual anchor.</li><li><b>Agni Purana & Matsya Purana:</b> Both contain detailed encyclopedic chapters on town planning, specifying the widths of concentric streets and the placement of different social classes (Varnas) based on their proximity to the divine center.</li></ul><h4>C. The Agamas (The Living Codes of the Temple City)</h4><ul><li><b>Kamikagama, Karanagama, and Suprabhedagama:</b> In South India, the Agamas are the supreme law. They do not just dictate how to carve the deity; they dictate how the entire town must be built around the deity. They prescribe the Prakaras (concentric rectangular walls and streets) that protect the sanctum from the chaotic energies of the outside world.</li></ul><h3>The Blueprint: How the 'Divine Reality' is Built</h3><p>According to these texts, a divine city is built using the Vastu Purusha Mandala. For a major city, a grid of 81 squares (9x9), known as the <b>Paramasayika mandala</b>, is drawn on the earth.</p><ul><li><b>The Brahmasthana (The Divine Center):</b> The central squares of the grid are the Brahmasthana (the seat of the Creator). This area is considered pure consciousness. No mortal is allowed to live here. It is exclusively reserved for the main Temple. This is the anchor of the city.</li><li><b>The Prakaras (The Concentric Layers):</b> As you move outward from the Brahmasthana, the energy transitions from pure spirit to pure matter. The city is built in concentric rectangular or circular layers.</li><li><b>The Zoning of Samsara (Worldly Life):</b><ul><li><i>Inner Ring:</i> Priests, Vedic scholars, and ascetics (Sattvic lifestyle, closest to the divine).</li><li><i>Middle Ring:</i> Rulers, warriors, merchants, and artisans (Rajasic lifestyle, the engine of society).</li><li><i>Outer Ring:</i> Agriculture, heavy industries, and labor (Tamasic/Earthly lifestyle).</li><li><i>The Periphery:</i> Cremation grounds and specific polluting industries (like tanneries) are placed far outside the city gates to protect the spiritual purity of the center.</li></ul></li></ul><h3>The Ultimate Example: Madurai Sthalam</h3><p>Madurai is the flawless, living embodiment of the Mayamatam and the Agamas. It is known in the texts as a <b>Padma Vana</b> (Lotus Forest) or <b>Kudal</b> (The Confluence).</p><ul><li><b>The Center (The Pistil of the Lotus):</b> At the absolute Brahmasthana sits the Meenakshi Sundareswarar Temple. Shiva (Sundareswarar) represents pure, formless Consciousness, and Shakti (Meenakshi) represents the dynamic Energy of the universe. They are the still point of the turning world.</li><li><b>The Streets (The Petals of the Lotus):</b> Radiating outward from the temple are concentric rectangular streets, named after the Tamil months: Chitrai Veedhi (Innermost), Aavani Moola Veedhi, Masi Veedhi, and Aadi Veedhi (Outermost).</li><li><b>The Transformation of Samsara into Dharma:</b> In a modern city, the center is usually a bank, a mall, or a corporate plaza (representing greed and commerce). In Madurai, the center is the Divine. Because the streets wrap around the temple, every time a citizen walks to the market, goes to school, or visits a friend, they are inherently performing Pradakshina (circumambulation) of God. Samsara (worldly life) is not opposed to spirituality; it physically revolves around it. The commerce of the outer streets is protected and sanctified by the stillness of the inner sanctum.</li><li><b>The Water Element:</b> The texts demand a water body for purification. Madurai is built on the banks of the Vaigai River, and the temple itself houses the Potramarai Kulam (Golden Lotus Tank), which historically served as the Sangam (the supreme academy of Tamil literature and spirituality).</li></ul><h3>Summary: Environment Dictates Consciousness</h3><p>The ancient texts of Nagara Nirmana realized a profound psychological and spiritual truth: Environment dictates consciousness. If you build a city with a shopping mall at the center, the society revolves around consumption. If you build a city with a stock exchange at the center, the society revolves around wealth. But if you build the city like Madurai—with the Temple (the symbol of eternal truth and inner peace) at the absolute center—then the entire society, no matter how busy their Samsara gets, is always held in the loving, gravitational embrace of the Divine.</p>",
                "sacred_city.png",
                now_str
            ),
            (
                "research",
                "Sacred Acoustics & Cardiac Rhythms: The Geometry of Chidambaram",
                "Vibhas Peruri & Council",
                "An empirical exploration of how the Nataraja temple dimensions resonate with the human heart rate variability (HRV).",
                "<p>The ancient temple of Nataraja in Chidambaram is not merely a place of worship, but a structural marvel designed to stabilize human bio-energetic fields. By analyzing its dimensions, we find that the 21,600 roof tiles and 72,000 iron nails mirror the daily respiration rate and nadis of the human body.</p><p>Modern cardiac research has demonstrated that stepping inside highly resonant stone chambers triggers a shift in autonomic nervous system balance. The heart rate variability stabilizes, promoting vagal tone and parasympathetic dominance. This aligns the physiological self with the higher Agamic levels of consciousness.</p>",
                "sacred_city.png",
                now_str
            ),
            (
                "story",
                "The Descent of the Astra: Parashurama\'s Mahendra Training",
                "Siddha Tradition",
                "Explore the legends of Mount Mahendra, where Sage Parashurama initiated warriors into higher dimensions of weapon acoustics.",
                "<p>The scriptures of Dhanurveda outline the distinction between simple physical weapons (Śāstras) and mental sound-resonated weapons (Astras). On Mount Mahendra, the warrior-sage Parashurama trained Drona and Karna. An Astra was not propelled by gunpowder, but by the focused concentration (Dharana) and vocal resonance (Mantra) of the practitioner.</p><p>This training demanded complete control of the vital breaths, matching the chest resonance with laryngeal and sinus projections to anchor sound vibrations in physical structures. The lesson of Mount Mahendra remains: power is a form of acoustic alignment, and only a steady mind can command force without destruction.</p>",
                "ancient_weapons.png",
                now_str
            ),
            (
                "magazine",
                "Era of Siddhas Magazine — Issue I: Resonating Temple Cities",
                "Siddha Editorial",
                "Our launch edition covering Vastu Purusha Mandala layouts, town thermodynamic principles, and spiritual architecture.",
                "<p>Welcome to the first edition of the Era of Siddhas Magazine. In this edition, we examine the ancient town planning models outlined in the Samarangana Sutradhara. By setting the thermodynamic grids and central space (Brahma Sthana) open to the sky, ancient architects created natural cooling drafts that kept temples comfortable during harsh monsoons.</p><p>We also discuss how these concepts are being implemented in modern eco-villages and sustainable residential plans to restore the connection between human dwelling and nature.</p>",
                "flying_manuscript.png",
                now_str
            )
        ]
        cursor.executemany("""
        INSERT INTO articles (category, title, author, summary, content, image_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, default_articles)
    
    conn.commit()
    conn.close()

# Models
class SeekerOnboard(BaseModel):
    name: str
    age: int
    grade: str
    interest: str
    discovery: str
    ideology: str
    wake: str
    study: str
    sleep: str

class LessonCompletion(BaseModel):
    seeker_username: str
    pillar: str
    course: str
    grade: str

class ReflectionSave(BaseModel):
    seeker_username: str
    pillar: str
    course: str
    content: str
    status: Optional[str] = "private"

class ReflectionShare(BaseModel):
    id: int

class AlertCreate(BaseModel):
    title: str
    body: str
    type: str = "alert-gold"

class BroadcastMessage(BaseModel):
    message: str
    type: str = "warning"

class StoryCreate(BaseModel):
    pillar: str
    title: str
    desc: str
    content: str

class ActivityCreate(BaseModel):
    pillar: str
    title: str
    desc: str
    action_link: str

class SimulationCreate(BaseModel):
    pillar: str
    title: str
    desc: str
    action_link: str

class ArticleCreate(BaseModel):
    category: str
    title: str
    author: str
    summary: str
    content: str
    image_url: Optional[str] = ""

class GuruChatRequest(BaseModel):
    pillar: str
    message: str
    history: List[Dict[str, str]]


# Connection Manager for WebSockets
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Handle connection closed issues silently
                pass

manager = ConnectionManager()

# Global communal marathon progress counts
marathon_counts = {"chanting": 342, "breathing": 84}

# Startup event
@app.on_event("startup")
async def startup_event():
    init_db()
    print("SQLite Database initialized at:", DB_PATH)

# REST API ENDPOINTS

@app.post("/api/onboard")
async def onboard_seeker(data: SeekerOnboard):
    # Normalize name as username
    username = data.name.strip().lower().replace(" ", "_")
    if not username:
        raise HTTPException(status_code=400, detail="Invalid seeker name")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now_str = datetime.now().isoformat()
    try:
        cursor.execute("""
        INSERT INTO seekers (username, name, age, grade, interest, discovery, ideology, wake_schedule, study_schedule, sleep_schedule, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            name=excluded.name,
            age=excluded.age,
            grade=excluded.grade,
            interest=excluded.interest,
            discovery=excluded.discovery,
            ideology=excluded.ideology,
            wake_schedule=excluded.wake_schedule,
            study_schedule=excluded.study_schedule,
            sleep_schedule=excluded.sleep_schedule
        """, (username, data.name, data.age, data.grade, data.interest, data.discovery, data.ideology, data.wake, data.study, data.sleep, now_str))
        
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    conn.close()
    return {"status": "success", "username": username, "grade": data.grade}

@app.get("/api/seeker/{username}")
async def get_seeker(username: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    seeker = cursor.execute("SELECT * FROM seekers WHERE username = ?", (username,)).fetchone()
    if not seeker:
        conn.close()
        raise HTTPException(status_code=404, detail="Seeker not found")
        
    # Get completed courses
    progress_rows = cursor.execute("SELECT * FROM progress WHERE seeker_username = ?", (username,)).fetchall()
    completed_courses = [dict(row) for row in progress_rows]
    
    conn.close()
    
    seeker_dict = dict(seeker)
    return {
        "profile": seeker_dict,
        "progress": completed_courses
    }

@app.post("/api/progress/complete")
async def complete_lesson(data: LessonCompletion):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now_str = datetime.now().isoformat()
    try:
        # Check if record exists
        existing = cursor.execute(
            "SELECT id FROM progress WHERE seeker_username = ? AND course_id = ? AND pillar = ? AND grade = ?",
            (data.seeker_username, data.course, data.pillar, data.grade)
        ).fetchone()
        
        if not existing:
            cursor.execute(
                "INSERT INTO progress (seeker_username, course_id, pillar, grade, completed, completed_at) VALUES (?, ?, ?, ?, 1, ?)",
                (data.seeker_username, data.course, data.pillar, data.grade, now_str)
            )
            conn.commit()
            
            # Broadcast milestone event to Sangha WebSocket clients
            grade_labels = { "primary": "Grades 1-5", "secondary": "Grades 6-12", "ug": "UG / PG", "phd": "Higher Knowledge (PhD)" }
            label = grade_labels.get(data.grade, data.grade)
            milestone_msg = {
                "type": "milestone",
                "author": "System",
                "content": f"🎉 Seeker <strong>{data.seeker_username}</strong> completed the <strong>{data.course}</strong> course at the <strong>{label}</strong> level!",
                "timestamp": now_str
            }
            await manager.broadcast(milestone_msg)
            
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    conn.close()
    return {"status": "success", "completed_at": now_str}

@app.post("/api/reflections")
async def save_reflection(data: ReflectionSave):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now_str = datetime.now().isoformat()
    try:
        cursor.execute(
            "INSERT INTO reflections (seeker_username, course_id, pillar, content, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (data.seeker_username, data.course, data.pillar, data.content, data.status, now_str)
        )
        conn.commit()
        ref_id = cursor.lastrowid
        
        if data.status == "shared":
            # Broadcast live Sangha post
            post_msg = {
                "type": "post",
                "author": data.seeker_username,
                "content": data.content,
                "category": f"{data.pillar.capitalize()} Reflection",
                "timestamp": now_str
            }
            await manager.broadcast(post_msg)
            
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    conn.close()
    return {"status": "success", "id": ref_id}

@app.get("/api/reflections/{username}")
async def get_reflections(username: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    rows = cursor.execute("SELECT * FROM reflections WHERE seeker_username = ? ORDER BY id DESC", (username,)).fetchall()
    refs = [dict(row) for row in rows]
    conn.close()
    return refs

@app.post("/api/reflections/share")
async def share_reflection(data: ReflectionShare):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        ref = cursor.execute("SELECT * FROM reflections WHERE id = ?", (data.id,)).fetchone()
        if not ref:
            conn.close()
            raise HTTPException(status_code=404, detail="Reflection not found")
            
        cursor.execute("UPDATE reflections SET status = 'shared' WHERE id = ?", (data.id,))
        conn.commit()
        
        ref_dict = dict(ref)
        # Broadcast post to WebSocket
        post_msg = {
            "type": "post",
            "author": ref_dict["seeker_username"],
            "content": ref_dict["content"],
            "category": f"{ref_dict['pillar'].capitalize()} Reflection",
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast(post_msg)
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    conn.close()
    return {"status": "success"}

@app.get("/api/sangha/feed")
async def get_sangha_feed():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 1. Fetch shared reflections
    reflection_rows = cursor.execute(
        "SELECT seeker_username as author, content, pillar || ' Reflection' as category, created_at as timestamp FROM reflections WHERE status = 'shared' ORDER BY id DESC LIMIT 20"
    ).fetchall()
    
    # 2. Fetch milestone achievements
    progress_rows = cursor.execute(
        "SELECT seeker_username, course_id, grade, completed_at FROM progress WHERE completed = 1 ORDER BY id DESC LIMIT 20"
    ).fetchall()
    
    feed = []
    
    for row in reflection_rows:
        feed.append({
            "type": "post",
            "author": row["author"],
            "content": row["content"],
            "category": row["category"],
            "timestamp": row["timestamp"]
        })
        
    grade_labels = { "primary": "Grades 1-5", "secondary": "Grades 6-12", "ug": "UG / PG", "phd": "Higher Knowledge (PhD)" }
    for row in progress_rows:
        label = grade_labels.get(row["grade"], row["grade"])
        feed.append({
            "type": "milestone",
            "author": "System",
            "content": f"🎉 Seeker <strong>{row['seeker_username']}</strong> completed the <strong>{row['course_id']}</strong> course at the <strong>{label}</strong> level!",
            "category": "Milestone Achieved",
            "timestamp": row["completed_at"]
        })
        
    # Sort descending by timestamp
    feed.sort(key=lambda x: x["timestamp"], reverse=True)
    conn.close()
    return feed[:30]

@app.get("/api/marathon")
async def get_marathon():
    return marathon_counts

@app.post("/api/marathon/contribute")
async def contribute_marathon(data: dict):
    m_type = data.get("type")
    if m_type in marathon_counts:
        marathon_counts[m_type] += 1
        # Broadcast the marathon count update to all active websockets
        await manager.broadcast({
            "type": "marathon_update",
            "counts": marathon_counts
        })
        return {"status": "success", "counts": marathon_counts}
    return {"status": "error", "message": "Invalid type"}

# ADMIN ENDPOINTS

@app.get("/api/admin/seekers")
async def admin_get_seekers():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM seekers ORDER BY id DESC").fetchall()
    seekers = [dict(row) for row in rows]
    conn.close()
    return seekers

@app.get("/api/admin/alerts")
async def admin_get_alerts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM alerts WHERE resolved = 0 ORDER BY id DESC").fetchall()
    alerts = [dict(row) for row in rows]
    conn.close()
    return alerts

@app.post("/api/admin/alerts")
async def admin_create_alert(data: AlertCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    try:
        cursor.execute(
            "INSERT INTO alerts (title, body, type, resolved, created_at) VALUES (?, ?, ?, 0, ?)",
            (data.title, data.body, data.type, now_str)
        )
        conn.commit()
        alert_id = cursor.lastrowid
        
        # Broadcast alert to all active users via WebSocket
        alert_msg = {
            "type": "alert",
            "title": data.title,
            "body": data.body,
            "alertType": data.type,
            "timestamp": now_str
        }
        await manager.broadcast(alert_msg)
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    conn.close()
    return {"status": "success", "id": alert_id}

@app.post("/api/admin/broadcast")
async def admin_broadcast(data: BroadcastMessage):
    # Direct live broadcast to all active websockets without database record
    now_str = datetime.now().isoformat()
    broadcast_msg = {
        "type": "broadcast",
        "content": data.message,
        "broadcastType": data.type,
        "timestamp": now_str
    }
    await manager.broadcast(broadcast_msg)
    return {"status": "success", "recipients": len(manager.active_connections)}

@app.post("/api/admin/stories")
async def create_story(data: StoryCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    try:
        cursor.execute(
            "INSERT INTO stories (pillar, title, desc, content, created_at) VALUES (?, ?, ?, ?, ?)",
            (data.pillar, data.title, data.desc, data.content, now_str)
        )
        conn.commit()
        await manager.broadcast({
            "type": "content_update",
            "category": "story",
            "pillar": data.pillar,
            "title": data.title
        })
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()
    return {"status": "success"}

@app.post("/api/admin/activities")
async def create_activity(data: ActivityCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    try:
        cursor.execute(
            "INSERT INTO activities (pillar, title, desc, action_link, created_at) VALUES (?, ?, ?, ?, ?)",
            (data.pillar, data.title, data.desc, data.action_link, now_str)
        )
        conn.commit()
        await manager.broadcast({
            "type": "content_update",
            "category": "activity",
            "pillar": data.pillar,
            "title": data.title
        })
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()
    return {"status": "success"}

@app.post("/api/admin/simulations")
async def create_simulation(data: SimulationCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    try:
        cursor.execute(
            "INSERT INTO simulations (pillar, title, desc, action_link, created_at) VALUES (?, ?, ?, ?, ?)",
            (data.pillar, data.title, data.desc, data.action_link, now_str)
        )
        conn.commit()
        await manager.broadcast({
            "type": "content_update",
            "category": "simulation",
            "pillar": data.pillar,
            "title": data.title
        })
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()
    return {"status": "success"}

@app.get("/api/content/all")
async def get_all_custom_content():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    stories = [dict(r) for r in cursor.execute("SELECT * FROM stories ORDER BY id DESC").fetchall()]
    activities = [dict(r) for r in cursor.execute("SELECT * FROM activities ORDER BY id DESC").fetchall()]
    simulations = [dict(r) for r in cursor.execute("SELECT * FROM simulations ORDER BY id DESC").fetchall()]
    
    conn.close()
    return {
        "stories": stories,
        "activities": activities,
        "simulations": simulations
    }

@app.post("/api/admin/articles")
async def create_article(data: ArticleCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    try:
        cursor.execute(
            "INSERT INTO articles (category, title, author, summary, content, image_url, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (data.category, data.title, data.author, data.summary, data.content, data.image_url, now_str)
        )
        conn.commit()
        await manager.broadcast({
            "type": "content_update",
            "category": "article",
            "title": data.title
        })
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    conn.close()
    return {"status": "success"}

@app.get("/api/public/articles")
async def get_public_articles():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM articles ORDER BY id DESC").fetchall()
    articles = [dict(row) for row in rows]
    conn.close()
    return articles

@app.post("/api/guru/chat")
async def guru_chat(data: GuruChatRequest):
    pillar = data.pillar.lower()
    message = data.message
    history = data.history
    
    # Count how many messages are from the user
    user_msg_count = sum(1 for m in history if m.get("sender") == "user")
    
    response_text = ""
    complete = False
    
    if pillar == "nagara":
        if user_msg_count == 0:
            response_text = "You speak of physical placement, but how does the empty center—the Brahmasthana—connect to the unmanifest space within your own heart? If the center is cluttered, does the architecture truly stand?"
        elif user_msg_count == 1:
            response_text = "But if you rely on the alignment of walls and elements to find peace, are you not making your consciousness dependent on physical forms? Can a bound spirit be freed by a geometric alignment?"
        else:
            response_text = "Indeed. The Vastu Shastra teaches that outer structure is merely a physical support for inner expansion. When the microcosm is aligned, the wall ceases to divide, and the Brahmasthana merges with the infinite. Your transmission of Nagara Nirmana is validated. The sanctuary gates are open."
            complete = True
            
    elif pillar == "rājya" or pillar == "rajya":
        if user_msg_count == 0:
            response_text = "A noble reflection. But when you are surrounded by flatterers and the intoxicant of absolute authority, how do you distinguish genuine feedback from the echo chamber of your own ego? What is your mirror?"
        elif user_msg_count == 1:
            response_text = "You speak of vigilance, yet the very act of 'governing' carries the weight of doership (Kartrtva). If you believe you are the one protecting Dharma, has pride not already conquered your crown?"
        else:
            response_text = "Pragmatic and profound. The raja acts only as a trustee (Nimitta-matra) of the cosmic order. Real governance is Rajya Palanam—ruling the kingdom of one's mind first. Your transmission of Rajya Palanam is validated. The sanctuary gates are open."
            complete = True
            
    else:  # yuddham
        if user_msg_count == 0:
            response_text = "Fierce action is easy when fueled by anger or desire for victory. But if you have no attachment to the outcome, where does the fire to fight injustice come from? Does detachment not breed passivity?"
        elif user_msg_count == 1:
            response_text = "If you say you fight because it is your duty, who decides what is 'just'? If your sword is drawn in detachment, does it not become indifferent to the suffering it inflicts or heals?"
        else:
            response_text = "You have touched the core of Gita's wisdom. Action without attachment is not passive; it is the absolute flow of universal will through a purified instrument. You fight not for personal fruits, but to restore cosmic balance. Your transmission of Yuddham is validated. The sanctuary gates are open."
            complete = True
            
    return {"response": response_text, "complete": complete}




# WebSocket Endpoint for real-time updates and announcements
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Maintain connection alive, listen for ping/pong if necessary
            data = await websocket.receive_text()
            # If clients send messages, we can route them here.
            # Currently clients read feeds via REST, WebSocket is primary for server->client pushes.
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

# Serve explicit routes
@app.get("/")
async def get_index():
    return FileResponse("index.html")

# Serve all static files (fallback route, mounted at root)
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8080, reload=True)
