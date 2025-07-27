from fastapi import FastAPI, HTTPException, Depends, Form
import hashlib
import sqlite3
import jwt
from typing import Annotated
import config as cfg

app = FastAPI()

@app.post('/register')
def register(username: str = Form(...), password: str = Form(...)):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Username already exists")
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
        return {"status": "success"}
    except sqlite3.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")

@app.post('/login')
def login(username: str = Form(...), password: str = Form(...)):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password_hash)
            )
            user = cursor.fetchone()
            cursor.close()

            if user:
                payload = {
                    "username": username,
                    "best_score": user[3]
                }
                token = jwt.encode(payload, cfg.key, algorithm="HS256")
                return {"token": token}
            else:
                raise HTTPException(status_code=403, detail="Incorrect credentials")
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Database error")
    
@app.get('/abc')
def abc():
    return {"abc":"abc"}

@app.get('/scoreboard')
def scoreboard():
    try:
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users ORDER BY bscore DESC"
            )
            data = cursor.fetchall()
            cursor.close()
            return data
    except:
        raise HTTPException(status_code=500, detail='Internal server errror')

@app.post('/update')
def update_score(tkn: str = Form(...), scr: str = Form(...)):
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        try:
            decoded = jwt.decode(tkn, cfg.key, algorithms=["HS256"])
            username = decoded.get('username')
            cur.execute(f'UPDATE users SET bscore = bscore + {scr} WHERE username = \'{username}\'')
            conn.commit()
            return {'status': 'success'}
        except:
            raise HTTPException(status_code=403, detail='not verified')
        finally:
            cur.close()

@app.get('/add')
def add_planet(pid: int, uid: str):
    print(pid)
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        try:
            cur.execute(f"UPDATE users SET pids = pids || ' {str(pid)}' WHERE username = '{uid}'")
            conn.commit()
            return {'status': 'success'}
        except:
            return {'status':'failed'}
        finally:
            cur.close()

@app.get('/get')
def get_planet(uid: str):
    print(uid)
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        try:
            cur.execute(f"SELECT pids FROM users WHERE username = '{uid}'")
            return {'pids': str(cur.fetchone())}
        except:
            return {'status':'failed'}
        finally:
            cur.close()


@app.on_event("startup")
def init_db():
    with sqlite3.connect("db.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                bscore FLOAT DEFAULT 0.0,
                pids TEXT DEFAULT ''
            )
        """)
        conn.commit()