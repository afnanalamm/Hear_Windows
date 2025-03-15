from customtkinter import CTkLabel

class NotificationBadge(CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(text="0", text_color="red")  # Default badge text and color

    def update_badge(self, unread_count):
        """Update the badge with the number of unread notifications."""
        self.configure(text=str(unread_count))
