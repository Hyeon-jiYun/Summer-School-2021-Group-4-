## Text recognition
## Inspired from https://towardsdatascience.com/building-a-simple-text-recognizer-in-python-93e453ddb759
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'  # your path may be different

# assigning an image from the source path
img = Image.open("Immagine.jpg")
# converts the image to result and saves it into result variable
result = pytesseract.image_to_string(img)

print(result)