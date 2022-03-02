import urllib.request
from PIL import Image, ImageChops
import io
import requests
import fitz

def fotos_download(name_file:str, list_url:list):
    """
    Read a list of fotos pdf and append all in unique file and save it
    """
    file = open(f"{name_file}.pdf", 'wb')
    for r in list_url:
        response = urllib.request.urlopen(r)
        file.write(response.read())
    file.close()

def trim(im):
    """
    Croft a image and remove the white spaces
    """
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def get_concat_v_blank(im1, im2, color=(0, 0, 0)):

    """
    Append on vertical size
    """

    dst = Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def get_concat_h_blank(im1, im2, color=(0, 0, 0)):
    """
    Concat the images in row
    """
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_h_multi_blank(im_list):
    """
    Take multi images and append all
    """
    _im = im_list.pop(0)
    for im in im_list:
        _im = get_concat_h_blank(_im, im)
    return _im



#open the fitz file
def imageBytes(path_fotos_pdf:str):
    """
    Load image and transform it on bytes and resize these
    """
    pdf = fitz.open(path_fotos_pdf)
    image_bytes = []
    for page_index in range(len(pdf)):
        # get the page itself
        page = pdf[page_index]
        for image_index, img in enumerate(page.get_images(), start=1):
            
            # get the XREF of the image
            xref = img[0]
            
            # extract the image bytes
            base_image = pdf.extract_image(xref)
            image_bytes.extend([base_image["image"]])
    new_im_en = []
    # Resize image
    for img_t in image_bytes:
        g = Image.open(io.BytesIO(img_t))
        new_im = trim(g.resize((400,400)))
        new_im_en.extend([new_im])
    if len(new_im_en>4):
        new_image_concat = get_concat_h_multi_blank(new_im_en[:4])
        new_image_concat_row = get_concat_h_multi_blank(new_im_en[4:])
        newMerge = get_concat_v_blank(new_image_concat,new_image_concat_row)
    else:
        newMerge = get_concat_h_multi_blank(new_im_en)

    return newMerge