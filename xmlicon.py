import os
import xml.etree.ElementTree as ET
import cairosvg
import tkinter as tk
from tkinter import filedialog, messagebox

def xml_to_svg(xml_path, svg_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        if root.tag != 'vector':
            raise ValueError("Not a valid Android vector drawable XML.")

        width = root.attrib.get('android:width', '24dp').replace('dp', '')
        height = root.attrib.get('android:height', '24dp').replace('dp', '')
        viewport_width = root.attrib.get('android:viewportWidth', width)
        viewport_height = root.attrib.get('android:viewportHeight', height)

        svg_data = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {viewport_width} {viewport_height}">\n'

        for path in root.findall('path'):
            path_data = path.attrib.get('android:pathData')
            fill_color = path.attrib.get('android:fillColor', '#FFFFFF')
            svg_data += f'  <path d="{path_data}" fill="{fill_color}"/>\n'

        svg_data += '</svg>'

        with open(svg_path, 'w') as f:
            f.write(svg_data)

        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

def convert_svg_to_png(svg_path, png_path, output_size=512):
    try:
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=output_size, output_height=output_size)
        return True
    except Exception as e:
        messagebox.showerror("PNG Conversion Error", str(e))
        return False

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def convert():
    xml_file = entry_file.get()
    if not xml_file or not os.path.isfile(xml_file):
        messagebox.showwarning("Invalid File", "Please select a valid XML file.")
        return

    output_svg = os.path.splitext(xml_file)[0] + "_output.svg"
    output_png = os.path.splitext(xml_file)[0] + "_output.png"

    if xml_to_svg(xml_file, output_svg):
        if convert_svg_to_png(output_svg, output_png):
            messagebox.showinfo("Success", f"Files saved:\n\n{output_svg}\n{output_png}")

# 🔳 GUI Window Setup
app = tk.Tk()
app.title("XML to SVG/PNG Converter")
app.geometry("400x200")
app.resizable(False, False)
app.configure(bg="#1e1e1e")

title = tk.Label(app, text="🧩 XML to SVG/PNG Converter", font=("Segoe UI", 14), bg="#1e1e1e", fg="white")
title.pack(pady=10)

frame = tk.Frame(app, bg="#1e1e1e")
frame.pack(pady=10)

entry_file = tk.Entry(frame, width=35, font=("Segoe UI", 10))
entry_file.pack(side=tk.LEFT, padx=(0, 10))

btn_browse = tk.Button(frame, text="Browse", command=browse_file, bg="#444", fg="white", font=("Segoe UI", 10))
btn_browse.pack(side=tk.LEFT)

btn_convert = tk.Button(app, text="Convert to SVG + PNG", command=convert, bg="#d11a2a", fg="white", font=("Segoe UI", 11, "bold"))
btn_convert.pack(pady=20)

app.mainloop()