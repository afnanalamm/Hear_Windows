from customtkinter import *
from customtkinter import CTkImage
from tkinter import *
from tkinter import PhotoImage, messagebox, filedialog, simpledialog, ttk
from LOGIN_WINDOW_CONSTANTS import *
import os, sys, random, time, datetime, subprocess
from MAIN_WINDOW_CONSTANTS import *
from PIL import ImageTk, Image
import pandas as pd
from pathlib import Path



# DATA_DIR = Path("data")
# POSTS_FILE = DATA_DIR / "petitions.csv"
# REACTIONS_FILE = DATA_DIR / "reactions.csv"
# DEFAULT_IMAGE = "default_image.jpg"  # Create this image or modify path

# try:
#     petitions_df = pd.read_csv(POSTS_FILE)
# except FileNotFoundError:
#     petitions_df = pd.DataFrame(columns=[
#         'petition_id', 'user_id', 'title', 'content', 'subdistrict',
#         'city', 'country', 'tags', 'created_at', 'media_path'
#     ])

# try:
#     reactions_df = pd.read_csv(REACTIONS_FILE)
# except FileNotFoundError:
#     reactions_df = pd.DataFrame(columns=[
#         'reaction_id', 'user_id', 'petition_id', 'comment_id',
#         'reaction_type', 'created_at'
#     ])



class AppTabView(CTkTabview):
    def __init__(self, master, **kwargs): #background
        super().__init__(master, **kwargs)

        # Configure grid weights for responsive sizing
        self.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        # create tabs
        self.add(TRENDS)
        self.add(NEW)
        self.add(RESPONSES)
        self.add(SOLUTIONS)
        self.add(YOU)

class CommentsSectionFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        self.label = CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20, sticky = NSEW)   


def authenticate_login(id_entry, password_entry, application_to_open, parent_window): # takes two parameters (password and id)
    id = id_entry.get()
    password = password_entry.get()
    if id != "" and password != "":  # if any ID and Password is given. FUTURE: Hash password; use dictionary; take only id numbers, or emails
        open_application(application_to_open, parent_window)     # application_to_open takes relative filepath
                                                  #subprocess.run('python', file_to_open)        
                                                  # #os.open('python Home_Window.py') AI sugested that this is more modern
        # parent_window.destroy()  # destroy the login window to prevent Python from freezing
        
    else:
        warning = messagebox.showerror(title= 'Error!', message= 'Please enter your login credentials!')

def open_application(rel_file_path, parent_window): # takes relative or file path as argument
    #application = str(rel_file_path)
    #os.system('"%s"' % application)
    subprocess.run(['python', str(rel_file_path)]) 
    '''I ended up using subprocess.run()'''
    parent_window.destroy()  # destroy the login window to prevent Python from freezing



def open_file(canvas):
    global filepath
    filepath = filedialog.askopenfilename(title= 'Select File',
                                           filetypes= (
                                               ('image files', "*.jpg"),
                                               ('text files', "*.txt"),
                                               ("all files", "*.*"))
                                            )
    try:
        image = Image.open(filepath).resize(PICTURE_PREVIEW_IMAGE_SIZE, Image.LANCZOS) # type: ignore
        image = ImageTk.PhotoImage(image)
        canvas.image = image  # keep a reference to avoid garbage collection
        canvas.create_image(0, 0, image=image, anchor=NW)
    except Exception as e:
        print(f"Error loading image: {e}")
        global filepath_from_upload_button
        
# def clear_petition_fields():
#     petition_title_entry.delete(0, END)
#     description_textbox.delete("1.0", END)
#     location_dropdown.set("")

# def create_petition():
#     global petitions_df
#     global tab_view
#     new_petition = {
#         'petition_id': len(petitions_df) + 1,
#         'user_id': 1,
#         'title': petition_title_entry.get(), # type: ignore
#         'content': description_textbox.get("1.0", END).strip(), # type: ignore
#         'subdistrict': location_dropdown.get(), # type: ignore
#         'city': "London",
#         'country': "UK",
#         'tags': "test",
#         'created_at': pd.Timestamp.now(),
#         'media_path': filepath
#     }
    
#     petitions_df = pd.concat([petitions_df, pd.DataFrame([new_petition])], ignore_index=True)
#     save_data()
#     # clear_petition_fields()
#     messagebox.showinfo("Success", "Post created successfully!")



def update_reaction(button):
    current_text = button.cget("text")
    emoji, count = current_text.split()
    new_count = int(count) + 1
    button.configure(text=f"{emoji} {new_count}")

