import socket
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import io
import pyautogui
import os
import random


HOST = '127.0.0.1'
PORT = 65432

last_x, last_y = None, None
pen_color = "black"  # Default pen color

def send_data(sock, data, data_type="DRAW"):
    if data_type == "IMAGE":
        # Sending image data with a header
        sock.sendall(b'IMG' + len(data).to_bytes(4, 'big') + data)
    elif data_type == "CLEAR":
        # Sending clear command
        sock.sendall(b'CLR')
    else:
        # Sending drawing data
        sock.sendall(json.dumps(data).encode())

def receive_data(sock, canvas):
    while True:
        try:
            header = sock.recv(3)
            if header:
                if header == b'IMG':
                    # Receive image data
                    length = int.from_bytes(sock.recv(4), 'big')
                    img_data = b''
                    while length > 0:
                        chunk = sock.recv(min(length, 2048))
                        img_data += chunk
                        length -= len(chunk)
                    # Display the image
                    img = Image.open(io.BytesIO(img_data))
                    img.thumbnail((1000, 850))
                    img_tk = ImageTk.PhotoImage(img)
                    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
                    canvas.img_tk = img_tk  # Keep a reference to avoid garbage collection
                elif header == b'CLR':
                    # Clear the canvas
                    canvas.delete("all")
                else:
                    # Receive drawing data
                    data = header + sock.recv(1021)  # 1024 - header length
                    drawing_data = json.loads(data.decode())
                    canvas.create_line(drawing_data['x1'], drawing_data['y1'], drawing_data['x2'], drawing_data['y2'], fill=drawing_data['color'], width=2)
        except:
            break

def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def draw(event, sock, canvas):
    global last_x, last_y
    canvas.create_line(last_x, last_y, event.x, event.y, fill=pen_color, width=2)
    send_data(sock, {'x1': last_x, 'y1': last_y, 'x2': event.x, 'y2': event.y, 'color': pen_color})
    last_x, last_y = event.x, event.y

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        with open(file_path, 'rb') as file:
            img_data = file.read()
        # Display the image on the local canvas
        img = Image.open(file_path)
        img.thumbnail((1000, 850))
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.img_tk = img_tk  # Keep a reference to avoid garbage collection
        
        # Send the image data to the server for broadcasting
        send_data(sock, img_data, data_type="IMAGE")

def set_pen_color(color):
    global pen_color
    pen_color = color

def clear_canvas():
    canvas.delete("all")
    send_data(sock, None, data_type="CLEAR")  # Send clear command to the server

def save_ss():
    x=random.randint(10,100000000)
    y=str(x)
    # Get the directory of the client file
    directory = os.path.dirname(__file__)
    # Define the path for the screenshot
    screenshot_path = os.path.join(directory, y+'.png')
    # Take a screenshot
    screenshot = pyautogui.screenshot(region=(root.winfo_rootx() + canvas.winfo_x(), root.winfo_rooty() + canvas.winfo_y(), canvas.winfo_width(), canvas.winfo_height()))
    # Save the screenshot
    screenshot.save(screenshot_path)
    print(f"Screenshot saved as {screenshot_path}")

def create_color_buttons(root):
    colors = ['red', 'green', 'blue', 'yellow', 'black', 'purple', 'orange', 'cyan']  # List of colors
    for i, color in enumerate(colors):
        btn = tk.Button(root, bg=color, width=2, height=1, command=lambda c=color: set_pen_color(c))
        btn.pack(pady=5)

pen_color = "blue"  # Default pen color to light blue

def main():
    global canvas, sock, root

    root = tk.Tk()
    root.title("CLIENT--2")

    # Set up the canvas (whiteboard) with a black background
    canvas = tk.Canvas(root, bg="black", width=630, height=600)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Set up the color buttons on the left side
    color_frame = tk.Frame(root)
    color_frame.pack(side=tk.LEFT, fill=tk.Y)

    create_color_buttons(color_frame)

    # Load the image for the "Add Image" button replacement
    img = Image.open("img.png")
    img = img.resize((100, 60), Image.Resampling.LANCZOS)  # Resize to match the button size
    img_tk = ImageTk.PhotoImage(img)

    # Create a label as a clickable image button for adding image
    img_btn = tk.Label(color_frame, image=img_tk, cursor="hand2")
    img_btn.img_tk = img_tk  # Keep a reference to avoid garbage collection
    img_btn.pack(side=tk.BOTTOM, pady=10)

    # Bind the image button to the open_image function
    img_btn.bind("<Button-1>", lambda e: open_image())

    # Load the image for the "Clear" button
    eraser_img = Image.open("eraser.png")
    eraser_img = eraser_img.resize((100, 50), Image.Resampling.LANCZOS)  # Resize to match the button size and make it a bit bigger
    eraser_img_tk = ImageTk.PhotoImage(eraser_img)

    # Create a label as a clickable image button for clearing canvas
    eraser_btn = tk.Label(color_frame, image=eraser_img_tk, cursor="hand2")
    eraser_btn.eraser_img_tk = eraser_img_tk  # Keep a reference to avoid garbage collection
    eraser_btn.pack(side=tk.BOTTOM, pady=20)

    # Bind the eraser image button to the clear_canvas function
    eraser_btn.bind("<Button-1>", lambda e: clear_canvas())

    # Add a Save button below the other buttons
    save_btn = tk.Button(color_frame, text="Save", width=10, height=2, command=save_ss)
    save_btn.pack(side=tk.BOTTOM, pady=20)

    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # Start a thread to receive data
    threading.Thread(target=receive_data, args=(sock, canvas), daemon=True).start()

    # Bind mouse events to the canvas
    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", lambda event: draw(event, sock, canvas))

    root.mainloop()
    sock.close()

if __name__ == "__main__":
    main()
