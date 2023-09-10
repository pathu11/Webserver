# Custom Web Server README

This repository contains a simple custom web server programmed in Python.

## Project Overview

- **Server Language**: Python
- **Listening Port**: 2728
- **Supports PHP**: Yes

## Prerequisites

Before you can run the web server, ensure that you have the following prerequisites installed on your system:

- Python 3.x (for running the server)
- PHP (if you plan to serve PHP files)

## Getting Started

1. **Download**:  download this project repository to your local machine.

2. **Web Content Directory**: Ensure that your web content (HTML, PHP, etc.) is placed in the `htdocs` directory within the project. You can organize your web pages into subdirectories as needed.

3. **PHP Installation**: This zip file also includes the `php` folder, which contains the PHP runtime environment. The server is configured to use this installed PHP folder for serving PHP files.

4. **Server Configuration (Optional)**: If you want to customize the server configuration (e.g., change the listening port), you can do so by modifying the `server.py` source code.

## Running the Web Server

1. **Start the Server**:
   - Open a terminal or command prompt.
   - Navigate to the project directory where the `server.py` file is located.

2. **Run the Server**:
   - Execute the following command to start the web server:

     ```bash
     python server.py
     ```

3. **Access Web Pages**:
   - Open your web browser and type `http://localhost:2728` in the address bar.
   - The server will serve the `index.php` file by default when you access `http://localhost:2728/`. You can navigate to other pages within the `htdocs` directory as well.

## Stopping the Server

- To stop the server, press `Ctrl+C` in the terminal or command prompt where the server is running.

## Customizing the Server

- You can customize the web content by adding or modifying files in the `htdocs` directory. Additionally, you can adjust server settings within the `server.py` file.

