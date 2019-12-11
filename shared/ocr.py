import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageFilter
from pytesseract import image_to_string


# requires:
# pip install seaborn pytesseract
# brew install tesseract
def ocr(image, blur=5):
    image = add_white_border(image)
    im = render_image(image)
    im.show()
    im = im.filter(ImageFilter.GaussianBlur(blur))
    im.show()
    message = image_to_string(im, config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return message


def add_white_border(image):
    image = [
        [0, *line, 0]
        for line in image
    ]
    wide = len(image[0])
    image = [[0] * wide] + image + [[0] * wide]
    return image


def render_image(image):
    sns.heatmap(image, cbar=False, yticklabels=False, xticklabels=False)
    plt.axis('equal')
    plt.savefig('temp.png', format='png')
    return Image.open('temp.png')
