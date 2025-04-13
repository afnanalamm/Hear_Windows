from tkinter import *
from tkinter import messagebox
from customtkinter import *
from PIL import ImageTk, Image
import pandas as pd
from pathlib import Path
from tkinter import *
from tkinter import ttk
from customtkinter import *
from MAIN_WINDOW_CONSTANTS import *
from FUNCTIONS import *
from PIL import ImageTk, Image



# ======================== CONSTANTS ========================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DATA_DIR = Path("data")
POSTS_FILE = DATA_DIR / "test_posts.csv"
REACTIONS_FILE = DATA_DIR / "test_reactions.csv"
DEFAULT_IMAGE = "HERE_WINDOW_ICON.jpg"  # Create this image or modify path

# ======================== DATA SETUP ========================
DATA_DIR.mkdir(exist_ok=True)

try:
    posts_df = pd.read_csv(POSTS_FILE)
except FileNotFoundError:
    posts_df = pd.DataFrame(columns=[
        'post_id', 'user_id', 'title', 'content', 'subdistrict',
        'city', 'country', 'tags', 'created_at', 'media_path'
    ])

try:
    reactions_df = pd.read_csv(REACTIONS_FILE)
except FileNotFoundError:
    reactions_df = pd.DataFrame(columns=[
        'reaction_id', 'user_id', 'post_id', 'comment_id',
        'reaction_type', 'created_at'
    ])

def save_data():
    posts_df.to_csv(POSTS_FILE, index=False)
    reactions_df.to_csv(REACTIONS_FILE, index=False)

# ======================== CORE FUNCTIONS ========================


def stat_adder(post_id=None, reaction_type='like'):
    global reactions_df
    user_id = 1  # Replace with actual user ID
    
    existing = reactions_df[
        (reactions_df['user_id'] == user_id) & 
        (reactions_df['post_id'] == post_id) 
    ]
    
    if not existing.empty:
        reactions_df = reactions_df.drop(existing.index)
    
    if existing.empty or existing.iloc[0]['reaction_type'] != reaction_type:
        new_reaction = {
            'reaction_id': len(reactions_df) + 1,
            'user_id': user_id,
            'post_id': post_id,
            'comment_id': None,
            'reaction_type': reaction_type,
            'created_at': pd.Timestamp.now()
        }
        reactions_df = pd.concat([reactions_df, pd.DataFrame([new_reaction])], ignore_index=True)
    
    save_data()
    update_reaction_display(post_id)

def update_reaction_display(post_id=None):
    for widget in comments_section_frame.winfo_children():
        if hasattr(widget, 'post_id') and (post_id is None or widget.post_id == post_id):
            likes = len(reactions_df[(reactions_df['post_id'] == widget.post_id) & 
                                   (reactions_df['reaction_type'] == 'like')])
            dislikes = len(reactions_df[(reactions_df['post_id'] == widget.post_id) & 
                                      (reactions_df['reaction_type'] == 'dislike')])
            widget.reaction_label.configure(text=f"👍 {likes} 👎 {dislikes}")

# ======================== POST MANAGEMENT ========================
def create_post(file):
    global posts_df
    new_post = {
        'post_id': len(posts_df) + 1,
        'user_id': 1,
        'title': post_title_entry.get(),
        'content': description_textbox.get("1.0", END).strip(),
        'subdistrict': location_dropdown.get(),
        'city': "London",
        'country': "UK",
        'tags': "test",
        'created_at': pd.Timestamp.now(),
        'media_path': filepath_from_upload_button
    }
    
    posts_df = pd.concat([posts_df, pd.DataFrame([new_post])], ignore_index=True)
    save_data()
    add_post_to_ui(new_post)
    clear_post_fields()
    messagebox.showinfo("Success", "Post created successfully!")

def clear_post_fields():
    post_title_entry.delete(0, END)
    description_textbox.delete("1.0", END)
    location_dropdown.set("")

def add_post_to_ui(post):
    post_frame = CTkFrame(master=comments_section_frame)
    post_frame.pack(fill="x", pady=5)
    post_frame.post_id = post['post_id']
    
    # Post content
    CTkLabel(post_frame, text=post['title'], font=("Arial", 14, "bold")).pack(anchor="w")
    CTkLabel(post_frame, text=post['content'], wraplength=500).pack(anchor="w")
    CTkLabel(post_frame, 
            text=f"{post['subdistrict']}, {post['city']}, {post['country']}",
            text_color="gray").pack(anchor="w")
    
    # Reactions
    reaction_frame = CTkFrame(post_frame)
    reaction_frame.pack(anchor="e")
    
    likes = len(reactions_df[(reactions_df['post_id'] == post['post_id']) & 
                           (reactions_df['reaction_type'] == 'like')])
    dislikes = len(reactions_df[(reactions_df['post_id'] == post['post_id']) & 
                              (reactions_df['reaction_type'] == 'dislike')])
    
    reaction_label = CTkLabel(reaction_frame, text=f"👍 {likes} 👎 {dislikes}")
    reaction_label.pack(side="left", padx=5)
    
    CTkButton(reaction_frame, text="Agree", width=80,
             command=lambda pid=post['post_id']: stat_adder(pid, 'like')).pack(side="left", padx=5)
    CTkButton(reaction_frame, text="Disagree", width=80,
             command=lambda pid=post['post_id']: stat_adder(pid, 'dislike')).pack(side="left", padx=5)
    
    post_frame.reaction_label = reaction_label

# ======================== GUI SETUP ========================
home_window = CTk()
home_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
home_window.title("Social Media App")

# Tab System
tab_view = CTkTabview(master=home_window)
tab_view.pack(fill="both", expand=True, padx=10, pady=10)
tab_view.add("Trends")
tab_view.add("New Post")

# Trends Tab
comments_section_frame = CTkScrollableFrame(tab_view.tab("Trends"))
comments_section_frame.pack(fill="both", expand=True)


# New Post Tab
post_creation_frame = CTkFrame(tab_view.tab("New Post"))
post_creation_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Post Title
CTkLabel(post_creation_frame, text="Post Title:").pack(anchor="w")
post_title_entry = CTkEntry(post_creation_frame, width=400)
post_title_entry.pack(fill="x", pady=5)

# Location
CTkLabel(post_creation_frame, text="Location:").pack(anchor="w")
location_dropdown = CTkComboBox(post_creation_frame, 
                               values=["Downtown", "Suburb", "Rural"])
location_dropdown.pack(fill="x", pady=5)

# Description
CTkLabel(post_creation_frame, text="Description:").pack(anchor="w")
description_textbox = CTkTextbox(post_creation_frame, height=150)
description_textbox.pack(fill="x", pady=5)

# Post Button
CTkButton(post_creation_frame, text="Create Post", command=create_post).pack(pady=10)

# Load existing posts
for _, post in posts_df.iterrows():
    add_post_to_ui(post)

class ResponsePopup():    #Copilot generated this class, but I have modified it to suit my needs
    def __init__(self):
        self.window = CTkToplevel()
        self.window.title("Response")
        self.window.geometry("600x300")
        # self.set_default_color_theme("green")  # Removed as it's not a valid method
        # self.window.protocol("WM_DELETE_WINDOW", self.close)

        # Create a label and button in the popup window
        self.label = CTkLabel(self.window, text="Please enter your response as to why\nyou've accepted/rejected the petition")
        self.label.pack(pady=20)

        self.reply_textbox = CTkTextbox(master= self.window, height = 300, width = 200, corner_radius = 10,
                                        fg_color= "#2d54d1")
        self.reply_textbox.pack(pady=20)

        # Create a reply button
        self.reply_button = CTkButton(self.window, text="Reply", command=self.close)
        self.reply_button.pack(pady=0)

        # Create a close button
        self.close_button = CTkButton(self.window, text="Close", command=self.close)
        self.close_button.pack(pady=0)

    def reply(self):
        pass

    def close(self):
        self.window.destroy()

my_button = CTkButton(tab_view.tab('Trends'), text="Send Response", command=ResponsePopup)
my_button.pack(pady=10)

home_window.mainloop()