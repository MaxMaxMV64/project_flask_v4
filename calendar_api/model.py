from datetime import date
import sqlite3


class Event:
    def __init__(self, id=None, event_date=None, title="", text=""):
        self.id = id
        self.event_date = event_date
        self.title = title[:30]
        self.text = text[:200]

    @staticmethod
    def validate(event_date):
        """Проверяет, существует ли событие на указанную дату."""
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE event_date=?", (event_date,))
        result = cursor.fetchone()
        conn.close()
        return bool(result)

    @classmethod
    def create(cls, event_date, title, text):
        if cls.validate(event_date):
            raise ValueError(f"Событие на {event_date} уже существует.")
        
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (event_date, title, text) VALUES (?, ?, ?)",
            (event_date, title, text)
        )
        conn.commit()
        conn.close()
    
    @classmethod
    def get_all_events(cls):
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def get_event_by_id(cls, id):
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE id=?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        else:
            return None

    @classmethod
    def update_event(cls, id, new_title, new_text):
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE events SET title=?, text=? WHERE id=?",
            (new_title, new_text, id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete_event(cls, id):
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id=?", (id,))
        conn.commit()
        conn.close()