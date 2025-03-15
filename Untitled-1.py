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
from NEW_POST_TAB_CONSTANTS import *
from PIL import ImageTk, Image

# ======================== CONSTANTS ========================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DATA_DIR = Path("data")
POSTS_FILE = DATA_DIR / "posts.csv"
REACTIONS_FILE = DATA_DIR / "reactions.csv"
DEFAULT_IMAGE = "default_image.jpg"  # Create this image or modify path

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


for idx, comment in enumerate(example_comments):
    comment_frame = CTkFrame(
        master=comments_section_frame,
        fg_color=COMMENT_FRAME_BACKGROUND,
        corner_radius=COMMENT_FRAME_CORNER_RADIUS
    )
    comment_frame.pack(fill="x", pady=COMMENT_FRAME_PADY)

    user_label = CTkLabel(
        master=comment_frame,
        text=comment["user"],
        font=COMMENT_USER_FONT,
        text_color=COMMENT_USER_TEXT_COLOR
    )
    user_label.pack(anchor="w", padx=COMMENT_PADX)

    comment_label = CTkLabel(
        master=comment_frame,
        text=comment["comment"],
        font=COMMENT_TEXT_FONT,
        text_color=COMMENT_TEXT_COLOR,
        wraplength=COMMENTS_SECTION_FRAME_WIDTH - 40
    )
    comment_label.pack(anchor="w", padx=COMMENT_PADX)

    # Reaction buttons frame
    reaction_frame = CTkFrame(comment_frame, fg_color="transparent")
    reaction_frame.pack(anchor="e", padx=5, pady=5)

    # Thumbs up button
    thumbs_up_button_i = 'thumbs_up_button' + str(idx)
    thumbs_down_button_i = 'thumbs_up_button' + str(idx)

    thumbs_up_button_i = CTkButton(
        master=reaction_frame,
        text="👍 0",
        width=COMMENT_REACTION_BUTTON_WIDTH,
        height=COMMENT_REACTION_BUTTON_HEIGHT,
        font=COMMENT_REACTION_BUTTON_FONT,
        fg_color=COMMENT_REACTION_BUTTON_BG,
        hover_color=COMMENT_REACTION_BUTTON_HOVER_COLOR,
        bg_color=COMMENT_REACTION_BUTTON_BG,
        command=lambda: update_reaction(thumbs_up_button_i)
    )
    thumbs_up_button_i.pack(side="left", padx=COMMENT_REACTION_BUTTON_SPACING)

    # Thumbs down button
    thumbs_down_button_i = CTkButton(
        master=reaction_frame,
        text="👎 0",
        width=COMMENT_REACTION_BUTTON_WIDTH,
        height=COMMENT_REACTION_BUTTON_HEIGHT,
        font=COMMENT_REACTION_BUTTON_FONT,
        fg_color=COMMENT_REACTION_BUTTON_BG,
        hover_color=COMMENT_REACTION_BUTTON_HOVER_COLOR,
        bg_color=COMMENT_REACTION_BUTTON_BG,
        command=lambda: update_reaction(thumbs_down_button_i)
    )
    thumbs_down_button_i.pack(side="left", padx=COMMENT_REACTION_BUTTON_SPACING)



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

home_window.mainloop()