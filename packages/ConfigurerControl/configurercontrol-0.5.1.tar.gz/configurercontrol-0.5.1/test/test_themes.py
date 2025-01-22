import tkinter as tk
import unittest
from ConfigurerControl.images import images, IconName, Icons, get_tk_image, ic
from PIL import Image, ImageFont, ImageDraw


class TestType(unittest.TestCase):

    def test_create_default(self):
        new_img = Image.new('RGB', (100, 100), 'white')
        font = ImageFont.load_default(size=50)
        pencil = ImageDraw.Draw(new_img)
        pencil.text((50, 50), '?', anchor="ms", font=font, fill='red')
        new_img.show()

    def test_Literal(self):
        lit = IconName
        print(lit)

    def test_tkImage(self):
        root = tk.Tk()
        icons: Icons = {n: get_tk_image(img) for n, img in images.items()}
        root.mainloop()
