# database.py
import sqlite3
import requests
import streamlit as st

class Database:
    DB_PATH = "trip_planner.db"

    @staticmethod
    def _connect():
        return sqlite3.connect(Database.DB_PATH)

    @staticmethod
    def init():
        """Creates all tables on first run, and migrates older schemas if needed."""
        conn   = Database._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trips (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    city    TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trip_items (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    trip_id INTEGER,
                    item    TEXT,
                    checked BOOLEAN DEFAULT 0,
                    FOREIGN KEY(trip_id) REFERENCES trips(id)
                )
            """)
            existing_cols = [row[1] for row in cursor.execute("PRAGMA table_info(trip_items)")]
            if "checked" not in existing_cols:
                cursor.execute("ALTER TABLE trip_items ADD COLUMN checked BOOLEAN DEFAULT 0")
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def register(username, password):
        """Returns True on success, False if username already exists."""
        conn   = Database._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def login(username, password):
        """Returns user_id on success, None on failure."""
        conn   = Database._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?",
                           (username, password))
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    @staticmethod
    def save_trip(user_id, city, checklist_items):
        """Inserts a trip + its items."""
        conn   = Database._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO trips (user_id, city) VALUES (?, ?)",
                           (user_id, city))
            trip_id = cursor.lastrowid
            for item in checklist_items:
                checked = 1 if item["checked"] else 0
                cursor.execute(
                    "INSERT INTO trip_items (trip_id, item, checked) VALUES (?, ?, ?)",
                    (trip_id, item["text"], checked)
                )
            conn.commit()
            return True
        except sqlite3.OperationalError:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def load_trips(user_id, sort_mode="newest"):
        """Returns a sorted list of (id, city) tuples for the given user."""
        conn   = Database._connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, city FROM trips WHERE user_id = ? ORDER BY id DESC",
                (user_id,)
            )
            rows = cursor.fetchall()
        finally:
            conn.close()

        if sort_mode == "oldest":
            return list(reversed(rows))
        elif sort_mode == "atoz":
            return sorted(rows, key=lambda t: t[1].lower())
        return rows

    @staticmethod
    def load_items(trip_id):
        """Returns list of (item_text, checked) for the given trip."""
        conn   = Database._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT item, checked FROM trip_items WHERE trip_id = ?",
                           (trip_id,))
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def delete_trip(trip_id):
        """Deletes a trip and all its items."""
        conn   = Database._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM trip_items WHERE trip_id = ?", (trip_id,))
            cursor.execute("DELETE FROM trips    WHERE id = ?",        (trip_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def fetch_weather(city):
        """Calls OpenWeatherMap API using secure Streamlit secrets."""
        try:
            api_key = st.secrets["WEATHER_API_KEY"]
            url  = (f"https://api.openweathermap.org/data/2.5/weather"
                    f"?q={city}&appid={api_key}&units=metric")
            data = requests.get(url, timeout=5).json()
            if data.get("cod") == 200:
                temp      = data["main"]["temp"]
                feels     = data["main"]["feels_like"]
                condition = data["weather"][0]["description"].title()
                humidity  = data["main"]["humidity"]
                return (f"🌡  {temp}°C  (feels {feels}°C)  |  "
                        f"💧  {humidity}% humidity  |  "
                        f"☁  {condition}")
            return "⚠ Weather unavailable"
        except Exception:
            return "⚠ Could not fetch weather"

    @staticmethod
    def fetch_tripadvisor(city):
        """Calls SerpApi TripAdvisor Search API using secure Streamlit secrets."""
        try:
            api_key = st.secrets["SERPAPI_API_KEY"]
            url = (f"https://serpapi.com/search.json"
                   f"?engine=tripadvisor&q={city}&api_key={api_key}")
            data = requests.get(url, timeout=5).json()
            return data.get("locations", [])
        except Exception:
            pass
        return []
