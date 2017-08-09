import PIL
from PIL import Image

def pb_resizeAndMergeImages(background, sizeImages, spaceBetweenPhotos, spaceMargin, image1, image2, image3, image4):
        # Do the resize
        targetSizeBackground = pb_getSquarePixelResolution(sizeImages, spaceBetweenPhotos, spaceMargin)
        background = background.resize((targetSizeBackground,targetSizeBackground))
        
        targetSize = (sizeImages,sizeImages)
        image1 = image1.resize(targetSize)
        image2 = image2.resize(targetSize)
        image3 = image3.resize(targetSize)
        image4 = image4.resize(targetSize)

        # Do the merging
        return pb_mergeImages(background, image1, image2, image3, image4, spaceMargin, pb_getOffset2(sizeImages, spaceMargin, spaceBetweenPhotos))

def pb_mergeImages(background, image1, image2, image3, image4, offset1, offset2):
        # Do the merging
	background.paste(image1, (offset1,offset1))
        background.paste(image2, (offset2,offset1))
        background.paste(image3, (offset1,offset2))
        background.paste(image4, (offset2,offset2))
	return background

def pb_getSquarePixelResolution(imagesToCopyResolution, spaceBetweenPhotos, spaceMargin):
        return imagesToCopyResolution * 2 + spaceBetweenPhotos + spaceMargin * 2

def pb_getOffset2(imagesToCopyResolution, spaceBetweenPhotos, spaceMargin):
        return spaceMargin + imagesToCopyResolution + spaceBetweenPhotos