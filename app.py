import tkinter as tk
import os
import sys
import subprocess
import assessments
from PIL import Image, ImageTk

def ensure_requirements(req_file="requirements.txt"):
    if not os.path.exists(req_file):
        return
    if os.environ.get("LABOR_REQ_INSTALLED") == "1":
        return
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], check=True)
        os.environ["LABOR_REQ_INSTALLED"] = "1"
    except subprocess.CalledProcessError as e:
        print("Failed to install requirements:", e)

ensure_requirements()

root = tk.Tk()
root.title("LABOR - Applicatie")
root.geometry("1000x600")
root.configure(bg="white")

SIDEBAR_WIDTH = 180
LOGO_MAX_SIZE = 160

sidebar = tk.Frame(root, bg="black", width=SIDEBAR_WIDTH)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)


logo_path = os.path.join("images", "Labor-logo.png")
try:
    original_img = Image.open(logo_path)
    w, h = original_img.size
    max_size = min(LOGO_MAX_SIZE, SIDEBAR_WIDTH - 40)
    scale = min(max_size / w, max_size / h)
    new_size = (int(w * scale), int(h * scale))
    resized_img = original_img.resize(new_size, Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(resized_img)

    logo_label = tk.Label(sidebar, image=logo, bg="black")
    logo_label.image = logo
    logo_label.place(relx=0.5, rely=1.0, anchor="s", y=-20)
except Exception as e:
    print("Logo error:", e)

content = tk.Frame(root, bg="white")
content.pack(side="right", expand=True, fill="both")

BUTTON_WIDTH = 18
BUTTON_HEIGHT = 4
BUTTON_BG = "#d9d9d9"
BUTTON_FONT = ("Segoe UI", 12)
btn_back = tk.Button(
    sidebar,
    text="← Terug",
    bg="black",
    fg="white",
    relief="flat",
    bd=0,
    font=("Segoe UI", 11, "bold"),
    activebackground="black",
    activeforeground="white",
)

def show_back_button():
    if not btn_back.winfo_ismapped():
        btn_back.pack(anchor="nw", pady=20, padx=15)

def hide_back_button():
    if btn_back.winfo_ismapped():
        btn_back.pack_forget()


def open_prognose_model():
        
#go to Prognosemodel.py


def show_home():
    hide_back_button()

    for w in content.winfo_children():
        w.destroy()

    button_frame = tk.Frame(content, bg="white")
    button_frame.pack(expand=True)

    btn_assessments = tk.Button(
        button_frame,
        text="Assessments",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        bg=BUTTON_BG,
        relief="flat",
        font=BUTTON_FONT,
        command=open_assessments,
    )
    btn_assessments.grid(row=0, column=0, padx=60, pady=20)

    btn_prognose = tk.Button(
        button_frame,
        text="Prognose model",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        bg=BUTTON_BG,
        relief="flat",
        font=BUTTON_FONT,
        command=open_prognose_model,
    )
    btn_prognose.grid(row=0, column=1, padx=60, pady=20)

def open_loopbaanankers():
    """Toon de pagina Fase 2.0 – Loopbaanankers in de rechterkant."""
    show_back_button()
    btn_back.config(command=open_assessments)   # ← HIER toegevoegd

    for w in content.winfo_children():
        w.destroy()

    assessments.build_loopbaanankers_page(content)

def open_assessments():
    show_back_button()
    btn_back.config(command=show_home)

    for w in content.winfo_children():
        w.destroy()

    assessments.build_assessments_page(content, open_loopbaanankers)

show_home()

root.mainloop()