# career_anchors.py
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass
from collections import Counter

# -------------------- Styles --------------------
S = {
    "bg": "#ffffff",
    "row1": "#eeeeee",
    "row2": "#e0e0e0",
    "header_dark": "#000000",
    "header": "#807C7D",
    "yellow": "#f1c40f",
    "box": "#f5f5f5",
    "btn_on": "#4d4d4d",
    "f_title": ("Segoe UI", 14, "bold"),
    "f_sub": ("Segoe UI", 10),
    "f": ("Segoe UI", 10),
    "f_b": ("Segoe UI", 10, "bold"),
    "f_cell": ("Segoe UI", 11),
    "f_cell_b": ("Segoe UI", 11, "bold"),
}

ANCHOR_COLS = [
    ("Omhoog | V", "V"),
    ("Veilig | W", "W"),
    ("Vrij | X", "X"),
    ("Balans | Y", "Y"),
    ("Uitdaging | Z", "Z"),
]

# -------------------- Data --------------------
@dataclass(frozen=True)
class Statement:
    q: int
    anchor: str
    text: str


_RAW_STATEMENTS = r'''
1|V|Graag wil ik het voor mezelf en voor anderen dusdanig regelen dat succes verzekerd is.
1|X|Ik houd me binnen een werksituatie het liefst bezig met mijn eigen zaken.
2|Y|Binnen het werk moet er tijd zijn voor zaken die jezelf belangrijk vindt en moet er gelegenheid zijn om zinvolle relaties te cultiveren.
2|V|Vooruitkomen is voor mij belangrijker dan persoonlijke behoeften.
3|W|Ik werk graag in een omgeving waar hard werken, loyaliteit en toewijding gewaardeerd wordt.
3|X|Ik houd van een werksituatie waar ik mijn eigen doelen kan stellen en ze kan bereiken op mijn eigen manier en op mijn eigen tempo.
4|V|Ik ben strijdlustig, kan goed analyseren en met mensen omgaan.
4|Y|Ik kan goed mijn evenwicht bewaren tussen de eisen van mijn werk en die van mijn privé-leven.
5|X|Ik wil onafhankelijk werken.
5|W|Ik houd ervan me een vertegenwoordiger te voelen van een groter geheel.
6|Z|Ik houd ervan als consultant of probleemoplosser te werken en me dusdanig te profileren door middel van een opwindend project.
6|V|Ik houd ervan in een situatie te werken waarin ik de leiding heb en verantwoordelijk ben voor het bereiken van bepaalde doelen.
7|Y|Mijn echtgenoot/partner is net zo belangrijk voor mij als mijn loopbaan.
7|Z|Mijn echtgenoot/partner verdwijnt naar de achtergrond als ik midden in een zeer opwindend project zit.
8|X|Het allerbelangrijkst voor mij is vrijheid.
8|Y|Het allerbelangrijkst voor mij is een doel in mijn leven.
9|W|Ik ben bekwaam, loyaal, betrouwbaar en ik werk hard.
9|Z|Ik ben sociaal en in de omgang, een goede leider en een goede organisator.
10|X|Ik ben onafhankelijk.
10|Y|Ik ben evenwichtig.
11|Z|Ik ben iemand die in actie komt door opwindende projecten.
11|Y|Ik ben iemand die graag met anderen werkt.
12|X|Ik ben ambitieus en iemand die graag met anderen wedijvert.
12|W|Ik ben iemand die een medewerker zijn met wie men kan rekenen.
13|Z|Ik voel zelfvertrouwen en ben in staat mezelf te redden.
13|V|Ik heb veel fantasie en enthousiasme.
14|W|Ik ben stabiel en vasthoudend.
14|X|Ik ben onafhankelijk en in staat een eigen koers te bepalen.
15|Y|Ik ben iemand die goed kan plannen en coördineren.
15|Z|Ik ben iemand die situaties analyseert en creatieve, nieuwe oplossingen ontwikkelt.
16|V|Ik ben een expert op mijn terrein.
16|W|Ik ben een betrouwbare en degelijk persoon.
17|Y|Ik ben iemand die wil werken volgens vaststaande procedures.
17|X|Ik ben iemand die probeert de doelen in het werk in overeenstemming te brengen met het persoonlijk nastreven.
18|Z|Een persoonlijk doel is om mijn eigen lot te bepalen.
18|Y|Een persoonlijk doel is om mijn werk te verweven met mijn privé-leven.
19|W|Ik vind het belangrijk een veilige baan te hebben en het gevoel te hebben erbij te horen.
19|X|Ik vind het belangrijk om tijd te kunnen besteden aan mijn privé-leven en hobby’s.
20|V|Ik geef de voorkeur aan een carrière waarin veel promotiekansen voorhanden zijn.
20|Z|Ik geef de voorkeur aan om in staat gesteld te worden uitdagende problemen en taken aan te pakken.
21|Y|Ik ben graag in een werksituatie waar invloed uitgeoefend kan worden.
21|W|Ik waardeer een baan waar je langere tijd kunt blijven werken en waar je gewaardeerd en geaccepteerd wordt.
22|V|Ik denk dat de juiste mensen en goede vrienden maken belangrijk is om vooruit te komen.
22|Z|Ik denk dat het essentieel is om interessesgebieden te ontwikkelen.
23|Y|Voor mij geldt als basis het scheppen van een evenwicht tussen mijn privé-leven en mijn werk.
23|W|Voor mij geldt als basis stabiliteit, waardering en een veilige plaats binnen mijn werksituatie.
24|X|Ik denk dat ik graag een positie zou willen hebben met een maximum aan zelfstandigheid.
24|V|Ik denk dat ik graag tot "de kring van ingewijden" zou willen behoren.
25|W|Voor mij geldt als basis stabiliteit, waardering en een veilige plaats op het werk.
25|V|Als basis geldt voor mij dat ik vooruit wil komen in de werkomgeving.
26|V|Ik denk dat geld, macht en aanzien een belangrijke maatstaf zijn van een succesvolle loopbaan.
26|Y|Ik denk dat een loopbaan succesvol is als je evenveel tijd hebt voor het werk, het gezin en je eigen ontwikkeling.
27|Z|Ik wil liever uitblinken op mijn gebied.
27|W|Ik wil liever beschouwd worden als betrouwbaar en loyaal.
28|W|Ik geef de voorkeur aan het werken met een team op lange termijn en een hechte basis.
28|Z|Ik geef de voorkeur aan het werken met een taakgerichte of projectgroep op korte termijn basis en in een hoog tempo.
29|Z|Ik geef de voorkeur aan professionele ontwikkeling en permanente training.
29|X|Ik geef de voorkeur aan professionele ontwikkeling om een expert te worden en om meer flexibiliteit en onafhankelijkheid te verkrijgen.
30|Y|Ik geef de voorkeur aan een werksituatie die een evenwicht garandeert tussen mijn privé-leven en mijn werk.
30|Z|Ik geef de voorkeur aan een werksituatie die opwindend is en mij stimuleert.
'''.strip()

CAREER_STATEMENTS: list[Statement] = [
    Statement(int(q), a, t)
    for q, a, t in (line.split("|", 2) for line in _RAW_STATEMENTS.splitlines() if line.strip())
]

CAREER_ANCHOR_STATEMENTS = {
    "Omhoog komen": "Deze op opwaartse mobiliteit gerichte loopbaanoriëntatie wordt gewoonlijk geassocieerd met het vooruitkomen in een hiërarchische en/of statusgevoelige organisatie. Het verwerven van steeds meer invloed speelt in deze kaders een grote rol. Prestige en beloning nemen bij iedere opwaartse beweging toe.",
    "Veilig voelen": "Sommige personen hebben behoefte aan een veilige baan in een duidelijke organisatie die vooral gekenmerkt wordt door orde en rust. Zij geven de voorkeur aan een lang en vast dienstverband, erkenning en appreciatie door de werkgever. In ruil daarvoor bieden ze een loyale en toegewijde instelling en zijn ze niet bang om hard te werken. Onderling respect, wederkerigheid en loyaliteit karakteriseren de werkhouding.",
    "Vrij zijn": "Personen met deze loopbaanoriëntatie zijn er op uit hun grenzen te verkennen. De nadruk ligt bij hen meer op het verwerven van persoonlijke autonomie, ruimte en verantwoordelijkheid voor het bereiken van resultaten dan op gebondenheid, zekerheid en vaste regels. Men is bereid zeer hard te werken als daar gunstige voorwaarden tegenover staan in de sfeer van onafhankelijkheid en zelfcontrole. Interessant werk is belangrijk maar individuele vrijheid is het uiteindelijke doel.",
    "Balans vinden": "Sommige mensen zoeken een optimaal evenwicht tussen werk, privé-leven en zelfontwikkeling. Het werk vormt voor hen slechts één dimensie van hun totale levensvervulling. De aandacht voor werk en privé-leven kan verschillen afhankelijk van de situatie.",
    "Uitdaging zoeken": "Deze loopbaanoriëntatie wordt gekenmerkt door de behoefte aan opwinding en uitdaging en een sterke betrokkenheid bij het werk. Autonomie is belangrijk maar het belangrijkste is opwindend en uitdagend werk.",
}

# -------------------- Helpers --------------------
def clear_frame(frame: tk.Widget) -> None:
    for w in frame.winfo_children():
        w.destroy()


def scrollable(parent: tk.Widget) -> tk.Frame:
    wrap = tk.Frame(parent, bg=S["bg"])
    wrap.pack(fill="both", expand=True)

    c = tk.Canvas(wrap, bg=S["bg"], highlightthickness=0)
    sb = tk.Scrollbar(wrap, orient="vertical", command=c.yview)
    c.configure(yscrollcommand=sb.set)

    c.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    inner = tk.Frame(c, bg=S["bg"])
    win = c.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>", lambda _e: c.configure(scrollregion=c.bbox("all")))
    c.bind("<Configure>", lambda e: c.itemconfig(win, width=e.width))

    def _on_wheel(e):
        c.yview_scroll(-int(e.delta / 120), "units")

    c.bind("<Enter>", lambda _e: c.bind_all("<MouseWheel>", _on_wheel))
    c.bind("<Leave>", lambda _e: c.unbind_all("<MouseWheel>"))

    return inner


def desc_box(parent: tk.Widget, name: str, text: str) -> None:
    box = tk.Frame(parent, bg=S["box"], bd=1, relief="solid")
    box.pack(fill="x", pady=4)

    tk.Label(
        box, text=name, bg=S["yellow"], fg="black",
        font=S["f_b"], width=16, anchor="center", padx=4, pady=4
    ).pack(side="left", fill="y")

    tk.Label(
        box, text=text, bg=S["box"], fg="black", font=S["f"],
        justify="left", wraplength=650, anchor="w", padx=8, pady=6
    ).pack(side="left", fill="both", expand=True)


# -------------------- Result table (dynamic max) --------------------
def build_result_table(parent: tk.Widget, max_score: int):
    """Create score table and return updater(totals: Counter[str,int])."""
    outer = tk.Frame(parent, bg=S["bg"])
    outer.pack(fill="x", padx=20, pady=(10, 10))

    tk.Label(
        outer, text="Resultaten – score per loopbaananker",
        bg=S["bg"], fg="black", font=("Segoe UI", 11, "bold"), anchor="w"
    ).pack(fill="x", pady=(0, 6))

    table = tk.Frame(outer, bg=S["bg"])
    table.pack(fill="x")

    headers = ["Score", "Omschrijving"] + [t for t, _ in ANCHOR_COLS]
    for col, text in enumerate(headers):
        tk.Label(
            table, text=text,
            bg=S["header_dark"], fg="white",
            font=S["f_b"], padx=10,
            anchor="center"
        ).grid(row=0, column=col, sticky="nsew")

    table.grid_columnconfigure(0, weight=0, minsize=90)
    table.grid_columnconfigure(1, weight=1, minsize=400)
    for c in range(2, 7):
        table.grid_columnconfigure(c, weight=1, minsize=160)

    scores = list(range(max_score, -1, -1))
    marker: dict[tuple[int, str], tk.Label] = {}

    # 3 zones + 0 row
    third = max(1, max_score // 3)
    spans = {
        max_score: ("Sterk", third),
        max_score - third: ("Neutraal", third),
        max_score - 2 * third: ("Matig", third),
    }

    for i, sc in enumerate(scores, start=1):
        tk.Label(
            table, text=str(sc),
            bg=S["yellow"], fg="black",
            font=S["f_b"], padx=8, pady=2,
            anchor="center"
        ).grid(row=i, column=0, sticky="nsew")

        if sc in spans and sc != 0:
            txt, rs = spans[sc]
            tk.Label(
                table, text=txt,
                bg=S["bg"], fg="black",
                font=("Segoe UI", 10, "bold"),
                anchor="center", pady=2
            ).grid(row=i, column=1, rowspan=rs, sticky="nsew")
        elif sc == 0:
            tk.Label(table, text="", bg=S["bg"]).grid(row=i, column=1, sticky="nsew")

        for j, (_title, code) in enumerate(ANCHOR_COLS, start=2):
            lbl = tk.Label(
                table, text="",
                bg=S["bg"], fg="black",
                font=("Segoe UI", 12, "bold"),
                bd=1, relief="solid",
                padx=6, pady=2,
                anchor="center"
            )
            lbl.grid(row=i, column=j, sticky="nsew")
            marker[(sc, code)] = lbl

    def update(totals: Counter[str]):
        for lbl in marker.values():
            lbl.config(text="")

        for _title, code in ANCHOR_COLS:
            sc = int(totals.get(code, 0))
            sc = max(0, min(max_score, sc))
            marker[(sc, code)].config(text="X")

    return update


# -------------------- Page builder --------------------
def build_loopbaanankers_page(parent_frame: tk.Frame, navigate) -> None:
    clear_frame(parent_frame)
    inner = scrollable(parent_frame)

    tk.Label(
        inner,
        text="Fase 2.0 | Wat wil de cliënt? | Identificatie van de loopbaanwaarden",
        bg=S["bg"], fg="black", font=S["f_title"], anchor="w"
    ).pack(fill="x", padx=20, pady=(20, 2))

    tk.Label(
        inner,
        text=("Beoordeling van stelling a.h.v. onderstaande criteria:\n"
              "Met welke stelling kan cliënt zich het sterkst identificeren?"),
        bg=S["bg"], fg="black", font=S["f_sub"], anchor="w", justify="left"
    ).pack(fill="x", padx=20, pady=(0, 15))

    table = tk.Frame(inner, bg=S["bg"])
    table.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    for c in range(7):
        table.grid_columnconfigure(c, weight=0)
    table.grid_columnconfigure(1, weight=1)

    headers = [("Nummer", 0), ("Stelling", 1)] + [(t, 2 + i) for i, (t, _code) in enumerate(ANCHOR_COLS)]
    for text, col in headers:
        tk.Label(
            table, text=text, bg=S["header"], fg="white", font=S["f_b"],
            padx=10, anchor="w" if col <= 1 else "center"
        ).grid(row=0, column=col, sticky="nsew")

    questions = sorted({s.q for s in CAREER_STATEMENTS})
    max_score = len(questions)  # 30 (1 keuze per vraag)

    # 1 var per question: stores "row_id:CODE" (unique cell among both rows)
    q_vars: dict[int, tk.StringVar] = {q: tk.StringVar(value="") for q in questions}

    # for repainting
    q_to_rows: dict[int, list[int]] = {q: [] for q in questions}
    row_buttons: dict[int, dict[str, tk.Radiobutton]] = {}

    def refresh_question(q: int) -> None:
        sel = q_vars[q].get()
        for rid in q_to_rows[q]:
            for code, rb in row_buttons[rid].items():
                if sel == f"{rid}:{code}":
                    rb.config(text="1", font=S["f_cell_b"])
                else:
                    rb.config(text="", font=S["f_cell"])

    def select(q: int, rid: int, code: str) -> None:
        q_vars[q].set(f"{rid}:{code}")

    # counts for rowspan in "Nummer" column (2 rows per question)
    q_row_counts = Counter(s.q for s in CAREER_STATEMENTS)
    shown: set[int] = set()

    for rid, st in enumerate(CAREER_STATEMENTS, start=1):
        row_bg = S["row1"] if rid % 2 else S["row2"]

        # merged question number
        if st.q not in shown:
            tk.Label(
                table, text=str(st.q), width=4,
                bg=S["yellow"], fg="black",
                font=S["f_b"], anchor="c"
            ).grid(
                row=rid, column=0, rowspan=q_row_counts[st.q],
                padx=(10, 10), pady=2, sticky="nsw"
            )
            shown.add(st.q)

        # statement label (click on text => choose default anchor for this statement)
        stmt_label = tk.Label(
            table, text=st.text,
            bg=row_bg, fg="black",
            font=S["f"], anchor="w",
            justify="left", wraplength=700,
            padx=12, pady=6,
            cursor="hand2",
        )
        stmt_label.grid(row=rid, column=1, sticky="nsew", padx=(0, 10), pady=2)
        stmt_label.bind("<Button-1>", lambda _e, q=st.q, r=rid, code=st.anchor: select(q, r, code))

        q_to_rows[st.q].append(rid)
        row_buttons[rid] = {}

        # 5 clickable cells (any column)
        for i, (_title, code) in enumerate(ANCHOR_COLS):
            col = 2 + i
            cell = tk.Frame(table, bg=row_bg, bd=1, relief="solid", cursor="hand2")
            cell.grid(row=rid, column=col, padx=3, pady=2, sticky="nsew")

            # one variable per question => only 1 selection for both rows
            val = f"{rid}:{code}"
            rb = tk.Radiobutton(
                cell,
                variable=q_vars[st.q],
                value=val,
                indicatoron=False,
                text="",
                width=2,
                font=S["f_cell"],
                bg=row_bg,
                fg="black",
                activebackground=row_bg,
                activeforeground="black",
                selectcolor=row_bg,
                relief="flat",
                borderwidth=0,
                cursor="hand2",
            )
            rb.pack(expand=True, fill="both")
            row_buttons[rid][code] = rb

            # clicking anywhere in cell selects too
            cell.bind("<Button-1>", lambda _e, q=st.q, r=rid, c=code: select(q, r, c))

    # traces after UI created
    for q, var in q_vars.items():
        var.trace_add("write", lambda *_a, _q=q: refresh_question(_q))

    for q in questions:
        refresh_question(q)

    parent_frame.loopbaan_vars = q_vars  # for validation later

    # ---- descriptions ----
    desc = tk.Frame(inner, bg=S["bg"])
    desc.pack(fill="x", padx=20, pady=(20, 10))

    tk.Label(
        desc, text="Loopbaanankers – omschrijving",
        bg=S["bg"], fg="black",
        font=("Segoe UI", 11, "bold"),
        anchor="w"
    ).pack(fill="x", pady=(0, 5))

    for name, text in CAREER_ANCHOR_STATEMENTS.items():
        desc_box(desc, name, text)

    # ---- results ----
    result_updater = build_result_table(inner, max_score=max_score)

    def totals() -> Counter[str]:
        # count by CODE from "rid:CODE"
        t = Counter()
        for v in q_vars.values():
            s = v.get()
            if ":" in s:
                _rid, code = s.split(":", 1)
                t[code] += 1
        return t

    def update_results(*_a):
        t = totals()
        result_updater(t)
        parent_frame.loopbaan_scores = dict(t)

    for var in q_vars.values():
        var.trace_add("write", update_results)
    update_results()

    # ---- submit ----
    def on_submit() -> None:
        missing = [q for q, v in parent_frame.loopbaan_vars.items() if not v.get().strip()]
        if missing:
            messagebox.showwarning(
                "Onvolledige vragenlijst",
                f"Er zijn nog {len(missing)} vragen zonder keuze."
            )
            return

        # store structured results: per question -> (row_id, anchor)
        results = {}
        for q, v in q_vars.items():
            rid_s, code = v.get().split(":", 1)
            results[q] = {"row_id": int(rid_s), "anchor": code}

        parent_frame.loopbaan_results = results
        parent_frame.loopbaan_scores = dict(totals())
        navigate("phase2.1")

    btn_row = tk.Frame(inner, bg=S["bg"])
    btn_row.pack(fill="x", pady=(10, 20))

    tk.Button(
        btn_row, text="Opslaan en verder",
        bg=S["btn_on"], fg="white",
        font=("Segoe UI", 11, "bold"),
        padx=20, pady=5,
        command=on_submit
    ).pack(side="right", padx=30)


# ---- Optional: run standalone for testing ----
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Loopbaanankers (Career Anchors)")
    root.geometry("1400x800")

    host = tk.Frame(root, bg=S["bg"])
    host.pack(fill="both", expand=True)

    def navigate(page: str):
        messagebox.showinfo("Navigate", f"Go to: {page}")

    build_loopbaanankers_page(host, navigate)
    root.mainloop()
