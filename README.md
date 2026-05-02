# AI News Meme Studio

AI News Meme Studio is a cutting-edge platform that transforms trending technology news into viral memes using advanced AI models. It features a robust **FastAPI** backend, a high-performance **PySide6** desktop interface, and a modern **Next.js** web dashboard.

## 🚀 Features

-   **Trending News Feed**: Automatically scrapes the latest technology news from Google News, Reddit, Bing, and DuckDuckGo.
-   **AI News Analysis**: Uses **Gemma 4** to analyze headlines and generate clever, context-aware meme captions.
-   **High-Fidelity Image Generation**: Leverages the **Flux-based Z-Image** model to generate stunning visuals.
-   **RAG (Retrieval-Augmented Generation)**: Semantic search over news articles using vector embeddings.
-   **Dual Interface**: Access the studio via the **PySide6 Desktop App** or the **Next.js Web App**.
-   **Standardized API**: A clean hub with strict constants for status and errors.

## 🛠️ Architecture

The project follows a decoupled, service-oriented architecture:
-   **Frontend**: Next.js (Web) and PySide6 (Desktop).
-   **Backend**: FastAPI serving as the central controller hub.
-   **Controllers**: Modular API endpoints for News, Memes, RAG, and AI.
-   **Services**: Business logic for AI generation, news scraping, and image processing.
-   **Repository**: SQLAlchemy-based data persistence (SQLite) with semantic search support.
-   **Constants**: Specialized modules for `api_status`, `error_code`, `error_message`, and `status`.

## ⚙️ Installation & Running

1.  **Start the API Backend**:
    ```bash
    python run_api.py
    ```
2.  **Start the Web Interface**:
    ```bash
    cd web && npm run dev
    ```

## 📝 API Standards

The API uses a unified three-field response structure:
```json
{
  "status": 1,   // 1 for Success, 0 for Error (from api_status.py)
  "error": {
    "code": 200,   // Integer code (200 for Success, e.g., 404 for Not Found)
    "message": "Success", // Human readable (from error_message.py)
    "field": null // Optional validation field
  },
  "data": { ... } // Payload
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
