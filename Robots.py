import sys
import requests
import keyboard
import os
import imgkit
from PIL import Image
from fpdf import FPDF

def path_traversal_info():
    print("""    
         __
 _(\    |@@|
(__/\__ \--/ __
   \___|----|  |   __
       \ }{ /\ )_ / _\
       /\__/\ \__O (__
      (--/\--)    \__/
      _)(  )(_
     `---''---`
    """)
    name = input('what name would you like to give to your directory\n')
    os.mkdir(name)
    os.chdir(name)
    pdf = FPDF()

    url = sys.argv[1]

    robots_url = url+'/robots.txt'

    website = requests.get(robots_url)

    page = website.text
    lines = page.splitlines()
    maybe=[]
    for line in lines:
        split = line.split(': ')[1]
        if split.startswith('/'):
            comb = (url + split)
            a = requests.get(comb)
            print(a.status_code, comb)
            change = split.replace("/", "_")
            maybe.append(change+'.png')
            try:
                imgkit.from_url(comb, change+'.png')
            except:
                print('nothing found')
                
    for image in maybe:
        cover = Image.open(image)
        width, height = cover.size
        width, height = float(width * 0.264583), float(height * 0.264583)
        pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
        orientation = 'P' if width < height else 'L'
        width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
        height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
        pdf.add_page(orientation=orientation)
        pdf.image(image, 0, 0, width, height)
    pdf.output("yourfile.pdf", "F")

path_traversal_info()
