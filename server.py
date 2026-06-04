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
