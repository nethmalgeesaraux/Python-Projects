import json
import os

NOTES_FILE = "notes.json"


def load_notes():
    """Load notes from file."""
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_notes(notes):
    """Save notes to file."""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)


def add_note():
    title = input("Enter note title: ").strip()
    content = input("Enter note content: ").strip()
    notes = load_notes()
    notes.append({"title": title, "content": content})
    save_notes(notes)
    print(f" Note '{title}' added successfully!")


def view_notes():
    notes = load_notes()
    if not notes:
        print("No notes found.")
        return
    print("\n📝 All Notes:")
    for i, note in enumerate(notes, start=1):
        print(f"{i}. {note['title']}")
    print()


def read_note():
    notes = load_notes()
    if not notes:
        print("No notes to read.")
        return
    title = input("Enter the note title to read: ").strip()
    for note in notes:
        if note["title"].lower() == title.lower():
            print(f"\nTitle: {note['title']}")
            print(f"Content:\n{note['content']}\n")
            return
    print(" Note not found.")


def search_notes():
    keyword = input("Enter keyword to search: ").lower()
    notes = load_notes()
    found = [note for note in notes if keyword in note["title"].lower() or keyword in note["content"].lower()]
    if not found:
        print("No matching notes found.")
        return
    print("\n🔍 Search Results:")
    for note in found:
        print(f"- {note['title']}")
    print()


def delete_note():
    notes = load_notes()
    if not notes:
        print("No notes to delete.")
        return
    title = input("Enter the title of the note to delete: ").strip()
    new_notes = [note for note in notes if note["title"].lower() != title.lower()]
    if len(new_notes) == len(notes):
        print(" Note not found.")
        return
    save_notes(new_notes)
    print(f"🗑️ Note '{title}' deleted successfully!")


def update_note():
    notes = load_notes()
    if not notes:
        print("No notes to update.")
        return
    title = input("Enter the title of the note to update: ").strip()
    for note in notes:
        if note["title"].lower() == title.lower():
            print(f"Current content:\n{note['content']}")
            new_content = input("Enter new content: ").strip()
            note["content"] = new_content
            save_notes(notes)
            print(f"✅ Note '{title}' updated successfully!")
            return
    print(" Note not found.")




if __name__ == "__main__":
    main_menu()
