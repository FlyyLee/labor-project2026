import tkinter as tk
from tkinter import ttk, scrolledtext

# Structuur:
# {
#   "Bloktitel": [
#       {
#           "id": "Q1",
#           "vraag": "Vraagtekst",
#           "opties": {"Optietekst": gewicht (float)}
#       }, ...
#   ]
# }
# Gewicht 0.25 = minimale belemmering, 1.00 = maximale belemmering

PROGNOSE_MODEL_DATA = {
    "I. PERSOON (Personalia, Gezondheid, Profilering, Competentie)": [
        {
            "id": "Q1",
            "vraag": "Q1: Wat is de huidige fysieke gezondheidstoestand?",
            "opties": {
                "Uitstekend (0 beperkingen)": 0.25,
                "Goed (kleine beperkingen)": 0.50,
                "Matig (aanzienlijke beperkingen)": 0.75,
                "Slecht (zeer ernstig belemmerend)": 1.00,
            },
        },
        # Overige vragen zijn inhoudelijk ongewijzigd en hier weggelaten
    ],
}

# SCORE-CONSTANTEN
# Het model gaat uit van één gekozen optie per vraag.
# De minimale en maximale score volgen direct uit het aantal vragen.

QUESTION_COUNT = sum(len(block) for block in PROGNOSE_MODEL_DATA.values())
MIN_SCORE = QUESTION_COUNT * 0.25
MAX_SCORE = QUESTION_COUNT * 1.00
SCORE_RANGE = MAX_SCORE - MIN_SCORE


def get_risk_level(total_score: float):
    """
    Zet een totale gewogen score om naar:
    - risicopercentage (0–100)
    - classificatie (laag → zeer hoog)
    - korte interpretatieve toelichting

    Deze functie bevat bewust géén UI-logica.
    """

    percentage = ((total_score - MIN_SCORE) / SCORE_RANGE) * 100
    percentage = max(0, min(100, percentage))

    if percentage <= 20:
        return (
            "LAAG RISICO",
            "Weinig belemmeringen; snelle en duurzame plaatsing is realistisch.",
            "#228B22",
            percentage,
        )
    if percentage <= 45:
        return (
            "GEMIDDELD RISICO",
            "Overwegend goede kansen, maar enkele drempels vragen gerichte aandacht.",
            "#FFBF00",
            percentage,
        )
    if percentage <= 75:
        return (
            "HOOG RISICO",
            "Meerdere structurele drempels; intensieve begeleiding is noodzakelijk.",
            "#FFA500",
            percentage,
        )

    return (
        "ZEER HOOG RISICO",
        "Ernstige structurele belemmeringen; fundamentele interventie vereist.",
        "#DC143C",
        percentage,
    )


def calculate_results(variables: dict):
    """
    Leest alle antwoorden uit de UI-variabelen en berekent:
    - totale gewogen score
    - aantal onbeantwoorde vragen

    Verwacht dat elke StringVar exact overeenkomt met een optie in de data.
    """

    question_map = {
        q["id"]: q
        for block in PROGNOSE_MODEL_DATA.values()
        for q in block
    }

    total_score = 0.0
    missing = 0

    for q_id, var in variables.items():
        selected = var.get()
        if not selected:
            missing += 1
            continue
        total_score += question_map[q_id]["opties"][selected]

    return total_score, missing

#UI

def build_prognose_page(root: tk.Widget):
    """
    Bouwt de volledige Tkinter-interface in het meegegeven root-widget.

    Verwacht een Tk- of Frame-instantie; bestaande children worden verwijderd.
    """

    COLORS = {
        "bg": "white",
        "fg": "black",
        "accent": "#f0f0f0",
        "button_bg": "#333333",
        "button_fg": "white",
    }

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=COLORS["bg"])

    variables = {}

    main = tk.Frame(root, bg=COLORS["bg"])
    main.pack(fill="both", expand=True, padx=20, pady=20)

    left = tk.Frame(main, bg=COLORS["bg"])
    right = tk.Frame(main, bg=COLORS["bg"])
    left.grid(row=0, column=0, sticky="nsew")
    right.grid(row=0, column=1, sticky="n")

    main.grid_columnconfigure(0, weight=4)
    main.grid_columnconfigure(1, weight=1)

    # Scrollbare container voor de vragenlijst
    canvas = tk.Canvas(left, bg=COLORS["bg"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
    content = tk.Frame(canvas, bg=COLORS["bg"])

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    window = canvas.create_window((0, 0), window=content, anchor="nw")

    content.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )
    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfigure(window, width=e.width),
    )

    tk.Label(
        content,
        text="Prognosemodel Re-integratiekansen",
        font=("Helvetica", 16, "bold"),
        bg=COLORS["bg"],
    ).pack(fill="x", pady=10)

    for block_title, questions in PROGNOSE_MODEL_DATA.items():
        tk.Label(
            content,
            text=block_title,
            font=("Helvetica", 12, "bold"),
            bg=COLORS["accent"],
            anchor="w",
            padx=5,
            pady=5,
        ).pack(fill="x", pady=(10, 5))

        for q in questions:
            frame = tk.Frame(content, bg=COLORS["bg"], bd=1, relief=tk.RIDGE)
            frame.pack(fill="x", pady=3)

            tk.Label(
                frame,
                text=q["vraag"],
                font=("Helvetica", 10, "bold"),
                wraplength=450,
                bg=COLORS["bg"],
                anchor="w",
            ).pack(fill="x", padx=10, pady=5)

            var = tk.StringVar()
            variables[q["id"]] = var

            for text, weight in q["opties"].items():
                tk.Radiobutton(
                    frame,
                    text=f"{text} ({weight:.2f})",
                    variable=var,
                    value=text,
                    bg=COLORS["bg"],
                    anchor="w",
                ).pack(fill="x", padx=20)

    # Resultaatweergave
    result_label = tk.Label(right, font=("Helvetica", 16, "bold"), bg=COLORS["bg"])
    description_label = tk.Label(right, wraplength=300, justify=tk.LEFT, bg=COLORS["bg"])

    def on_calculate():
        score, missing = calculate_results(variables)

        if missing:
            result_label.config(text=f"{missing} vragen niet ingevuld", fg="#DC143C")
            description_label.config(
                text="Alle vragen moeten beantwoord zijn voor een geldige prognose."
            )
            return

        level, text, color, pct = get_risk_level(score)
        result_label.config(text=f"{pct:.1f}% – {level}", fg=color)
        description_label.config(text=text)

    tk.Button(
        right,
        text="Bereken Risicoscore",
        command=on_calculate,
        bg=COLORS["button_bg"],
        fg=COLORS["button_fg"],
        font=("Helvetica", 12, "bold"),
    ).pack(fill="x", pady=10)

    result_label.pack(fill="x", pady=10)
    description_label.pack(fill="x")


# STANDALONE GEBRUIK

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prognosemodel Re-integratiekansen")
    build_prognose_page(root)
    root.mainloop()
