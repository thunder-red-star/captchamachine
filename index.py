# Import opencv, tessaract to read the captcha and bust it
import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Read the image
img = cv2.imread('captcha/captcha1.png')

# Convert to black and white
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur the image
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Remove

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the image
im2 = img.copy()

# Save that image for debugging purposes
cv2.imwrite('captcha/captcha1_copy.png', thresh)

# Text variable
text = ''

# Loop through the contours
for cnt in contours:
    # Get bounding box
    x, y, w, h = cv2.boundingRect(cnt)

    # Draw rectangle
    cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Crop the image
    roi = thresh[y:y + h, x:x + w]

    # Read the text
    text += pytesseract.image_to_string(roi, config='--psm 10')

    # Print the text
    print(text)

# Output
# 5
# 3
# 4
# 2
# 1
