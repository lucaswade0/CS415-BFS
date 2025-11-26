CS 415 Project 3 - Pathfinding with BFS and Best-First Search

REQUIREMENTS
- Python 3
- Pillow library

!!! Pillow IS Already Installed On Blue !!!
(don't do below intsallation if running on blue)

INSTALLATION
Install Pillow by running:
  pip install Pillow

Or if using pip3:
  pip3 install Pillow

USAGE
Run the program:
  python main.py

Or if using python3:
  python3 main.py

The program will ask you for:
1. Input image file name (BMP format)
2. Start row and column
3. Destination row and column
4. Output file names for BFS and Best-First Search results

OUTPUT
The program creates two output images:
- BFS result: visited pixels in green, shortest path in red
- Best-First Search result: visited pixels in green, shortest path in red

Both algorithms find the shortest path, but Best-First Search typically visits fewer nodes.
