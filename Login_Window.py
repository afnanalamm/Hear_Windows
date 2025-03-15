from customtkinter import * 
from customtkinter import CTkImage
from LOGIN_WINDOW_CONSTANTS import *
from FUNCTIONS import *
#from PIL import Image, ImageTk
from tkinter import *
from tkinter import PhotoImage
import os                           #DON'T REALLY NEED: from subprocess import run



login_window = Tk()  # create the window

# LOGIN_WINDOW_LIGHT_ICON = Image.open("LOGIN_WINDOW_ICON.jpg")
# LOGIN_WINDOW_DARK_ICON = Image.open("LOGIN_WINDOW_ICON.jpg")

# login_window.update_idletasks()  # Update the window to get correct width and height
SCREEN_WIDTH = login_window.winfo_width()  # type: ignore
SCREEN_HEIGHT = login_window.winfo_height()  # type: ignore

login_window.geometry(f"{LOGIN_WINDOW_WIDTH}x{LOGIN_WINDOW_HEIGHT}")
login_window.title(LOGIN_WINDOW_TITLE)
# login_window._set_appearance_mode(LOGIN_WINDOW_APPEARANCE_MODE)
login_window.configure(width= 10)
login_window.iconbitmap("LOGIN_WINDOW_ICON.ico") # set the window icon


# setting all the boundary cells to have a width and height of 1, and only the central cell to have a width and height of 10
login_window.columnconfigure((0,2), weight=1)
login_window.columnconfigure((1),   weight=10)
login_window.rowconfigure((0,2),    weight=1)
login_window.rowconfigure((1),      weight=10)

login_frame = CTkFrame(master=login_window, bg_color=LOGIN_WINDOW_FRAME_BACKGROUND_COLOR, corner_radius=LOGIN_WINDOW_FRAME_CORNER_RADIUS, 
                       width=LOGIN_WINDOW_FRAME_WIDTH,   height=LOGIN_WINDOW_FRAME_HEIGHT, border_color=LOGIN_WINDOW_FRAME_BORDER_COLOUR)

login_frame.grid(row=2, column=1, sticky='nsew') # make the frame expand to fill the whole cell
login_frame.configure(bg_color = LOGIN_WINDOW_FRAME_BACKGROUND_COLOR, corner_radius = LOGIN_WINDOW_FRAME_CORNER_RADIUS, 
                      border_color = LOGIN_WINDOW_FRAME_BORDER_COLOUR)
login_frame.columnconfigure((0,1), weight= 1)
login_frame.rowconfigure((0,1),    weigh = 1)

resident_id_label = Label(master= login_frame, text= RESIDENT_ID_LABEL_TEXT, font= RESIDENT_ID_LABEL_FONT,)   
#creating the Resident ID label    corner_radius= RESIDENT_ID_LABEL_CORNER_RADIUS

resident_id_label.grid(row = 0, column = 0, sticky = 'nsew')  # place the label at the top left corner of the frame
# resident_id_label._set_appearance_mode(LOGIN_WINDOW_APPEARANCE_MODE)  # set it to have the same apprearnce mode as the parent window
resident_id_label.configure(height = RESIDENT_ID_LABEL_HEIGHT, 
                            background = RESIDENT_ID_LABEL_BACKGROUND_COLOR, 
                            foreground = RESIDENT_ID_LABEL_FOREGROUND_COLOR #                     ch     
                            )  # make the label expand to fill the whole cell
# Removed duplicate label creation

resident_password_label = Label(master= login_frame, text= RESIDENT_PASSWORD_LABEL_TEXT, font= RESIDENT_PASSWORD_LABEL_FONT,)
#creating the Resident ID label    corner_radius= RESIDENT_ID_LABEL_CORNER_RADIUS

resident_password_label.grid(row = 1, column = 0, sticky = 'nsew')  # place the label at the top left corner of the frame
# resident_id_label._set_appearance_mode(LOGIN_WINDOW_APPEARANCE_MODE)  # set it to have the same apprearnce mode as the parent window
resident_password_label.configure(
                            height = RESIDENT_PASSWORD_LABEL_HEIGHT, 
                            background = RESIDENT_PASSWORD_LABEL_BACKGROUND_COLOR, 
                            foreground = RESIDENT_PASSWORD_LABEL_FOREGROUND_COLOR                            
                            )  # make the label expand to fill the whole cell

resident_id_entry = CTkEntry(master= login_frame, corner_radius= RESIDENT_ID_ENTRY_CORNER_RADIUS)
resident_id_entry.grid(row = 0, column = 1, stick = 'ew') # make the entry box expand to streach the whole cell's width

resident_password_entry = CTkEntry(master= login_frame, corner_radius= RESIDENT_ID_ENTRY_CORNER_RADIUS)
resident_password_entry.grid(row = 1, column = 1, stick = 'ew') # make the entry box expand to streach the whole cell's width

login_button = CTkButton(master= login_frame,     text= LOGIN_BUTTON_TEXT,    corner_radius= LOGIN_BUTTON_CORNER_RADIUS, 
                         font= LOGIN_BUTTON_FONT, fg_color= LOGIN_BUTTON_FG,
                         hover=LOGIN_BUTTON_HOVER,
                         command= lambda: authenticate_login(resident_id_entry, resident_password_entry, 'Main_Window.py', login_window)) # hover_foreground= LOGIN_BUTTON_HOVER_FG, hover_background= LOGIN_BUTTON_HOVER_BG , bg_color= LOGIN_BUTTON_BG
# hover_foreground and hover_background DON'T EVEN EXIST!!!

login_button.place(relx=0.5, rely=0.5, anchor=CENTER)  # place the button in the center of the frame


login_window.mainloop()

