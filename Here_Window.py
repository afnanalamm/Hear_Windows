from tkinter import *
from tkinter import ttk, PhotoImage, messagebox, filedialog, simpledialog
from customtkinter import *
from customtkinter import CTkImage
from PIL import Image as PilImage, ImageTk
import pandas as pd
from pathlib import Path
# import os, sys, random, time, datetime, subprocess
from LOGIN_WINDOW_CONSTANTS import *
from HERE_WINDOW_CONSTANTS import *

# Initialize data structures at the start
DATA_DIR = Path("data")
PETITIONS_FILE = DATA_DIR / "petitions.csv"
REACTIONS_FILE = DATA_DIR / "reactions.csv"
COMMENTS_FILE = DATA_DIR / "comments.csv"
ALL_COMMENTS_FILE = DATA_DIR / "all_comments.csv"
RESPONSE_INFO_FILE = DATA_DIR / "response_info.csv"

# Initialize the current petition index
global current_petition_index
current_petition_index = 0

'''============================= CLASSES ====================================='''
class ResponsePopup():    #Copilot generated this class, but I have modified it to suit my needs
    def __init__(self, title, response = str):
        self.window = CTkToplevel()
        self.window.title("Response")
        self.window.geometry(f"600x350")
        self.window.attributes('-topmost', True)  # Ensure the popup is on top of other windows
        # self.window.focus_force()  # Focus on the popup window

        # Create a label and button in the popup window
        self.reply_notice_label = CTkLabel(self.window, text= f"Please elaborate why you {response} the petition: \n {title}")
        self.reply_notice_label.pack(pady=20)
        self.reply_notice_label.configure(bg_color = 'black', fg_color = '#010101', text_color = 'white', corner_radius = 10)

        self.reply_textbox = CTkTextbox(master= self.window, height = 200, width = 600, corner_radius = 10,
                                        fg_color= "#010110")
        self.reply_textbox.pack(pady=4)

        # Create a reply button
        self.reply_button = CTkButton(master= self.window, text="Reply", command=lambda: self.reply())
        self.reply_button.pack(padx=2, pady=2)

        # Create a close button
        self.cancel_button = CTkButton(master= self.window, text="Cancel", command=self.cancel)
        self.cancel_button.pack(padx=2, pady=2)

    def reply(self):
        choice = messagebox.askyesno("Reply", "Are you sure you want to send this reply?")
        if choice == True:
            print("Reply sent:", self.reply_textbox.get("1.0", "end-1c"))
            self.reply_textbox.delete("1.0", "end")
        else:
            print("Reply cancelled")

    def cancel(self):
        self.window.destroy()

# Constants
DEFAULT_USER = "You"  # Default username for new comments

'''============================= FUNCTIONS ====================================='''

# Helper Functions
def create_reaction_buttons(parent, index=None):
    """Creates and packs reaction buttons (thumbs up/down) into the given parent."""
    reaction_frame = CTkFrame(parent, fg_color="transparent")
    reaction_frame.pack(anchor="e", padx=5, pady=5)

    thumbs_up = CTkButton(
        master=reaction_frame,
        text="👍 0",
        width=COMMENT_REACTION_BUTTON_WIDTH,
        height=COMMENT_REACTION_BUTTON_HEIGHT,
        font=COMMENT_REACTION_BUTTON_FONT,
        fg_color=COMMENT_REACTION_BUTTON_BG,
        hover_color=COMMENT_REACTION_BUTTON_HOVER_COLOR,
        bg_color=COMMENT_REACTION_BUTTON_BG,
    )
    thumbs_up.pack(side="left", padx=COMMENT_REACTION_BUTTON_SPACING)

    thumbs_down = CTkButton(
        master=reaction_frame,
        text="👎 0",
        width=COMMENT_REACTION_BUTTON_WIDTH,
        height=COMMENT_REACTION_BUTTON_HEIGHT,
        font=COMMENT_REACTION_BUTTON_FONT,
        fg_color=COMMENT_REACTION_BUTTON_BG,
        hover_color=COMMENT_REACTION_BUTTON_HOVER_COLOR,
        bg_color=COMMENT_REACTION_BUTTON_BG,
    )
    thumbs_down.pack(side="left", padx=COMMENT_REACTION_BUTTON_SPACING)

    if index is not None:
        thumbs_up.configure(command=lambda idx=index, b=thumbs_up: update_reaction(idx, "👍", b))
        thumbs_down.configure(command=lambda idx=index, b=thumbs_down: update_reaction(idx, "👎", b))


def create_comment_widget(comment, parent, index=None):
    """Creates a comment UI widget in the given parent container."""
    comment_frame = CTkFrame(
        master=parent,
        fg_color=COMMENT_FRAME_BACKGROUND,
        corner_radius=COMMENT_FRAME_CORNER_RADIUS,
    )
    comment_frame.pack(fill="x", pady=COMMENT_FRAME_PADY)

    user_label = CTkLabel(
        master=comment_frame,
        text=comment.get("user", DEFAULT_USER),
        font=COMMENT_USER_FONT,
        text_color=COMMENT_USER_TEXT_COLOR,
    )
    user_label.pack(anchor="w", padx=COMMENT_PADX)

    comment_label = CTkLabel(
        master=comment_frame,
        text=comment.get("comment", ""),
        font=COMMENT_TEXT_FONT,
        text_color=COMMENT_TEXT_COLOR,
        wraplength=COMMENTS_SECTION_FRAME_WIDTH - 40,
    )
    comment_label.pack(anchor="w", padx=COMMENT_PADX)

    create_reaction_buttons(comment_frame, index)




def update_petition_display(petition_index):
    """Updates the main petition display (image, title, content) for the given petition index."""
    home_image = PilImage.open(petitions_df["media_path"][petition_index]).resize(RESIZED_IMAGE_TUPLE, PilImage.LANCZOS)
    home_image = ImageTk.PhotoImage(home_image)
    home_image_label.config(image=home_image)
    home_image_label.image = home_image

    image_info_label.config(text=petitions_df["title"][petition_index])
    # image_title_label.config(text=petitions_df["title"][petition_index])

def load_petition(direction):
    """Loads the next or previous petition based on the direction."""
    global current_petition_index, comments_holder_list

    if direction == "next" and current_petition_index < len(petitions_df) - 1:
        current_petition_index += 1
    elif direction == "previous" and current_petition_index > 0:
        current_petition_index -= 1
    elif direction == "previous" and current_petition_index == 0:
        messagebox.showinfo("Whoa!", "You've reached the first ever petition!")
    else:
        current_petition_index = 0

    update_petition_display(current_petition_index)
    # read_post_comments(petitions_df["petition_id"][current_petition_index])

    for widget in comments_section_frame.winfo_children():
        widget.destroy()

    # Initialize comments_holder_list with comments for the current petition
    comments_holder_list = []  # Replace with actual logic to fetch comments for the current petition

    for idx, comment in enumerate(comments_holder_list):
        create_comment_widget(comment, comments_section_frame, index=idx)

def load_petition_description(index):
    """Loads the description of your petition in a pop-up window."""
    description = petitions_df["content"][index]
    messagebox.showinfo('Post Description', description)

def save_data():
    """Saves petition and reaction data to CSV files."""
    petitions_df.to_csv(PETITIONS_FILE, index=False)
    reactions_df.to_csv(REACTIONS_FILE, index=False)



def initialize_dataframes():
    """Initializes dataframes with error handling."""
    global petitions_df, reactions_df, comments_df, all_comments_df, response_info_df
    try:
        petitions_df = pd.read_csv(PETITIONS_FILE, on_bad_lines='warn') if PETITIONS_FILE.exists() else pd.DataFrame(columns=[
            "petition_id", "user_id", "title", "content", "subdistrict", "city", "country", 
            "tags", "created_at", "media_path", "num_agree", "num_disagree", "status"
        ])
        reactions_df = pd.read_csv(REACTIONS_FILE) if REACTIONS_FILE.exists() else pd.DataFrame(columns=[
            "reaction_id", "user_id", "petition_id", 
            "reaction_type", "created_at"
        ])
        comments_df = pd.read_csv(COMMENTS_FILE) if COMMENTS_FILE.exists() else pd.DataFrame(columns=[
            "petition_id", "user_id", "all_comments_id"
        ])
        all_comments_df = pd.read_csv(ALL_COMMENTS_FILE) if ALL_COMMENTS_FILE.exists() else pd.DataFrame(columns=[
            "all_comments_id", "comment"
        ])
        response_info_df = pd.read_csv(RESPONSE_INFO_FILE) if RESPONSE_INFO_FILE.exists() else pd.DataFrame(columns=[
            "response_info_id", "response_text", "responded_at"
        ])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initialize data: {e}")
        raise
def save_data():
    try:
        petitions_df.to_csv(PETITIONS_FILE, index=False)
        reactions_df.to_csv(REACTIONS_FILE, index=False)
        comments_df.to_csv(COMMENTS_FILE, index=False)
        all_comments_df.to_csv(ALL_COMMENTS_FILE, index=False)
        response_info_df.to_csv(RESPONSE_INFO_FILE, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def respond_petition(response = str):
    """Handles the command from the accept & reject petitions buttons on the council side"""
    global current_petition_index
    try:
        #Get data about the current petition
        petition_title = petitions_df.iloc[current_petition_index]["title"]
        petition_id = petitions_df.iloc[current_petition_index]["petition_id"]
    
        match response:
            case "Accept":
                ResponsePopup(response= "accepted", title= petition_title)
                petitions_df.at[current_petition_index, "status"] = "accepted"
            case "Reject":
                ResponsePopup(response= "rejected", title= petition_title)
                petitions_df.at[current_petition_index, "status"] = "rejected"
        # save_data()
        

    except Exception as e:
        messagebox.showerror("Error!", f"Failed to respond to petition: /n {e}")
        raise
    finally:
        save_data()



def update_reaction(comment_id, reaction_type, button):
    """Updates the reaction count for a comment."""
    global reactions_df
    try:
        new_reaction = {
            "reaction_id": len(reactions_df) + 1,
            "user_id": 1,
            "petition_id": None,
            "comment_id": comment_id,
            "reaction_type": reaction_type,
            "created_at": pd.Timestamp.now(),
        }
        reactions_df = pd.concat([reactions_df, pd.DataFrame([new_reaction])], ignore_index=True)

        count = len(reactions_df[(reactions_df["comment_id"] == comment_id) & (reactions_df["reaction_type"] == reaction_type)])
        button.configure(text=f"{reaction_type} {count}")

        notifications.insert(0, {"text": f"❤️ Someone reacted {reaction_type} to your comment", "time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")})
        # update_notifications()
        save_data()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update reaction: {e}")

def update_stat(stat_type):
    """Updates agree/disagree counts and saves them to a file."""
    try:
        if len(petitions_df) == 0:
            messagebox.showwarning("Warning", "No petitions available")
            return

        agree_count = petitions_df.at[current_petition_index, "num_agree"]
        disagree_count = petitions_df.at[current_petition_index, "num_disagree"]

        if stat_type == "agree":
            agree_count += 1
            petitions_df.at[current_petition_index, "num_agree"] = agree_count
        elif stat_type == "disagree":
            disagree_count += 1
            petitions_df.at[current_petition_index, "num_disagree"] = disagree_count
        save_data()
        agree_stat.configure(text=f"Agree: {agree_count}")
        disagree_stat.configure(text=f"Disagree: {disagree_count}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update stats: {e}")
    # with open("LikeDislikeStats.txt", "w") as stats_file:
    #     stats_file.write(f"{agree_count}\n{disagree_count}")



def load_image(path, size):
    """Loads and resizes an image."""
    try:
        image = PilImage.open(path).resize(size, PilImage.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
        return None


def save_data():
    try:
        petitions_df.to_csv(PETITIONS_FILE, index=False)
        reactions_df.to_csv(REACTIONS_FILE, index=False)
        comments_df.to_csv(COMMENTS_FILE, index=False)
        all_comments_df.to_csv(ALL_COMMENTS_FILE, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")


def open_file(canvas):
    try:
        global filepath
        filepath = filedialog.askopenfilename(
            title='Select File',
            filetypes=(
                ('Image files', "*.jpg;*.png;*.gif"),
                ('All files', "*.*")
            )
        )
        if filepath:
            image = PilImage.open(filepath).resize(PICTURE_PREVIEW_IMAGE_SIZE, PilImage.LANCZOS)
            image = ImageTk.PhotoImage(image)
            canvas.image = image
            canvas.delete("all")  # Clear canvas first
            canvas.create_image(0, 0, image=image, anchor=NW)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image: {e}")
        canvas.delete("all")
        canvas.create_text(
            PICTURE_PREVIEW_WIDTH / 2,
            PICTURE_PREVIEW_HEIGHT / 2,
            text="Error loading image"
        )

def create_petition():
    global petitions_df
    global tab_view
    new_petition = {
        'petition_id': len(petitions_df) + 1,
        'user_id': 1,
        'title': petition_title_entry.get(), # type: ignore
        'content': description_textbox.get("1.0", END).strip(), # type: ignore
        'subdistrict': location_dropdown.get(), # type: ignore
        'city': "London",
        'country': "UK",
        'tags': "test",
        'created_at': pd.Timestamp.now(),
        'media_path': filepath,
        'num_agree': 0,
        'num_disagree': 0,
        'status': "pending"
    }
    petitions_df = pd.concat([petitions_df, pd.DataFrame([new_petition])], ignore_index=True)
    save_data()
    messagebox.showinfo("Success!", "Post created successfully!")

def cleanup():
    """Clean up resources before closing"""
    try:
        save_data()
        global home_image
        if 'home_image' in globals():
            del home_image
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clean up: {e}")
    finally:
        main_window.destroy()


'''======================== MAIN WINDOW SETUP ========================'''

# Window setup
main_window = Tk()
main_window.configure(padx=5, pady=5)
main_window.geometry(f"{WINDOW_WIDTH+50}x{WINDOW_HEIGHT}+0+0")
main_window.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
main_window.title(WINDOW_TITLE)
main_window.iconbitmap(WINDOW_ICONBITMAP)

# Add window cleanup handler
main_window.protocol("WM_DELETE_WINDOW", cleanup)

tab_view = CTkTabview(master=main_window)
tab_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
tab_view.grid_rowconfigure(0, weight=1)
main_window.grid_columnconfigure(0, weight=1)

# create tabs
tab_view.add(ALL)
tab_view.add(PENDING)
tab_view.add(APPROVED)
tab_view.add(SUSPENDED)
tab_view.add(SETTINGS)

tab_view.tab(ALL).configure(height=TAB_HEIGHT, width=TAB_WIDTH)  # just resizing all tabs, so that they are all the same size
tab_view.tab(PENDING).configure(height=TAB_HEIGHT, width=TAB_WIDTH)  # needed to resize this one initially, as the image-display frame was being cut off
tab_view.tab(APPROVED).configure(height=TAB_HEIGHT, width=TAB_WIDTH)
tab_view.tab(SUSPENDED).configure(height=TAB_HEIGHT, width=TAB_WIDTH)
tab_view.tab(SETTINGS).configure(height=TAB_HEIGHT, width=TAB_WIDTH)

home_frame = Frame(master=tab_view.tab(ALL), background=FRAME_BACKGROUND, width=FRAME_WIDTH, height=FRAME_HEIGHT)
home_frame.grid_configure(row=0, column=0, sticky=NSEW)

home_image = PilImage.open('MAIN_WINDOW_ICON.jpg').resize(RESIZED_IMAGE_TUPLE, PilImage.LANCZOS)
home_image = ImageTk.PhotoImage(home_image)


home_image_label = Label(
    master=home_frame,
    width=HOME_IMAGE_LABEL_WIDTH,
    height=HOME_IMAGE_LABEL_HEIGHT,
    background=HOME_IMAGE_LABEL_BACKGROUND,
    image=home_image
)
home_image_label.grid(
    row=HOME_IMAGE_LABEL_ROW,
    column=HOME_IMAGE_LABEL_COLUMN,
    rowspan=HOME_IMAGE_LABEL_ROWSPAN,
    columnspan=HOME_IMAGE_LABEL_COLUMNSPAN,
    sticky=HOME_IMAGE_LABEL_STICKY
)

# Reactions Frame Setup
reactions_frame = Frame(
    master=home_frame,
    height=REACTIONS_FRAME_HEIGHT,
    width=REACTIONS_FRAME_WIDTH,
    background=REACTION_FRAME_BACKGROUND
)
reactions_frame.place(
    relx=REACTION_FRAME_RELX,
    rely=REACTION_FRAME_RELY
)

# def update_stat(stat_type, agree, disagree):
#     """Updates agree/disagree counts and saves them to a file."""
#     global agree_count, disagree_count

#     if stat_type == "agree":
#         agree_count = str(int(agree_count) + 1)
#     elif stat_type == "disagree":
#         disagree_count = str(int(disagree_count) + 1)

#     with open("LikeDislikeStats.txt", "w") as stats_file:
#         stats_file.write(f"{agree_count}\n{disagree_count}")

#     agree.configure(text=f"Agree: {agree_count}")
#     disagree.configure(text=f"Disagree: {disagree_count}")

stat_type = StringVar()  # Need this to check the value of the radiobuttons-AG🟨

# Stats labels
agree_stat = CTkLabel(
    master=reactions_frame,  # label for agree stat -AG🟨
    text=AGREE_STAT_TEXT,
    bg_color=AGREE_STAT_BG_COLOR,
    corner_radius=AGREE_STAT_CORNER_RADIUS,
    width=REACTION_BUTTON_WIDTH,
)
agree_stat.grid(
    row=AGREE_STAT_ROW,
    column=AGREE_STAT_COLUMN,
    sticky=AGREE_STAT_STICKY,
    padx=AGREE_STAT_PADX,
    pady=AGREE_STAT_PADY
)

disagree_stat = CTkLabel(
    master=reactions_frame,  # label for disagree stat -AG🟨
    text=DISAGREE_STAT_TEXT,
    bg_color=DISAGREE_STAT_BG_COLOR,
    corner_radius=DISAGREE_STAT_CORNER_RADIUS,
    width=REACTION_BUTTON_WIDTH,
)
disagree_stat.grid(
    row=DISAGREE_STAT_ROW,
    column=DISAGREE_STAT_COLUMN,
    sticky=DISAGREE_STAT_STICKY,
    padx=DISAGREE_STAT_PADX,
    pady=DISAGREE_STAT_PADY
)

accept_button = Radiobutton(
    master=reactions_frame,
    foreground=ACCEPT_BUTTON_BACKGROUND,
    activebackground=ACCEPT_BUTTON_BACKGROUND,
    width=REACTION_BUTTON_WIDTH,
    text=ACCEPT_BUTTON_TEXT,
    variable=stat_type,
    value=0,  # Added variable=stat_type -AG🟨
    command=lambda: respond_petition("Accept")
)
accept_button.grid(
    row=ACCEPT_BUTTON_ROW,
    column=ACCEPT_BUTTON_COLUMN,
    sticky=ACCEPT_BUTTON_STICKY,
    padx=ACCEPT_BUTTON_PADX,
    pady=ACCEPT_BUTTON_PADY
)

reject_button = Radiobutton(
    master=reactions_frame,
    foreground=REJECT_BUTTON_BACKGROUND,
    activebackground=REJECT_BUTTON_BACKGROUND,
    width=REACTION_BUTTON_WIDTH,
    text=REJECT_BUTTON_TEXT,
    variable=stat_type,
    value=1,  # Will not work without variable=stat_type -AG🟨
    command=lambda: respond_petition("Reject")
)
reject_button.grid(
    row=REJECT_BUTTON_ROW,
    column=REJECT_BUTTON_COLUMN,
    sticky=REJECT_BUTTON_STICKY,
    padx=REJECT_BUTTON_PADX,
    pady=REJECT_BUTTON_PADY
)

info_button = Button(
    master=reactions_frame,
    activebackground=INFO_BUTTON_BACKGROUND,
    width=REACTION_BUTTON_WIDTH,
    text=INFO_BUTTON_TEXT,
    command=lambda: load_petition_description(current_petition_index)  # type: ignore
)
info_button.grid(
    row=INFO_BUTTON_ROW,
    column=INFO_BUTTON_COLUMN,
    sticky=INFO_BUTTON_STICKY,
    padx=INFO_BUTTON_PADX,
    pady=INFO_BUTTON_PADY
)

question_button = Button(
    master=reactions_frame,
    foreground=QUESTION_BUTTON_BACKGROUND,
    activebackground=QUESTION_BUTTON_BACKGROUND,
    width=REACTION_BUTTON_WIDTH,
    text=QUESTION_BUTTON_TEXT
)
question_button.grid(
    row=QUESTION_BUTTON_ROW,
    column=QUESTION_BUTTON_COLUMN,
    sticky=QUESTION_BUTTON_STICKY,
    padx=QUESTION_BUTTON_PADX,
    pady=QUESTION_BUTTON_PADY
)

share_button = Button(
    master=reactions_frame,
    foreground=SHARE_BUTTON_FOREGROUND,
    activebackground=SHARE_BUTTON_BACKGROUND,
    width=REACTION_BUTTON_WIDTH,
    text=SHARE_BUTTON_TEXT,
)
share_button.grid(
    row=SHARE_BUTTON_ROW,
    column=SHARE_BUTTON_COLUMN,
    sticky=SHARE_BUTTON_STICKY,
    padx=SHARE_BUTTON_PADX,
    pady=SHARE_BUTTON_PADY
)
# Image Info Label
image_info_label = Label(
    master=home_frame,
    text=IMAGE_INFO_LABEL_TEXT,
    background=IMAGE_INFO_LABEL_BACKGROUND,
    height=IMAGE_INFO_LABEL_HEIGHT,
    width=IMAGE_INFO_LABEL_WIDTH
)
image_info_label.grid(
    row=IMAGE_INFO_LABEL_ROW,
    column=IMAGE_INFO_LABEL_COLUMN,
    sticky=IMAGE_INFO_LABEL_STICKY,
    padx=IMAGE_INFO_LABEL_PADX,
    pady=IMAGE_INFO_LABEL_PADY
)

# Comments Section Frame
comments_section_frame = CTkScrollableFrame(
    master=home_frame,
    width=COMMENTS_SECTION_FRAME_WIDTH,
    height=COMMENTS_SECTION_FRAME_HEIGHT,
    fg_color=COMMENTS_SECTION_FRAME_BACKGROUND,
    scrollbar_button_color=COMMENTS_SECTION_SCROLLBAR_COLOR,
    scrollbar_button_hover_color=COMMENTS_SECTION_SCROLLBAR_HOVER_COLOR
)
comments_section_frame.grid(
    row=IMAGE_INFO_LABEL_ROW + 1,  # Place directly below the image_info_label
    column=COMMENTS_SECTION_FRAME_COLUMN,
    sticky=COMMENTS_SECTION_FRAME_STICKY,
    padx=COMMENTS_SECTION_FRAME_PADX,
    pady=COMMENTS_SECTION_FRAME_PADY
)

next_petition_button = Button(
    master = tab_view.tab(ALL),
    text= NEXT_PETITION_BUTTON_TEXT,
    command= lambda: load_petition('next') # type: ignore
)
next_petition_button.grid(
    row = NEXT_PETITION_BUTTON_ROW,
    column= NEXT_PETITION_BUTTON_COLUMN,
    sticky= NEXT_PETITION_BUTTON_STICKY,
    pady= NEXT_PETITION_BUTTON_PADY,
    padx= NEXT_PETITION_BUTTON_PADX
)

previous_petition_button = Button(
    master = tab_view.tab(ALL),
    text= PREVIOUS_PETITION_BUTTON_TEXT,
    command= lambda: load_petition('previous') # type: ignore
)
previous_petition_button.grid(
    row = PREVIOUS_PETITION_BUTTON_ROW,
    column= PREVIOUS_PETITION_BUTTON_COLUMN,
    sticky= PREVIOUS_PETITION_BUTTON_STICKY,
    pady= PREVIOUS_PETITION_BUTTON_PADY,
    padx= PREVIOUS_PETITION_BUTTON_PADX
)

'''CODE FOR PENDING POST TAB'''
# ======================== APPROVED TAB (NOTIFICATIONS) ========================
# Notifications data list
notifications = []  # List to store notification messages

notifications_frame = CTkScrollableFrame(
    master=tab_view.tab(APPROVED),
    width=FRAME_WIDTH - 20,
    height=FRAME_HEIGHT - 50,
    fg_color="#f0f0f0"
)
notifications_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Initialize dataframes before starting the main loop
initialize_dataframes()

main_window.mainloop()