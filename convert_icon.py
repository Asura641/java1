from PIL import Image
import os

input_png = "icon.png"
output_ico = "icon.ico"

if os.path.exists(input_png):
    try:
        img = Image.open(input_png)
        img.save(output_ico, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
        print(f"Successfully converted {input_png} to {output_ico}")
    except Exception as e:
        print(f"Error converting image: {e}")
else:
    print(f"Error: {input_png} not found.")