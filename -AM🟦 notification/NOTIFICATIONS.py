notifications_df = pd.DataFrame(columns=[
    'notification_id',  # Unique ID for each notification
    'user_id',          # ID of the user who should receive the notification
    'message',          # The notification message (e.g., "User X liked your post")
    'created_at',       # Timestamp of the notification
    'is_read'           # Whether the notification has been read (True/False)
])



#Add Notification Logic to Key Events
def stat_adder(post_id=None, reaction_type='like'):
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
    update_reaction_display(post_id)

save_data()
update_reaction_display(post_id)



#Save Notifications to a CSV File
def save_data():
    posts_df.to_csv(POSTS_FILE, index=False)
    reactions_df.to_csv(REACTIONS_FILE, index=False)
    notifications_df.to_csv(NOTIFICATIONS_FILE, index=False)  # Save notifications

#define NOTIFICATIONS_FILE
NOTIFICATIONS_FILE = DATA_DIR / "notifications.csv"



#Load Notifications When the App Starts
try:
    notifications_df = pd.read_csv(NOTIFICATIONS_FILE)
except FileNotFoundError:
    notifications_df = pd.DataFrame(columns=[
        'notification_id', 'user_id', 'message', 'created_at', 'is_read'
    ])


#Display Notifications in the App

#Add a Notifications Tab

#Display Notifications in the Tab

def load_notifications():
    for widget in notifications_frame.winfo_children():
        widget.destroy()  # Clear existing notifications
    
    user_notifications = notifications_df[notifications_df['user_id'] == current_user_id]  # Replace with the logged-in user's ID
    for _, notification in user_notifications.iterrows():
        notification_label = CTkLabel(
            master=notifications_frame,
            text=f"{notification['message']} ({notification['created_at']})",
            text_color="gray" if notification['is_read'] else "black"
        )
        notification_label.pack(anchor="w", padx=5, pady=5)



#Mark notifications as read
def mark_as_read(notification_id):
    global notifications_df
    notifications_df.loc[notifications_df['notification_id'] == notification_id, 'is_read'] = True
    save_data()
    load_notifications()  # Refresh the notifications display



