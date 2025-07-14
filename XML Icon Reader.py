import os
import sys
import xml.etree.ElementTree as ET
import cairosvg

def xml_to_svg(xml_path, svg_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        if root.tag != 'vector':
            print("❌ Not a valid vector drawable XML.")
            return

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

        print(f"✅ SVG saved at: {svg_path}")
        return svg_path

    except Exception as e:
        print(f"❌ Error: {e}")

def convert_svg_to_png(svg_path, png_path, output_size=512):
    try:
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=output_size, output_height=output_size)
        print(f"✅ PNG saved at: {png_path}")
    except Exception as e:
        print(f"❌ PNG Conversion Error: {e}")

# 🔄 Input and output
xml_file = "icon.xml"         # ← Your input file
svg_file = "icon_output.svg"
png_file = "icon_output.png"

# 🧾 Convert XML → SVG → PNG
svg_path = xml_to_svg(xml_file, svg_file)
if svg_path:
    convert_svg_to_png(svg_file, png_file)