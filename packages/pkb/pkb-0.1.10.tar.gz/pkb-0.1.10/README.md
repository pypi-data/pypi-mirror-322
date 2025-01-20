# Personal Knowledge Base (PKB)

A tool to organize your personal information using markdown files, folders, and search functionality.

![PKG](screenshot.png)

**Source Code:** [https://github.com/hyw208/pkb](https://github.com/hyw208/pkb)


## Prerequisites

- Python 3.12.7 or higher

## Installation

1.  **Create a Knowledge Base Directory:**
    Start by creating a directory for your knowledge base (e.g., `kb`) and navigate into it:

    ```bash
    mkdir kb && cd kb
    ```

2.  **Clone the PKB Repository:**
    Clone the PKB repository to get the necessary `content` folder, `static` folder and `.env` file:

    ```bash
    git clone https://github.com/hyw208/pkb.git
    ```

3.  **Copy Essential Files:**
    Copy the `content` folder and `.env` file into your knowledge base directory:

    ```bash
    cp -R ./pkb/content .
    cp -R ./pkb/static .
    cp ./pkb/.env .
    ```

4.  **Set Up a Virtual Environment:**
    Create and activate a virtual environment to manage dependencies:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

5.  **Install the PKB Library:**
    Install the `pkb` library using pip:

    ```bash
    pip install pkb
    ```

## Launching the PKB

You can launch the PKB using either of the following methods:

**Method 1: Using the `pkb.fast` Module**

```bash
python -m pkb.fast
```

**Method 2: Using `uvicorn`**

```bash
uvicorn pkb.fast:app
```

## Accessing the PKB

You can open a browser and access it using `http://0.0.0.0:8000` or `http://127.0.0.1:8000/` or `http://localhost:8000` 


## Customization

You can customize your PKB by modifying the `.env` file. After making changes, save the file and restart the PKB to apply them.

**Changing the Site Name**

To change the site name, modify the `WEBSITE_NAME` variable in the `.env` file:

```bash
WEBSITE_NAME="Your New Site Name"
```

**Changing Navigation Items**

To change the navigation items, modify the `HEADER_ITEMS` variable in the `.env` file. The values should correspond to the names of the markdown files in your `content` folder.

**Example:**

```bash
# From:
HEADER_ITEMS=home,services,contact,about,search

# To:
HEADER_ITEMS=home,"new file 1",new_file_2,search
```
**Note:** 

Make sure to create markdown files (e.g., `new file 1.md` and `new_file_2.md`) with some content under the `content` folder.

## What's Next?

Now that you have your PKB set up, you can:

Delete any files you don't need from the `content` folder.

Start creating your personal content using markdown files.

Have fun exploring and organizing your knowledge!