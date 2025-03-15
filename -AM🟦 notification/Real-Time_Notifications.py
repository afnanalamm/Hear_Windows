#Add a Polling Mechanism - this periodically checks for new notifications and updates the UI
import threading
import time

class RealTimeNotifications:
    def __init__(self, notifications_df, current_user_id, update_notification_badge, load_notifications):
        self.notifications_df = notifications_df
        self.current_user_id = current_user_id
        self.update_notification_badge = update_notification_badge
        self.load_notifications = load_notifications
        self.running = True

    def start_polling(self):
        def poll():
            while self.running:
                time.sleep(10)  # Check for new notifications every 10 seconds
                unread_count = len(self.notifications_df[
                    (self.notifications_df['user_id'] == self.current_user_id) & 
                    (self.notifications_df['is_read'] == False)
                ])
                if unread_count > 0:
                    self.update_notification_badge()
                    self.load_notifications()

        self.thread = threading.Thread(target=poll)
        self.thread.daemon = True
        self.thread.start()

    def stop_polling(self):
        self.running = False
