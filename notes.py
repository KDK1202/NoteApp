import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# Create notes folder if it doesn't exist
if not os.path.exists("notes"):
    os.mkdir("notes")

# --- Functions ---
def save_note():
    content = text_area.get("1.0", tk.END).strip()
    if content == "":
        messagebox.showwarning("Warning", "Cannot save empty note!")
        return
    title = simpledialog.askstring("Note Title", "Enter a title for your note:")
    if title:
        filename = f"notes/{title}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Saved", f"Note '{title}' saved successfully!")
        text_area.delete("1.0", tk.END)

def list_notes():
    files = os.listdir("notes")
    if not files:
        messagebox.showinfo("Info", "No saved notes found!")
        return

    def open_note(filename):
        with open(f"notes/{filename}", "r", encoding="utf-8") as f:
            content = f.read()
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, content)

    popup_note_selector("Select Note to Open", files, open_note)


def search_notes():
    keyword = simpledialog.askstring("Search Notes", "Enter keyword to search in notes:")
    if not keyword:
        return
    files = os.listdir("notes")
    matching_files = []
    for file in files:
        with open(f"notes/{file}", "r", encoding="utf-8") as f:
            content = f.read()
            if keyword.lower() in content.lower():
                matching_files.append(file)
    if not matching_files:
        messagebox.showinfo("No Results", f"No notes found containing '{keyword}'.")
        return

    def open_note(filename):
        with open(f"notes/{filename}", "r", encoding="utf-8") as file:
            content = file.read()
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, content)

    popup_note_selector("Select Note to Open", matching_files, open_note)


def delete_note():
    files = os.listdir("notes")
    if not files:
        messagebox.showinfo("Info", "No saved notes to delete!")
        return
    notes_str = "\n".join([f"{i+1}. {file}" for i, file in enumerate(files)])
    selected = simpledialog.askinteger("Delete Note", f"Saved notes:\n{notes_str}\n\nEnter note number to delete:")
    if selected:
        if 1 <= selected <= len(files):
            filename = f"notes/{files[selected-1]}"
            os.remove(filename)
            messagebox.showinfo("Deleted", f"Note '{files[selected-1]}' deleted successfully!")
        else:
            messagebox.showerror("Error", "Invalid selection.")

def rename_note():
    files = os.listdir("notes")
    if not files:
        messagebox.showinfo("Info", "No saved notes to rename!")
        return

    def rename_selected(filename):
        new_name = simpledialog.askstring("New Title", "Enter the new title for this note:")
        if new_name:
            new_filename = f"notes/{new_name}.txt"
            os.rename(f"notes/{filename}", new_filename)
            messagebox.showinfo("Renamed", f"Note renamed to '{new_name}' successfully!")

    popup_note_selector("Select Note to Rename", files, rename_selected)


def popup_note_selector(title, file_list, action):
    """
    title: string to display at top
    file_list: list of filenames to choose from
    action: function to call with selected filename
    """
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("300x300")

    label = tk.Label(popup, text="Select a note:")
    label.pack(pady=5)

    listbox = tk.Listbox(popup)
    for file in file_list:
        listbox.insert(tk.END, file)
    listbox.pack(pady=5, fill="both", expand=True)

    def on_select():
        selected_index = listbox.curselection()
        if selected_index:
            filename = file_list[selected_index[0]]
            action(filename)
            popup.destroy()
        else:
            messagebox.showerror("Error", "Please select a note.")

    select_button = tk.Button(popup, text="Select", command=on_select)
    select_button.pack(pady=5)

# --- Window Setup ---
root = tk.Tk()
root.title("Note Taking App")
root.geometry("500x400")

# --- Text Area ---
text_area = tk.Text(root, font=("Arial", 12))
text_area.pack(padx=10, pady=10, expand=True, fill="both")

# --- Buttons ---
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

save_button = tk.Button(button_frame, text="Save Note", command=save_note, width=15)
save_button.pack(side="left", padx=5)

list_button = tk.Button(button_frame, text="List Notes", command=list_notes, width=15)
list_button.pack(side="left", padx=5)

search_button = tk.Button(button_frame, text="Search Notes", command=search_notes, width=15)
search_button.pack(side="left", padx=5)

delete_button = tk.Button(button_frame, text="Delete Note", command=delete_note, width=15)
delete_button.pack(side="left", padx=5)

rename_button = tk.Button(button_frame, text="Rename Note", command=rename_note, width=15)
rename_button.pack(side="left", padx=5)

# --- Run App ---
root.mainloop()
