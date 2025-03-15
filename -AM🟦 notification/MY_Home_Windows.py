import tkinter as tk
from tkinter import messagebox, filedialog
from customtkinter import CTk, CTkTabview, CTkFrame, CTkLabel, CTkButton, CTkTextbox, CTkComboBox, CTkScrollableFrame
from PIL import Image, ImageTk
import pandas as pd
from pathlib import Path
import threading
import time

# Constants
DATA_DIR = Path("data")
POSTS_FILE = DATA_DIR / "posts.csv"
REACTIONS_FILE = DATA_DIR / "reactions.csv"
NOTIFICATIONS_FILE = DATA_DIR / "notifications.csv"
DEFAULT_IMAGE = "default_image.jpg"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TAB_NAMES = ["Trends", "New", "Responses", "Solutions", "You", "Notifications"]

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Load or initialize dataframes
def load_or_initialize_csv(filepath, columns):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        return pd.DataFrame(columns=columns)

posts_df = load_or_initialize_csv(POSTS_FILE, [
    'post_id', 'user_id', 'title', 'content', 'subdistrict', 'city', 'country', 'tags', 'created_at', 'media_path'
])

reactions_df = load_or_initialize_csv(REACTIONS_FILE, [
    'reaction_id', 'user_id', 'post_id', 'comment_id', 'reaction_type', 'created_at'
])

notifications_df = load_or_initialize_csv(NOTIFICATIONS_FILE, [
    'notification_id', 'user_id', 'message', 'created_at', 'is_read'
])

# Save data to CSV files
def save_data():
    posts_df.to_csv(POSTS_FILE, index=False)
    reactions_df.to_csv(REACTIONS_FILE, index=False)
    notifications_df.to_csv(NOTIFICATIONS_FILE, index=False)

class NotificationManager:
    @staticmethod
    def add_notification(post_id=None, reaction_type='like'):
        global reactions_df, notifications_df
        user_id = 1  # Replace with the ID of the user reacting to the post

        # Existing logic to update reactions
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
            
            # Add a notification for the post owner
            post_owner_id = posts_df.loc[posts_df['post_id'] == post_id, 'user_id'].values[0]
            notification_message = f"User {user_id} {reaction_type}d your post."
            new_notification = {
                'notification_id': len(notifications_df) + 1,
                'user_id': post_owner_id,
                'message': notification_message,
                'created_at': pd.Timestamp.now(),
                'is_read': False
            }
            notifications_df = pd.concat([notifications_df, pd.DataFrame([new_notification])], ignore_index=True)
            save_data()
            # update_reaction_display(post_id)

        save_data()
        # update_reaction_display(post_id)

# Display Notifications in the App
class NotificationLoader:
    def __init__(self, notifications_frame):
        self.notifications_frame = notifications_frame

    def load_notifications(self, current_user_id=1):
        for widget in self.notifications_frame.winfo_children():
            widget.destroy()
        
        user_notifications = notifications_df[notifications_df['user_id'] == current_user_id]
        for _, notification in user_notifications.iterrows():
            notification_label = CTkLabel(
                master=self.notifications_frame,
                text=f"{notification['message']} ({notification['created_at']})",
                text_color="gray" if notification['is_read'] else "black"
            )
            notification_label.pack(anchor="w", padx=5, pady=5)

    def mark_as_read(self, notification_id):
        global notifications_df
        notifications_df.loc[notifications_df['notification_id'] == notification_id, 'is_read'] = True
        save_data()
        self.load_notifications()

# Main Application Class
class SocialApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("Social Platform")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(padx=5, pady=5)

        # Tab View
        self.tab_view = CTkTabview(master=self)
        self.tab_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add Tabs
        for tab_name in TAB_NAMES:
            self.tab_view.add(tab_name)

        # Initialize Tabs
        self.trends_tab = TrendsTab(self.tab_view.tab("Trends"))
        self.new_post_tab = NewPostTab(self.tab_view.tab("New"))
        self.notifications_tab = NotificationsTab(self.tab_view.tab("Notifications"))

        # Start notification polling thread
        self.start_notification_polling()

    def start_notification_polling(self):
        def poll_notifications():
            while True:
                time.sleep(10)
                self.notifications_tab.load_notifications()

        threading.Thread(target=poll_notifications, daemon=True).start()

# Trends Tab
class TrendsTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = CTkScrollableFrame(parent)
        self.frame.pack(fill="both", expand=True)
        self.load_posts()

    def load_posts(self):
        for _, post in posts_df.iterrows():
            self.add_post(post)

    def add_post(self, post):
        post_frame = CTkFrame(self.frame)
        post_frame.pack(fill="x", pady=5)

        # Post Title
        CTkLabel(post_frame, text=post['title'], font=("Arial", 14, "bold")).pack(anchor="w")

        # Post Content
        CTkLabel(post_frame, text=post['content'], wraplength=500).pack(anchor="w")

        # Location
        CTkLabel(post_frame, text=f"{post['subdistrict']}, {post['city']}, {post['country']}", text_color="gray").pack(anchor="w")

        # Reactions
        reaction_frame = CTkFrame(post_frame)
        reaction_frame.pack(anchor="e")

        likes = len(reactions_df[(reactions_df['post_id'] == post['post_id']) & (reactions_df['reaction_type'] == 'like')])
        dislikes = len(reactions_df[(reactions_df['post_id'] == post['post_id']) & (reactions_df['reaction_type'] == 'dislike')])

        CTkLabel(reaction_frame, text=f"👍 {likes} 👎 {dislikes}").pack(side="left", padx=5)
        CTkButton(reaction_frame, text="Agree", width=80, command=lambda pid=post['post_id']: self.add_reaction(pid, 'like')).pack(side="left", padx=5)
        CTkButton(reaction_frame, text="Disagree", width=80, command=lambda pid=post['post_id']: self.add_reaction(pid, 'dislike')).pack(side="left", padx=5)

    def add_reaction(self, post_id, reaction_type):
        user_id = 1  # Replace with logged-in user ID
        existing = reactions_df[(reactions_df['user_id'] == user_id) & (reactions_df['post_id'] == post_id)]

        if not existing.empty:
            reactions_df.drop(existing.index, inplace=True)

        if existing.empty or existing.iloc[0]['reaction_type'] != reaction_type:
            new_reaction = {
                'reaction_id': len(reactions_df) + 1,
                'user_id': user_id,
                'post_id': post_id,
                'comment_id': None,
                'reaction_type': reaction_type,
                'created_at': pd.Timestamp.now()
            }
            reactions_df.loc[len(reactions_df)] = new_reaction

            # Notify post owner
            post_owner_id = posts_df.loc[posts_df['post_id'] == post_id, 'user_id'].values[0]
            notification_message = f"User {user_id} {reaction_type}d your post."
            new_notification = {
                'notification_id': len(notifications_df) + 1,
                'user_id': post_owner_id,
                'message': notification_message,
                'created_at': pd.Timestamp.now(),
                'is_read': False
            }
            notifications_df.loc[len(notifications_df)] = new_notification

        save_data()
        self.load_posts()

# New Post Tab
class NewPostTab:
    def __init__(self, parent):
        self.parent = parent
        self.filepath = None
        self.setup_ui()

    def setup_ui(self):
        # Image Preview
        self.preview_canvas = tk.Canvas(self.parent, width=200, height=200)
        self.preview_canvas.pack(pady=10)
        self.preview_canvas.create_text(100, 100, text="Upload an Image", fill="gray")

        # Upload Button
        CTkButton(self.parent, text="Upload Image", command=self.upload_image).pack(pady=5)

        # Post Title
        self.title_entry = CTkTextbox(self.parent, height=30, width=400)
        self.title_entry.pack(pady=5)

        # Post Description
        self.description_textbox = CTkTextbox(self.parent, height=100, width=400)
        self.description_textbox.pack(pady=5)

        # Location Dropdown
        self.location_dropdown = CTkComboBox(self.parent, values=["Location 1", "Location 2", "Location 3"])
        self.location_dropdown.pack(pady=5)

        # Submit Button
        CTkButton(self.parent, text="Create Post", command=self.create_post).pack(pady=10)

    def upload_image(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
        if self.filepath:
            image = Image.open(self.filepath).resize((200, 200), Image.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(image)
            self.preview_canvas.create_image(0, 0, anchor="nw", image=self.preview_image)

    def create_post(self):
        new_post = {
            'post_id': len(posts_df) + 1,
            'user_id': 1,  # Replace with logged-in user ID
            'title': self.title_entry.get("1.0", "end-1c"),
            'content': self.description_textbox.get("1.0", "end-1c"),
            'subdistrict': self.location_dropdown.get(),
            'city': "London",
            'country': "UK",
            'tags': "test",
            'created_at': pd.Timestamp.now(),
            'media_path': self.filepath
        }
        posts_df.loc[len(posts_df)] = new_post
        save_data()
        messagebox.showinfo("Success", "Post created successfully!")
        self.clear_fields()

    def clear_fields(self):
        self.title_entry.delete("1.0", "end")
        self.description_textbox.delete("1.0", "end")
        self.location_dropdown.set("")
        self.preview_canvas.delete("all")
        self.preview_canvas.create_text(100, 100, text="Upload an Image", fill="gray")

# Notifications Tab
class NotificationsTab:
    def __init__(self, parent):
        self.parent = parent
        self.notifications_frame = CTkScrollableFrame(parent)
        self.notifications_frame.pack(fill="both", expand=True)
        self.load_notifications()

    def load_notifications(self):
        for widget in self.notifications_frame.winfo_children():
            widget.destroy()

        user_notifications = notifications_df[notifications_df['user_id'] == 1]  # Replace with logged-in user ID
        for _, notification in user_notifications.iterrows():
            CTkLabel(self.notifications_frame, text=f"{notification['message']} ({notification['created_at']})",
                    text_color="gray" if notification['is_read'] else "black").pack(anchor="w", padx=5, pady=5)

# Run the Application
if __name__ == "__main__":
    app = SocialApp()
    app.mainloop()