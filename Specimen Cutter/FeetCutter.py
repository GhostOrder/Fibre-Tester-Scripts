# import cv2
from PIL import Image, ImageFont, ImageDraw
# import svgwrite
# from svgwrite import cm, mm
import numpy as np
from datetime import datetime

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

def convertFromFormat(string):
    if not type(string)==str: return None
    if string == "": return None
    if string.upper() == "NONE": return None
    if string.upper() == "TRUE": return True
    if string.upper() == "FALSE": return False
    if string[0] == "\"" and string[-1] == "\"":
        string1 = string[1:-1]
        return string1
    if string[0] == "(" and string[-1] == ")":
        string1 = string[1:-1]
        out = tuple([convertFromFormat(i.strip()) for i in string1.split(",")])
        return out
    if string[0] == "[" and string[-1] == "]":
        string1 = string[1:-1]
        out = [convertFromFormat(i.strip()) for i in string1.split(",")]
        return out
    try:
        return float(string)
    except:
        pass
    return None
    

with open("properties.txt") as f:
    lines = f.readlines()

slines = [[slfrag.strip() for slfrag in line.split("=",1)] for line in lines]
for sline in slines:
    if len(sline) < 2: continue
    val0 = sline[0]
    val1 = convertFromFormat(sline[1])
    if val0 == "BATCH_STR":
        batch_str = val1
        continue 
    if val0 == "SAVE_PATH":
        if val1 == None:
            save_path = "."
        else:
            save_path = val1
        continue
    if val0 == "SAVE_FILENAME":
        if val1 == None:
            save_filename = ""
        else:
            save_filename = val1
        continue
    if val0 == "PIXELS_PER_CM": 
        ppc = val1
        continue
    if val0 == "FEET_DIMENSIONS_MM": 
        feet_dimensions = val1
        continue
    if val0 == "LIGAMENT_WIDTH_MM":
        ligament_width = val1
        continue
    if val0 == "GAUGE_LENGTH_MM":
        gauge_length = val1
        continue
    if val0 == "FONTSIZE_MM":
        fontsize = val1 
        continue 
    if val0 == "PAPER_SIZE_CM":
        paper_size = val1 
        continue 
    if val0 == "PAPER_MARGINS_MM":
        paper_margins = val1 
        continue
    if val0 == "SPACING_MM":
        spacing = val1 
        continue 
    if val0 == "GRIP_SIZE_MM":
        grip_size = val1
        continue
    if val0 == "SIDE_SLOT_MM":
        side_slot = val1
        continue
    if val0 == "FOLDABLE":
        foldable = val1 
        continue
    if val0 == "ORIENTATION":
        orientation = val1 
        continue
    


# ppc = 57 #pixels per cm
# feet_dimensions = (20,40) #(weight, height) [mm]
# ligament_width = 2.5 #mm
# gauge_length = 12.7 #mm
# fontsize = 2.5 #mm
# paper_size = (17.145,23.495) #cm #limited by Cricut
# paper_margins = 10 #mm
# spacing = 2 #mm
# grip_size = 10 #mm
# side_slot = 2.5 #mm
# foldable = False
# orientation = 0

# batch_str = None

# save_path = "D:/Msc. in Materials Engineering/Thesis/Cricut"
# save_filename = "Gauge_Length_B_NonFolding"

paper_dimensions_px = tuple(map(lambda x: int(x*ppc), paper_size))
feet_dimensions_px = tuple(map(lambda x: int(x*ppc/10),feet_dimensions))
ligament_width_px = int(ligament_width*ppc/10)
gauge_length_px = int(gauge_length*ppc/10)
grip_size_px = int(grip_size*ppc/10)
side_slot_px = int(side_slot*ppc/10)
feet_dimensions_rotated = feet_dimensions
if orientation:
    feet_dimensions_rotated = (feet_dimensions[1],feet_dimensions[0])
feet_array_size = tuple(np.array(
    (np.array(paper_size)*10-2*0.1*paper_margins+spacing)/(np.array(feet_dimensions_rotated)+spacing),dtype=int))
spacing_px = int(spacing*ppc/10)
feet_dimensions_rotated_px = tuple(map(lambda x: int(x*ppc/10),feet_dimensions_rotated))
if batch_str is None: batch_str = str(hex(int(datetime.today().timestamp())))[2:]
txt = lambda n: "{}-{:0>3d}\nPD{}\nL = {} mm\n".format(
    batch_str,
    n,
    datetime.today().strftime("%Y%m%d"),
    gauge_length)
fontsize_px = 14
txt2 = lambda n: "{}-{:0>3d}".format(batch_str,n)

fnt = ImageFont.truetype("arial.ttf", fontsize_px)
feet_array_img = Image.new("LA",paper_dimensions_px,(0,0))

score_img = Image.new("LA",feet_dimensions_px,(0,0))
score_coords = np.array([(int(feet_dimensions_px[0]/2),int(0.25*feet_dimensions_px[1])),
                         (int(feet_dimensions_px[0]/2),int(0.75*feet_dimensions_px[1]))])
score_img_draw = ImageDraw.Draw(score_img)
score_img_draw.line(score_coords)
score_array_img = Image.new("LA",paper_dimensions_px,(0,0))

n=0
for i in range(feet_array_size[0]):
    for j in range(feet_array_size[1]):
        n += 1
        _txt = txt(n)
        _txt2 = txt2(n)
        text_size = get_text_dimensions(_txt,fnt)
        text2_size = get_text_dimensions(_txt2,fnt)
        text_layer = Image.new("LA",feet_dimensions_px,(0,0))
        text_layer_draw = ImageDraw.Draw(text_layer)
        text_margin = int(ligament_width_px/2)
        text_layer_draw.text((int(feet_dimensions_px[0]/2),text_margin+text_size[1]),_txt,(0,255),font=fnt,anchor="ms",align="center")
        text_layer_draw.text((int(feet_dimensions_px[0]/2),feet_dimensions_px[1]-text_margin-text2_size[1]),_txt2,(0,255),font=fnt,anchor="ms",align="center")
        feet_img = Image.new("LA",feet_dimensions_px,(255,255))
        feet_img_draw = ImageDraw.Draw(feet_img)
        feet_img_draw.rectangle(
            ((ligament_width_px,int((feet_dimensions_px[1]-gauge_length_px)/2)),
              (feet_dimensions_px[0]-ligament_width_px,int((feet_dimensions_px[1]+gauge_length_px)/2))),
            fill=(0,0))
        feet_img_draw.rounded_rectangle(
            ((ligament_width_px,grip_size_px),
             (ligament_width_px+side_slot_px,feet_dimensions_px[1]-grip_size_px)),
            radius=int(ligament_width_px/2),
            fill=(0,0))
        feet_img_draw.rounded_rectangle(
            ((feet_dimensions_px[0]-ligament_width_px-side_slot_px,grip_size_px),
             (feet_dimensions_px[0]-ligament_width_px,feet_dimensions_px[1]-grip_size_px)),
            radius=int(ligament_width_px/2),
            fill=(0,0))
        feet_img.paste(text_layer,mask=text_layer.convert("RGBA"))
        if orientation:
            feet_img = feet_img.rotate(90,expand=1)
        feet_array_img.paste(feet_img,
                              ((feet_dimensions_rotated_px[0]+spacing_px)*i,(feet_dimensions_rotated_px[1]+spacing_px)*j),
                              mask=feet_img.convert("RGBA"))
        score_array_img.paste(score_img,
                              ((feet_dimensions_rotated_px[0]+spacing_px)*i,(feet_dimensions_rotated_px[1]+spacing_px)*j),
                              mask=score_img.convert("RGBA"))


feet_array_img.save(save_path+"/"+save_filename+".png")

background_margin = 1 #px
background_size_px = tuple(map(lambda x: x + 2*background_margin, paper_dimensions_px))
background = Image.new("LA",background_size_px,(100,255))
#background.paste(feet_array_img,(background_margin,background_margin),mask=feet_array_img.convert("RGBA"))
background.paste(score_array_img,(background_margin,background_margin),mask=feet_array_img.convert("RGBA"))
new_background = background.rotate(0,expand=1)
new_background.show()

