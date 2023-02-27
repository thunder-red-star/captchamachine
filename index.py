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
img = cv2.imread('captcha/captcha3.png')

# This sequence of commands removes noise (dots and lines) from the captcha and makes it easier to read for tesseract. The final image is a sequence of letters (black on white background) without dots or lines.
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Resize 3x
img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
img = cv2.medianBlur(img, 21)
img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# Smooth the image to make the letters more readable
img = cv2.GaussianBlur(img, (5, 5), 0)

# create a copy with numpy format so we can do np.all(img[:, i] == 255) to check if the column is all white
numimg = np.array(img)

# Now we'll split the letters manually to make it easier for tesseract to read them. If a column is completely white, we'll assume that it's a space between letters.
# We'll store each bounding box in a list
boxes = []
reading = False
start = -1
end = -1
for i in range(img.shape[1]):
    # If column is completely white, we're not reading a letter
    if np.all(numimg[:, i] == 0) and reading:
        reading = False
        # If we were reading a letter, append the bounding box to the list
        if start != -1:
            boxes.append((start, i))
    # If column is not completely white, we're reading a letter
    else:
        # If we weren't reading a letter, start reading
        if not reading:
            reading = True
            start = i

# Remove bounding boxes that are one-pixel wide
toDelete = []
for box in boxes:
    # If the bounding box is one pixel wide, remove it
    if box[1] - box[0] == 1:
        toDelete.append(box)

# Remove the bounding boxes
for box in toDelete:
    boxes.remove(box)

text = ''

print(boxes)

im2 = img.copy()

# Loop through the contours
for letter in boxes:  
    # Draw rectangle
    cv2.rectangle(img, (letter[0], 0), (letter[1], img.shape[0]), (0, 255, 0), 2)

    # Crop the image
    roi = img[0:img.shape[0], letter[0]:letter[1]]

    # Flip the color of the image
    roi = cv2.bitwise_not(roi)

    # Print for debug
    print("The bounding box is: ", letter[0], letter[1])

    # Draw a red line that shows where the segmentation is
    cv2.line(im2, (letter[0], 0), (letter[0], img.shape[0]), (0, 0, 255), 2)

    # Save the image
    cv2.imwrite('captcha/captcha1_copy.png', im2)

    # Read the text
    text += pytesseract.image_to_string(roi, config='--psm 9 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

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
