# How to Install Track-CLI

1. **Clone the github repository**

    ```bash
    git clone https://github.com/7FIl/Track-CLI.git


2.  **Navigate to your project root (`track-cli/`) in your terminal.**

    ```bash
    cd track-cli
    ```

3.  **Create a virtual environment (if you don't have one):**

    ```bash
    python -m venv .venv
    ```

4.  **Activate the virtual environment:**

    * **On Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    * **On Windows:**
        ```cmd
        .venv\Scripts\activate
        ```

5.  **Install your package in "editable" mode:**

    ```bash
    pip install -e .
    ```

    The `-e` (or `--editable`) flag is excellent for development. It means that `pip` installs a link to your project, so any changes you make to the Python files (`src/track/cli.py`) will be immediately reflected when you run the `track` command, without needing to reinstall.

6. Test Your Command

With your virtual environment active, you should now be able to run your `track` command directly!

```bash
track add "Learn Python packaging"
track add "Refactor old code"
track list
track status in-progress 1
track list in-progress
track delete 2
track list
```

This project is Made, inspired from https://roadmap.sh/projects/task-tracker
