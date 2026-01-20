# ui_components.py
import tkinter as tk

# --- Scrollable container ---
def create_scrollable_container(parent, bg="white"):
    container = tk.Frame(parent, bg=bg)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=bg, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scroll_frame= tk.Frame(canvas, bg=bg)
    window_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_frame_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_resize(event):
        canvas.itemconfig(window_id, width=event.width)

    scroll_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_resize)

    def on_mousewheel(event):
        canvas.yview_scroll(-int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    return {
        "container": container,
        "canvas": canvas,
        "content": scroll_frame
    }

# --- Title and subtitle ---
def create_page_title(parent, title_text, subtitle_text):
    # -- Title label --
    title = tk.Label(
        parent,
        text=title_text,
        bg="white",
        fg="black",
        font=("Segoe UI", 14, "bold"),
        anchor="w"
    )
    title.pack(fill="x", padx=20, pady=(15, 5))

    # -- Subtitle label --
    subtitle = tk.Label(
        parent,
        text=subtitle_text,
        bg="white",
        fg="black",
        font=("Segoe UI", 10),
        anchor="w",
        justify="left"
    )
    subtitle.pack(fill="x", padx=20, pady=(0, 15))

    return title, subtitle

# --- Column headers ---
def create_column_headers(parent, labels, bg_color):
    header = tk.Frame(parent, bg=bg_color)
    header.pack(fill="x")
    for col, text in enumerate(labels):
        tk.Label(
            header,
            text=text,
            bg=bg_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w" if col < 2 else "e",
            padx=10 if col < 2 else 40,
            width=8 if col == 0 else None
        ).grid(row=0, column=col, sticky="w" if col < 2 else "e")
    
    return header

# --- Column row ---
def create_likert_row(parent, number, statement, var, options, styles):
    row = tk.Frame(parent, bg=styles["row_bg"])
    row.pack(fill="x", pady=1)
    row.grid_columnconfigure(1, weight=1)

    # -- Number label --
    num_label = tk.Label(
        row,
        text=str(number),
        width=4,
        bg=styles["number_bg"],
        fg="black",
        font=styles["number_font"],
        anchor="c"
    )
    num_label.grid(row=0, column=0, padx=(10, 10), sticky="w")

    # -- Statement label --
    stmt_label = tk.Label(
        row,
        text=statement,
        bg=styles["row_bg"],
        fg="black",
        font=styles["text_font"],
        anchor="w",
        justify="left",
        wraplength=650
    )
    stmt_label.grid(row=0, column=1, sticky="w", padx=10, pady=8)

    likert_frame = tk.Frame(row, bg=styles["row_bg"])
    likert_frame.grid(row=0, column=2, padx=20, pady=8, sticky="e")

    buttons = []

    def update_buttons():
        current = var.get()
        for value, widget in buttons:
            if current == value:
                widget.config(relief="sunken", bg=styles["active_bg"], fg="white")
            else:
                widget.config(relief="raised", bg=styles["inactive_bg"], fg="black")
    
    for col, value in enumerate(options):
        btn = tk.Label(
            likert_frame,
            text=value,
            width=3,
            bd=1,
            relief="raised",
            bg=styles["inactive_bg"],
            fg="black",
            font=styles["button_font"]
        )
        btn.grid(row=0, column=col, padx=4)

        def on_click(event, v=value):
            var.set(v)
            update_buttons()

        btn.bind("<Button-1>", on_click)
        buttons.append((value, btn))
    
    return row
