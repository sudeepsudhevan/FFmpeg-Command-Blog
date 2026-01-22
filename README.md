# FFmpeg Hub

A modern, community-driven platform for sharing and discovering useful FFmpeg commands. Built with Django and styled with a premium "Dark Glassmorphism" aesthetic.

## Features

-   **Command Library**: Browse a collection of FFmpeg commands with explanations.
-   **User Accounts**: Register and login to contribute.
-   **Add Commands**: Users can share their own useful scripts.
-   **Edit/Suggest**: 
    -   **Authors** can edit their own commands directly.
    -   **Community** can suggest edits to any command (Pull Request style).
-   **Review System**: Authors can approve or reject edit suggestions.
-   **Contributor Recognition**: Contributors are listed on the command detail page.
-   **Dashboard**: Manage your commands and suggestions in one place.
-   **Search**: Filter commands by title or code.
-   **Copy to Clipboard**: One-click copy for easy usage.
-   **Premium UI**: Fully responsive, dark-themed glassmorphism interface.

## Installation & Setup

### Prerequisites

-   Python 3.8+
-   pip

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd ffmpeg_hub
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    
    # Windows
    .\venv\Scripts\activate
    
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is missing, install manually: `pip install django python-dotenv`)*

4.  **Environment Configuration:**
    Create a `.env` file in the project root (next to `manage.py`):
    ```ini
    SECRET_KEY=your_secret_key_here
    DEBUG=True
    ```
    *A sample `.gitignore` is provided to exclude this file.*

5.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```
    Access the app at `http://127.0.0.1:8000/`.

## Usage Guide

### 1. Adding a Command
-   Navigate to **"Add Command"** in the navigation bar.
-   Fill in the **Title** (e.g., "Extract Audio from Video").
-   Paste the **Command** code.
-   Provide a helpful **Explanation** of what the flags do.
-   Click **Save**.

### 2. Editing Your Command
-   Go to the detail page of a command you created.
-   Click the **"Edit Command"** button (next to the title).
-   Update the details and save.

### 3. Suggesting an Edit
-   View a command created by someone else.
-   Click **"Suggest Edit"**.
-   Modify the command or explanation with your improvements.
-   Submit the suggestion.
-   The author will receive a notification in their **Dashboard**.

### 4. Reviewing Suggestions
-   Go to your **Dashboard**.
-   Look for "Pending Reviews".
-   Click **Review** to see a side-by-side comparison of the Current vs. Suggested version.
-   **Approve**: The command is updated immediately.
-   **Reject**: The suggestion is discarded.

### 5. Contributors
-   When a suggestion is approved, the suggester is added to the **"Contributors"** sidebar on the command page.

## Project Structure

-   `ffmpeg_blog/`: Project settings and configuration.
-   `commands/`: Main application app.
    -   `models.py`: Database definitions (`Command`, `EditRequest`).
    -   `views.py`: Logic for handling requests.
    -   `templates/`: HTML files using Django Template Language.
-   `.env`: Environment variables (Secret).
-   `.gitignore`: Files to exclude from Git.
