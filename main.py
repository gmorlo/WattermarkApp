import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFont, ImageDraw
import os


def choose_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if file_path:
        img_label.config(text=file_path)
        img = Image.open(file_path)

        max_width, max_height = 300, 200
        img.thumbnail((max_width, max_height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        img_display.config(image=img_tk, width=img.width, height=img.height)
        img_display.image = img_tk

        app.selected_image_path = file_path


def add_watermark():
    if not hasattr(app, 'selected_image_path'):
        messagebox.showerror("Error", "No image selected")
        return

    image_name = image_name_entry.get()
    if not image_name:
        messagebox.showerror("Error", "No image name entered")
        return

    save_folder = os.path.join(os.getcwd(), 'saved_images')
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    save_path = os.path.join(save_folder, f"{image_name}.png")

    img = Image.open(app.selected_image_path).convert("RGBA")

    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))

    font_path = "arial.ttf"

    text = watermark_name_entry.get()
    font_size = 100
    font = ImageFont.truetype(font_path, font_size)
    rotation_angle = 45

    for x in range(0, img.width, font_size * 3):
        for y in range(0, img.height, font_size * 3):
            text_img = Image.new('RGBA', (font_size * len(text), font_size), (255, 255, 255, 0))
            d_text = ImageDraw.Draw(text_img)
            d_text.text((0, 0), text, font=font, fill=(255, 255, 255, 128))

            rotated_text_img = text_img.rotate(rotation_angle, expand=1)

            txt.paste(rotated_text_img, (x, y), rotated_text_img)

    watermarked = Image.alpha_composite(img, txt)
    watermarked.save(save_path)

    messagebox.showinfo("Success", f"Image saved to {save_path}")


app = tk.Tk()
app.title("Image Watermarking App")

choose_img_button = tk.Button(app, text="Choose Image", command=choose_image)
choose_img_button.grid(row=0, column=0, padx=10, pady=10)

img_label = tk.Label(app, text="No image selected")
img_label.grid(row=0, column=1, padx=10, pady=10)

img_display = tk.Label(app, text="No image to display", width=60, height=10, bg='grey')
img_display.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

image_name_label = tk.Label(app, text="Enter Image Name:")
image_name_label.grid(row=2, column=0, padx=10, pady=10)

image_name_entry = tk.Entry(app)
image_name_entry.grid(row=2, column=1, padx=10, pady=10)

watermark_name_label = tk.Label(app, text="Enter Watermark Name:")
watermark_name_label.grid(row=3, column=0, padx=10, pady=10)

watermark_name_entry = tk.Entry(app)
watermark_name_entry.grid(row=3, column=1, padx=10, pady=10)

watermark_button = tk.Button(app, text="Add Watermark", command=add_watermark)
watermark_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

app.mainloop()
