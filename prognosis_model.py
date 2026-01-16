# prognosis_model.py
import tkinter as tk
from tkinter import ttk

# --------- Prognosis model page entry point ---------
def build_prognosis_page(parent):
    parent.configure(bg="white")

    # Clear previous widgets
    for w in parent.winfo_children():
        w.destroy()
    
    # --------- Page frame ---------
    page = tk.Frame(parent, bg="white")
    page.pack(fill="both", expand=True)

    # --------- Page header ---------
    header = tk.Frame(page, bg="white")
    header.pack(fill="x", padx=30, pady=(20, 10))

    title = tk.Label(
        header,
        text="Integratie prognosemodel",
        bg="white",
        fg="black",
        font=("Segoe UI", 14, "bold"),
        anchor="w"
    )
    title.pack(anchor="w")

    subtitle = tk.Label(
        header,
        text="Geef hier een uitleg over de pagina", # Placeholder description
        bg="white",
        fg="#000000",
        font=("Segeo UI", 10, "normal"),
        anchor="w"
    )
    subtitle.pack(anchor="w", pady=(4, 0))

    # --------- Scrollable content area ---------
    container = tk.Frame(page, bg="white")
    container.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = tk.Canvas(container, bg="white", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        container,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    content = tk.Frame(canvas, bg="#C0C0C0")
    canvas_window = canvas.create_window((0, 0), window=content, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=event.width)

    content.bind("<Configure>", on_configure)

    # --------- Section header: personalia ---------
    section = tk.Label(
        content,
        text="1. Personalia",
        bg="#727272",
        fg="white",
        padx=10,
        pady=6,
        anchor="w"
    )
    section.pack(fill="x", pady=(10, 0))

    def make_question_row(parent, number: int, question: str, options: list):
        """
        Creates a single question row with a number label, question text, and radiobutton options.

        Args:
            parent (tk.Frame): Parent frame to add the row.
            number (int): Question number.
            question (str): Question text.
            options (list[str]): List of option strings for radiobuttons.
        
        Returns:
            tk.StringVar: Variable storing the selected option.
        """
        row_frame = tk.Frame(parent, bg="B3B3B3")
        row_frame.pack(fill="x", pady=4, padx=10)

        # Number label
        num_label = tk.Label(
            row_frame,
            text=str(number),
            width=4,
            bg="F1C40F"
        )