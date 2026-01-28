# LABOR Arbeidsmarktintegratie - Modular Program
LABOR's modular program is a local Python/Tkinter application designed to streamline assessments and generate prognosis reports. The application allows users to complete various assessments, automatically calculate scores, and produce a clear report with percentages, results, and conclusions. All data is stored locally within the file explorer.

## Technologies

### Core language
- Python

### UI framework
- Tkinter
- Custom UI component layer `ui_components.py`
- Centralized styling layer `ui_styles.py`

### Data processing
- Pandas

### File I/O (Input/Output)
- OpenPyXL
- xlrd

### Platform integration
- pywin32

### Media
- Pillow

## Getting started

### Prerequisites

Ensure that [Python](https://www.python.org/downloads/) is installed on your system.

### Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/FlyyLee/labor-project2026
    ```
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Start the application**
    ```bash
    python app.py
    ```
    The application will open in a new window.