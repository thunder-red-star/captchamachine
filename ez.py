# Import opencv, tessaract to read the captcha and bust it
import cv2
import pytesseract
import numpy as np
import os

# If platform = windows, set the path to tesseract.exe
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Else, assume linux
else:
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Read the image
img = cv2.imread('captcha/captcha4.png')

# This sequence of commands removes noise (dots and lines) from the captcha and makes it easier to read for tesseract. The final image is a sequence of letters (black on white background) without dots or lines.
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Resize 3x
img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
img = cv2.medianBlur(img, 1)
img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# Smooth the image to make the letters more readable
img = cv2.GaussianBlur(img, (5, 5), 0)
    
# Flip the color of the image
img = cv2.bitwise_not(img)

cv2.imwrite('captcha/captcha1_copy.png', img)

# Read the text
text = pytesseract.image_to_string(img, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ load_system_dawg 0 load_freq_dawg 0')

# Replace common OCR errors
text = text.replace('6', 'B')
text = text.replace('0', 'O')
text = text.replace('8', 'B')
text = text.replace('1', 'I')
text = text.replace('5', 'S')
text = text.replace('2', 'Z')
text = text.replace('4', 'A')
text = text.replace('3', 'E')
text = text.replace('9', 'G')

# Remove any characters not in A-Z
text = ''.join([c for c in text if c.isalpha()])
text = text.upper()

# Output
print(text)
