import PIL
from PIL import Image

def pb_combineImages(background, image1, image2, image3, image4, offset1, offset2):
        # Do the resize
        image1 = image1.resize((246,246),PIL.Image.ANTIALIAS)
        image2 = image2.resize((246,246),PIL.Image.ANTIALIAS)
        image3 = image3.resize((246,246),PIL.Image.ANTIALIAS)
        image4 = image4.resize((246,246),PIL.Image.ANTIALIAS)
        # Do the merging
	background.paste(image1, (offset1,offset1))
        background.paste(image2, (offset2,offset1))
        background.paste(image3, (offset1,offset2))
        background.paste(image4, (offset2,offset2))
	return background

