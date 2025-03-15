from tkinter import *
from tkinter import ttk, PhotoImage, messagebox, filedialog, simpledialog
from customtkinter import *
from customtkinter import CTkImage
from PIL import Image as PilImage, ImageTk
import pandas as pd
from pathlib import Path
# import os, sys, random, time, datetime, subprocess
from LOGIN_WINDOW_CONSTANTS import *
from MAIN_WINDOW_CONSTANTS import *

# Initialize data structures at the start
DATA_DIR = Path("data")
PETITIONS_FILE = DATA_DIR / "petitions.csv"
REACTIONS_FILE = DATA_DIR / "reactions.csv"
COMMENTS_FILE = DATA_DIR / "comments.csv"
ALL_COMMENTS_FILE = DATA_DIR / "all_comments.csv"

# Global variables initialization
comment_reactions = {}
notifications = []
current_petition_index = 0  # Ensure this is defined
comments_holder_list = []  # Initialize comments_holder_list


# Constants
DEFAULT_USER = "You"  # Default username for new comments

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


def post_comment():
    """Handles posting a new comment."""
    global comments_df, all_comments_df

    comment_text = comment_textbox.get("1.0", "end-1c").strip()
    if comment_text:
        new_comment_id = {
            "petition_id": current_petition_index,
            "user_id": 1,
            "all_comments_id": len(all_comments_df) + 1,
        }

        comments_df = pd.concat([comments_df, pd.DataFrame([new_comment_id])], ignore_index=True)
        all_comments_df = pd.concat(
            [all_comments_df, pd.DataFrame([{"all_comments_id": len(all_comments_df) + 1, "comment": comment_text}])],
            ignore_index=True,
        )

        comments_df.to_csv(COMMENTS_FILE, index=False)
        all_comments_df.to_csv(ALL_COMMENTS_FILE, index=False)

        create_comment_widget({"comment": comment_text, "user": DEFAULT_USER}, comments_section_frame)
        comment_textbox.delete("1.0", "end")


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
    global petitions_df, reactions_df, comments_df, all_comments_df
    try:
        petitions_df = pd.read_csv(PETITIONS_FILE) if PETITIONS_FILE.exists() else pd.DataFrame(columns=[
            "petition_id", "user_id", "title", "content", "subdistrict", "city", "country", "tags", "created_at", "media_path"
        ])
        reactions_df = pd.read_csv(REACTIONS_FILE) if REACTIONS_FILE.exists() else pd.DataFrame(columns=[
            "reaction_id", "user_id", "petition_id", "reaction_type", "created_at"
        ])
        comments_df = pd.read_csv(COMMENTS_FILE) if COMMENTS_FILE.exists() else pd.DataFrame(columns=[
            "petition_id", "user_id", "all_comments_id"
        ])
        all_comments_df = pd.read_csv(ALL_COMMENTS_FILE) if ALL_COMMENTS_FILE.exists() else pd.DataFrame(columns=[
            "all_comments_id", "comment"
        ])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initialize data: {e}")
        raise


initialize_dataframes()

# Load like/dislike counts
try:
    with open("LikeDislikeStats.txt", "r") as stats_file:
        agree_count = stats_file.readline().strip() or "0"
        disagree_count = stats_file.readline().strip() or "0"
except FileNotFoundError:
    agree_count, disagree_count = "0", "0"
    with open("LikeDislikeStats.txt", "w") as stats_file:
        stats_file.write("0\n0")



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
    global agree_count, disagree_count

    if stat_type == "agree":
        agree_count = str(int(agree_count) + 1)
    elif stat_type == "disagree":
        disagree_count = str(int(disagree_count) + 1)

    with open("LikeDislikeStats.txt", "w") as stats_file:
        stats_file.write(f"{agree_count}\n{disagree_count}")

    agree_stat.configure(text=f"Agree: {agree_count}")
    disagree_stat.configure(text=f"Disagree: {disagree_count}")


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
        'media_path': filepath
    }
    petitions_df = pd.concat([petitions_df, pd.DataFrame([new_petition])], ignore_index=True)
    save_data()
    messagebox.showinfo("Success", "Post created successfully!")

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
tab_view.add(TRENDS)
tab_view.add(NEW)
tab_view.add(RESPONSES)
tab_view.add(SOLUTIONS)
tab_view.add(YOU)

tab_view.tab(TRENDS).configure(height=TAB_HEIGHT, width=TAB_WIDTH)  # just resizing all tabs, so that they are all the same size
tab_view.tab(NEW).configure(height=TAB_HEIGHT, width=TAB_WIDTH)  # needed to resize this one initially, as the image-display frame was being cut off
tab_view.tab(RESPONSES).configure(height=TAB_HEIGHT, width=TAB_WIDTH)
tab_view.tab(SOLUTIONS).configure(height=TAB_HEIGHT, width=TAB_WIDTH)
tab_view.tab(YOU).configure(height=TAB_HEIGHT, width=TAB_WIDTH)

home_frame = Frame(master=tab_view.tab(TRENDS), background=FRAME_BACKGROUND, width=FRAME_WIDTH, height=FRAME_HEIGHT)
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

def update_stat(stat_type, agree, disagree):
    """Updates agree/disagree counts and saves them to a file."""
    global agree_count, disagree_count

    if stat_type == "agree":
        agree_count = str(int(agree_count) + 1)
    elif stat_type == "disagree":
        disagree_count = str(int(disagree_count) + 1)

    with open("LikeDislikeStats.txt", "w") as stats_file:
        stats_file.write(f"{agree_count}\n{disagree_count}")

    agree.configure(text=f"Agree: {agree_count}")
    disagree.configure(text=f"Disagree: {disagree_count}")

stat_type = StringVar()  # Need this to check the value of the radiobuttons-AG🟨

# Stats labels
agree_stat = CTkLabel(
    master=reactions_frame,  # label for agree stat -AG🟨
    text=("Agree:", agree_count)
)
agree_stat.grid(
    row=0,
    column=0
)

disagree_stat = CTkLabel(
    master=reactions_frame,  # label for disagree stat -AG🟨
    text=("Disagree:", disagree_count)
)
disagree_stat.grid(
    row=1,
    column=0
)

agree_button = Radiobutton(
    master=reactions_frame,
    foreground=AGREE_BUTTON_BACKGROUND,
    activebackground=AGREE_BUTTON_BACKGROUND,
    width=7,  # REACTION_BUTTON_WIDTH
    text='AGREE', variable=stat_type, value=0,  # Added variable=stat_type -AG🟨
    command= update_stat('agree', agree_stat, disagree_stat)  # just added the command after to the agree/disagree buttons, which AG🟨 forgot --AA🟥
)
agree_button.grid(row=2, column=0)

disagree_button = Radiobutton(
    master=reactions_frame,
    foreground=DISAGREE_BUTTON_BACKGROUND,
    activebackground=DISAGREE_BUTTON_BACKGROUND,
    width= REACTION_BUTTON_WIDTH,
    text='DISAGREE',variable=stat_type, value=1, #Will not work without variable=stat_type -AG🟨
    command= lambda: update_stat('disagree', agree_stat, disagree_stat)
)
disagree_button.grid(row=3, column=0)  # row=3 AG🟨


# Additional buttons
info_button = Button(
    master=reactions_frame,
    activebackground=INFO_BUTTON_BACKGROUND,
    width=REACTION_BUTTON_WIDTH,
    text=INFO_BUTTON_TEXT,
    command= lambda: load_petition_description(current_petition_index)
)
info_button.grid(row=4, column=0)  # row 4 -AG🟨

question_button = Button(
    master=reactions_frame,
    foreground=QUESTION_BUTTON_BACKGROUND,
    activebackground=QUESTION_BUTTON_BACKGROUND,
    width=REACTION_BUTTON_WIDTH,
    text=QUESTION_BUTTON_TEXT
)
question_button.grid(row=5, column=0)  # row 5 -AG🟨

share_button = Button(
    master=reactions_frame,
    foreground=SHARE_BUTTON_FOREGROUND,
    activebackground=SHARE_BUTTON_BACKGROUND,
    width=REACTION_BUTTON_WIDTH,
    text=SHARE_BUTTON_TEXT,
)
share_button.grid(row=6, column=0)

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

# After comments_section_frame setup and before the next_petition_button
# Create comment entry frame
comment_entry_frame = Frame(
    master=home_frame,
    width=COMMENT_ENTRY_FRAME_WIDTH,
    height=COMMENT_ENTRY_FRAME_HEIGHT,
    bg=COMMENT_ENTRY_FRAME_BACKGROUND
)
comment_entry_frame.grid(
    row=COMMENT_ENTRY_FRAME_ROW,
    column=COMMENT_ENTRY_FRAME_COLUMN,
    sticky=COMMENT_ENTRY_FRAME_STICKY,
    padx=COMMENT_ENTRY_FRAME_PADX,
    pady=COMMENT_ENTRY_FRAME_PADY
)

# Create comment textbox
comment_textbox = Text(
    master=comment_entry_frame,
    height=COMMENT_TEXTBOX_HEIGHT,
    width=COMMENT_TEXTBOX_WIDTH,
    font=COMMENT_TEXTBOX_FONT,
    wrap=COMMENT_TEXTBOX_WRAP,
)
comment_textbox.pack(
    padx=COMMENT_TEXTBOX_PADX,
    pady=COMMENT_TEXTBOX_PADY
)

# Create petition button
post_comment_button = Button(
    master=comment_entry_frame,
    text=POST_COMMENT_BUTTON_TEXT,
    width=POST_COMMENT_BUTTON_WIDTH,
    height=POST_COMMENT_BUTTON_HEIGHT,
    bg=POST_COMMENT_BUTTON_BG,
    fg=POST_COMMENT_BUTTON_FG,
    font=POST_COMMENT_BUTTON_FONT,
    command=post_comment
)
post_comment_button.pack(
    padx=POST_COMMENT_BUTTON_PADX, 
    pady=POST_COMMENT_BUTTON_PADY
)

next_petition_button = Button(
    master = tab_view.tab(TRENDS),
    text= NEXT_PETITION_BUTTON_TEXT,
    command= lambda: load_petition('next')
)
next_petition_button.grid(
    row = NEXT_PETITION_BUTTON_ROW,
    column= NEXT_PETITION_BUTTON_COLUMN,
    sticky= NEXT_PETITION_BUTTON_STICKY,
    pady= NEXT_PETITION_BUTTON_PADY,
    padx= NEXT_PETITION_BUTTON_PADX
)

previous_petition_button = Button(
    master = tab_view.tab(TRENDS),
    text= PREVIOUS_PETITION_BUTTON_TEXT,
    command= lambda: load_petition('previous')
)
previous_petition_button.grid(
    row = PREVIOUS_PETITION_BUTTON_ROW,
    column= PREVIOUS_PETITION_BUTTON_COLUMN,
    sticky= PREVIOUS_PETITION_BUTTON_STICKY,
    pady= PREVIOUS_PETITION_BUTTON_PADY,
    padx= PREVIOUS_PETITION_BUTTON_PADX
)

'''CODE FOR NEW POST TAB'''
new_petition_frame = Frame(
    master=tab_view.tab(NEW), 
    background='#aaaaaa',
    width=NEW_PETITION_FRAME_WIDTH,
    height=NEW_PETITION_FRAME_HEIGHT,
    border=NEW_PETITION_FRAME_BORDER,
    cursor=NEW_PETITION_FRAME_CURSOR,
    padx=NEW_PETITION_FRAME_PADX,
    pady=NEW_PETITION_FRAME_PADY
)
new_petition_frame.place(
    relx=NEW_PETITION_FRAME_RELX,
    rely=NEW_PETITION_FRAME_RELY
    
)

picture_preview_canvas = Canvas(
    master=new_petition_frame,
    width=PICTURE_PREVIEW_WIDTH,
    height=PICTURE_PREVIEW_HEIGHT
)
picture_preview_canvas.create_text(
    PICTURE_PREVIEW_WIDTH / 2,
    PICTURE_PREVIEW_HEIGHT / 2,
    text=PICTURE_PREVIEW_TEXT
)
picture_preview_canvas.grid(
    row=PICTURE_PREVIEW_ROW,
    column=PICTURE_PREVIEW_COLUMN,
    rowspan=PICTURE_PREVIEW_ROWSPAN,
    columnspan=PICTURE_PREVIEW_COLUMNSPAN,
    padx=PICTURE_PREVIEW_PADX,
    pady=PICTURE_PREVIEW_PADY,
)

petition_description_frame = Frame(
    master=new_petition_frame, 
    background=POST_DESCRIPTION_FRAME_BACKGROUND,
    width=POST_DESCRIPTION_FRAME_WIDTH,
    height=POST_DESCRIPTION_FRAME_HEIGHT
)
petition_description_frame.grid(
    row=POST_DESCRIPTION_FRAME_ROW, 
    column=POST_DESCRIPTION_FRAME_COLUMN,
    sticky=POST_DESCRIPTION_FRAME_STICKY
)

location_dropdown = CTkComboBox(
    master=petition_description_frame, 
    values=LOCATION_DROPDOWN_VALUES, 
    width=5
)
location_dropdown.grid(
    row=LOCATION_DROPDOWN_ROW, 
    column=LOCATION_DROPDOWN_COLUMN, 
    sticky=LOCATION_DROPDOWN_STICKY
)

upload_cancel_button_frame = Frame(
    master= petition_description_frame,
    # width= UPLOAD_CANCEL_BUTTON_FRAME_WIDTH

)
upload_cancel_button_frame.grid(
    row=UPLOAD_CANCEL_BUTTON_FRAME_ROW,
    column=UPLOAD_CANCEL_BUTTON_FRAME_COLUMN,
    # columnspan=UPLOAD_CANCEL_BUTTON_FRAME_COLUMNSPAN,
    sticky=UPLOAD_CANCEL_BUTTON_FRAME_STICKY
)

upload_button = Button(
    master= upload_cancel_button_frame,
    text=UPLOAD_BUTTON_TEXT,
    width=UPLOAD_BUTTON_WIDHT,
    height=UPLOAD_BUTTON_HEIGHT,
    background=UPLOAD_BUTTON_BACKGROUND,
    fg=UPLOAD_BUTTON_FOREGROUND,
    command=lambda: open_file(picture_preview_canvas) # type: ignore
)
upload_button.grid(
    # relx=UPLOAD_BUTTON_RELX,
    # rely=UPLOAD_BUTTON_RELY
    row= UPLOAD_BUTTON_ROW,
    column=UPLOAD_BUTTON_COLUMN,
    sticky= UPLOAD_BUTTON_STICKY
)

cancel_upload_button = Button(
    master=upload_cancel_button_frame,  # Master frame (tab in this case)
    text=CANCEL_UPLOAD_BUTTON_TEXT,  # Button text
    width=CANCEL_UPLOAD_BUTTON_WIDTH,  # Button width
    height=CANCEL_UPLOAD_BUTTON_HEIGHT,  # Button height
    background=CANCEL_UPLOAD_BUTTON_BACKGROUND,  # Background color
    fg=CANCEL_UPLOAD_BUTTON_FOREGROUND,  # Text color
    command=lambda: picture_preview_canvas.delete("all")  # Command to execute
)
# Place the button in the window
cancel_upload_button.grid(
    # rely and relx not being used, as I switched to grid()
    # relx=CANCEL_UPLOAD_BUTTON_RELX,  # Relative x position
    # rely=CANCEL_UPLOAD_BUTTON_RELY  # Relative y position
    row=CANCEL_UPLOAD_BUTTON_ROW,
    column=CANCEL_UPLOAD_BUTTON_COLUMN,
    sticky=CANCEL_UPLOAD_BUTTON_STICKY
)

petition_title_label = Label(
    master=petition_description_frame,
    relief=POST_TITLE_ENTRY_RELIEF,
    borderwidth=POST_TITLE_ENTRY_BORDERWIDTH,  # has more functionality that CtkEntry
    width=POST_TITLE_ENTRY_WIDTH,
    text=POST_TITLE_LABEL_TEXT
)
petition_title_label.grid(
    row=POST_TITLE_ENTRY_ROW - 1,
    column=POST_TITLE_ENTRY_COLUMN,
    sticky=NSEW,
    padx=POST_TITLE_ENTRY_PADX,
    pady=POST_TITLE_ENTRY_PADY
)

petition_title_entry = Entry(
    master=petition_description_frame,
    relief=POST_TITLE_ENTRY_RELIEF,
    borderwidth=POST_TITLE_ENTRY_BORDERWIDTH,  # has more functionality that CtkEntry
    width=POST_TITLE_ENTRY_WIDTH
)
petition_title_entry.grid(
    row=POST_TITLE_ENTRY_ROW,
    column=POST_TITLE_ENTRY_COLUMN,
    sticky=NSEW,
    padx=POST_TITLE_ENTRY_PADX,
    pady=POST_TITLE_ENTRY_PADY
)

description_label = Label(
    master=petition_description_frame,
    relief=POST_TITLE_ENTRY_RELIEF,
    borderwidth=DESCRIPTION_LABEL_BORDERWIDTH,
    width=DESCRIPTION_LABEL_WIDTH,
    text=DESCRIPTION_LABEL_TEXT
)
description_label.grid(
    row=DESCRIPTION_LABEL_ROW,
    column=DESCRIPTION_LABEL_COLUMN,
    sticky=DESCRIPTION_LABEL_STICKY,
    padx=DESCRIPTION_LABEL_PADX,
    pady=DESCRIPTION_LABEL_PADY
)

description_textbox = CTkTextbox(
    master=petition_description_frame,
    width=DESCRIPTION_TEXTBOX_WIDTH,
    corner_radius=DESCRIPTION_TEXTBOX_CORNER_RADIUS,
    wrap=DESCRIPTION_TEXTBOX_WRAP,
    text_color=DESCRIPTION_TEXTBOX_TEXT_COLOUR,
    bg_color=DESCRIPTION_TEXTBOX_BACKGROUND,
    fg_color=DESCRIPTION_TEXTBOX_FG_COLOUR,
    border_color=DESCRIPTION_TEXTBOX_BORDER_COLOUR,
    border_width=DESCRIPTION_TEXTBOX_BORDER_WIDTH
)
description_textbox.grid(
    row=DESCRIPTION_TEXTBOX_ROW,
    column=DESCRIPTION_TEXTBOX_COLUMN,
    sticky=DESCRIPTION_TEXTBOX_STICKY
)

# Create the urgent checkbox
urgent_checkbox = CTkCheckBox(
    master=petition_description_frame,
    text=URGENT_CHECKBOX_TEXT,
    text_color=URGENT_CHECKBOX_TEXT_COLOR,
    fg_color=URGENT_CHECKBOX_FG_COLOR,
    border_color=URGENT_CHECKBOX_BORDER_COLOR,
    border_width=URGENT_CHECKBOX_BORDER_WIDTH,
    width=URGENT_CHECKBOX_WIDTH,
    height=URGENT_CHECKBOX_HEIGHT,
    corner_radius=URGENT_CHECKBOX_CORNER_RADIUS,
    hover_color=URGENT_CHECKBOX_HOVER_COLOR,
    bg_color="transparent"  # Changed from URGENT_CHECKBOX_BACKGROUND_COLOR
)
urgent_checkbox.grid(
    row=URGENT_CHECKBOX_ROW,
    column=URGENT_CHECKBOX_COLUMN,
    sticky=URGENT_CHECKBOX_STICKY
)

petition_button = CTkButton(
    master=petition_description_frame,  # Master frame
    text=PETITION_BUTTON_TEXT,  # Button text
    width=PETITION_BUTTON_WIDTH,  # Button width
    height=PETITION_BUTTON_HEIGHT,  # Button height
    corner_radius=PETITION_BUTTON_CORNER_RADIUS,  # Corner radius
    border_width=PETITION_BUTTON_BORDER_WIDTH,  # Border width
    fg_color=PETITION_BUTTON_FG_COLOR,  # Foreground color
    hover_color=PETITION_BUTTON_HOVER_COLOR,  # Hover color
    border_color=PETITION_BUTTON_BORDER_COLOR,  # Border color
    text_color=PETITION_BUTTON_TEXT_COLOR,  # Text color
    font=PETITION_BUTTON_FONT,  # Font and size
    state=PETITION_BUTTON_STATE,  # Button state
    hover=PETITION_BUTTON_HOVER,  # Enable hover effect
    command= create_petition
)
# Place the button in the grid
petition_button.grid(
    row=PETITION_BUTTON_ROW,
    column=PETITION_BUTTON_COLUMN,
    sticky=PETITION_BUTTON_STICKY
)

# ======================== RESPONSES TAB (NOTIFICATIONS) ========================
# Notifications data list
notifications = []  # List to store notification messages

notifications_frame = CTkScrollableFrame(
    master=tab_view.tab(RESPONSES),
    width=FRAME_WIDTH - 20,
    height=FRAME_HEIGHT - 50,
    fg_color="#f0f0f0"
)
notifications_frame.pack(pady=10, padx=10, fill="both", expand=True)

main_window.mainloop()