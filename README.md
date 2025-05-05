# Fusion Tag Renderer

A simple, intuitive web app for testing and previewing [Fusion](https://www.notion.so/Fusion-App-1d5759d6b003805890e9e51963279fd7) tag JSON files by applying regex-based tags to lists of file names, ranking them according to your tag priorities.

---

## Table of Contents

* [Overview](#overview)

* [Features](#features)

* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Running Locally](#running-locally)

* [Usage](#usage)

  * [Uploading a JSON Tag File](#uploading-a-json-tag-file)
  * [Entering File Names](#entering-file-names)
  * [Applying Tags & Viewing Results](#applying-tags-and-viewing-results)

* [JSON Format](#json-format)

* [Deployment](#deployment)

* [Contributing](#contributing)

* [License](#license)

* [Contact](#contact)

---

## Overview

**Fusion Tag Renderer** is a lightweight web application designed to help you **test**, **preview**, and **validate** the Fusion tag JSON files used by the Fusion Apple TV & iOS media-browser app. Simply upload a JSON file in the format your Fusion app expects, supply a list of candidate file names (or enter them manually), and the app will:

1. Parse all defined tags and their embedded regex patterns.
2. Apply each tag to every file name, one at a time.
3. Rank and display the files according to your tag priorities (earlier tags = higher value).

This makes it dead easy to spot misconfigured regexes, experiment with tag orderings, and quickly identify the “best” file out of a large batch.

---

## Features

* **Drag-and-drop JSON upload** for your Fusion tag definitions.
* **Inline tag listing** so you can instantly see which tags you’re testing.
* **Batch file-name import** via file upload or manual entry (one name per line).
* **Click-to-apply**: hit the Tag button and watch the app do its magic.
* **Automatic ranking**: files are sorted by how many and how highly they match your tags.
* **Zero setup**—hosted live on Render (no local install required), or run locally if you prefer.

---

## Getting Started

### Prerequisites

* **Python 3.8+**
* **pip** (usually bundled with Python)
* *(Optional)* A modern browser (Chrome, Safari, Firefox)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/hmcneill46/Fusion-Tag-Renderer.git
   cd Fusion-Tag-Renderer
   ```
2. **Create a virtual environment** (strongly recommended)

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

```bash
python run.py
```

By default, the app will start on **[http://localhost:5000](http://localhost:5000)**. Open that in your browser and you’re off to the races.

---

## Usage

### Uploading a JSON Tag File

1. Click **“Choose JSON file”**.
2. Select your Fusion tag JSON (the same format your iOS/Apple TV app uses).
3. The sidebar will populate with all available tags and show their regex patterns.

### Entering File Names

* **Upload a plain-text file** with one file name per line (great for large batches).
* **Or paste/edit manually** in the text area (one per line) for quick tests.

### Applying Tags & Viewing Results

1. Hit the **“Tag”** button.
2. The app applies each regex to each file name in turn.
3. Results appear in a sortable table, ordered by tag priority (first tag = highest weight).
4. You can instantly see which files match which tags, and how they stack up overall.

---

## JSON Format

Your JSON should follow the schema the Fusion app expects, with a top-level `groups` array for organizing tags, and a `filters` array containing each tag definition.

```json
{
  "groups": [
    {
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "Group Name 1",
      "color": "#RRGGBB",
      "isExpanded": false
    },
    {
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "Group Name 2",
      "color": "#RRGGBB",
      "isExpanded": true
    }
    // … additional groups …
  ],
  "filters": [
    {
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "Filter Name 1",
      "pattern": "(?i)\bPlaceholder\b",
      "type": "filter",
      "isEnabled": true,
      "tagStyle": "filled",
      "tagColor": "#RRGGBB",
      "textColor": "#RRGGBB",
      "imageURL": "https://example.com/icon1.png",
      "groupId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    },
    {
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "Filter Name 2",
      "pattern": "(?i)\bAnotherPlaceholder\b",
      "type": "filter",
      "isEnabled": false,
      "tagStyle": "outlined",
      "tagColor": "#RRGGBB",
      "textColor": "#RRGGBB",
      "imageURL": "https://example.com/icon2.png",
      "groupId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
    // … additional filters …
  ]
}
```

* **groups**: array of objects for categorizing tags.
* **filters**: array of tag definitions with regex patterns and display settings.

Use this template to structure your Fusion tag JSON files.

---

## Deployment

This app is already live at [fusion-tag-renderer.onrender.com](https://fusion-tag-renderer.onrender.com). If you’d like to deploy your own copy:

1. **Render.com**

   * Create a new **Web Service**.
   * Link your GitHub repo.
   * Set the **Build Command** to `pip install -r requirements.txt`.
   * Set the **Start Command** to `gunicorn run:app` (or `python run.py`).

2. **Alternatives**

   * Heroku (just use the provided `Procfile`).
   * Any other Python-hosting platform.

---

## Contributing

1. **Fork** this repo.
2. **Branch** your feature (`git checkout -b feature/X`).
3. **Commit** your changes (`git commit -m 'Add some feature'`).
4. **Push** to the branch (`git push origin feature/X`).
5. **Open** a Pull Request—describe what you’ve changed and why.

I’m happy to review bug-fixes, enhancements, or fresh ideas for data visualisations and extra filters.

---

## License

This project is released under the [MIT License](LICENSE).

---

## Contact

Created by Harry McNeill

– GitHub: [hmcneill46](https://github.com/hmcneill46)

– Website: [fusion-tag-renderer.onrender.com](https://fusion-tag-renderer.onrender.com)

Feel free to reach out if you spot any issues or have suggestions!
