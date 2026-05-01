# AI News Meme Studio

AI News Meme Studio is a cutting-edge desktop application that transforms trending technology news into viral memes using advanced AI models. Built with **PySide6**, **Gemma 4**, and **Flux**, it provides a seamless workflow from news discovery to meme creation.

## 🚀 Features

-   **Trending News Feed**: Automatically scrapes and displays the latest technology news from Google News.
-   **AI News Analysis**: Uses **Gemma 4** to analyze headlines and generate clever, context-aware meme captions.
-   **High-Fidelity Image Generation**: Leverages the **Flux-based Z-Image** model to generate stunning visuals tailored to the news topic.
-   **Automated Compositing**: Overlays generated text onto images with professional typography and formatting.
-   **Custom Meme Generator**: Create your own memes from any topic using the same AI-powered engine.
-   **Meme Gallery**: Keep track of all your generated creations with local database persistence.

## 🛠️ Architecture

The project follows a modular 3-layer architecture:
-   **UI Layer**: PySide6 components and pages.
-   **Services Layer**: Business logic for AI generation, news scraping, and image processing.
-   **Repository Layer**: Data persistence for memes and metadata.

Detailed system documentation can be found in [Agent.md](./Agent.md).

## 📋 Prerequisites

-   **Python 3.12+**
-   **CUDA-compatible GPU** (Minimum 16GB VRAM recommended for optimal performance).
-   **UV** (Python package manager).

## ⚙️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/nishanth-kj/Automation.git
    cd Automation
    ```

2.  **Install dependencies**:
    ```bash
    uv pip install -r pyproject.toml
    ```

3.  **Download Models**:
    Place the required models in the `models/` directory:
    -   `gemma-4-E2B-it`
    -   `z_image_turbo_bf16`

4.  **Run the Application**:
    ```bash
    uv run main.py
    ```

## 📝 Configuration

-   **Fonts**: The application looks for `arial.ttf` in `assets/fonts/`. It will fallback to the system font if missing.
-   **Database**: Uses a local SQLite database (`memes.db`) initialized on first run.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


