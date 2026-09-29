import sqlite3
from metadata import extract_metadata


def save_note(content: str, tags: list[str]) -> str:
    """Save a user's note to the persistent notes database.

    Use this when the user asks you to remember or save information.

    The tags argument must be a list of simple strings.
    Example: ["exam", "SF", "Friday"].
    Do not use dictionaries or objects inside tags.
    """
    metadata=extract_metadata(content)
    connection = sqlite3.connect("notes.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            tags TEXT NOT NULL
        )
    """)

    cursor.execute("PRAGMA table_info(notes)")
    columns = [column[1] for column in cursor.fetchall()]
    if "title" not in columns:
        cursor.execute("ALTER TABLE notes ADD COLUMN title TEXT")

    if "sentiment" not in columns:
        cursor.execute("ALTER TABLE notes ADD COLUMN sentiment TEXT")

    if "key_entities" not in columns:
        cursor.execute("ALTER TABLE notes ADD COLUMN key_entities TEXT")

    cursor.execute(
        """
        INSERT INTO notes (
            content,
            tags,
            title,
            sentiment,
            key_entities
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            content,
            ", ".join(tags),
            metadata.title,
            metadata.sentiment,
            ", ".join(metadata.key_entities)
        )
    )

    connection.commit()
    connection.close()

    return "Note saved successfully."


def search_notes(query: str) -> list:
    """Search the user's previously saved notes.
    Use this when the user asks about information that may have been saved earlier.
    """
    connection = sqlite3.connect("notes.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, content, tags, title, sentiment, key_entities
        FROM notes
        WHERE content LIKE ?
        """,
        (f"%{query}%",)
    )

    results = cursor.fetchall()

    connection.close()


    return results