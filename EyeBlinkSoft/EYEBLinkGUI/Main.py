import cv2 as cv
import numpy as np

# Create a blank image to represent the keyboard with a white background
keyboard = np.full((1000, 1500, 3), (255, 255, 255), dtype=np.uint8)

# Function to add heading to the center (without background color)
def add_heading(text):
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5  # Reduced font size for smaller text
    font_thickness = 3  # Reduced thickness for smaller text
    text_color = (0, 255, 0)  # Green text

    # Get text size
    text_size = cv.getTextSize(text, font, font_scale, font_thickness)[0]
    text_width = text_size[0]
    text_height = text_size[1]

    # Calculate the x and y coordinates to center the text
    text_x = (keyboard.shape[1] - text_width) // 2
    text_y = text_height + 20  # Some padding from the top (e.g., 20 pixels)

    # Put the text on the image (no background color this time)
    cv.putText(keyboard, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

# Define the function to create keys and add an image with a green border
def letter(x, y, icon_path, text_label):
    width = 160  # Key width
    height = 160  # Key height
    border = 1
    text_color = (255,0,0)  # Blue text for visibility

    # Draw the key (rectangle) with a blue border
    cv.rectangle(keyboard, (x + border, y + border), (x + width - border, y + height - border), (255, 0, 0), border)

    # Load the image (icon) and resize it to fit the key
    icon = cv.imread(icon_path)
    if icon is None:
        print(f"Error: Image {icon_path} not found.")
        return

    icon_resized = cv.resize(icon, (width, height))

    # Convert icon to grayscale and create a mask for blending
    icon_gray = cv.cvtColor(icon_resized, cv.COLOR_BGR2GRAY)
    _, mask = cv.threshold(icon_gray, 1, 255, cv.THRESH_BINARY)
    mask_inv = cv.bitwise_not(mask)

    # Define the region of interest (ROI) on the keyboard where the icon will be placed
    roi = keyboard[y:y + height, x:x + width]

    # Create the background and foreground for blending
    keyboard_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
    icon_fg = cv.bitwise_and(icon_resized, icon_resized, mask=mask)

    # Add the icon to the region of interest
    dst = cv.add(keyboard_bg, icon_fg)
    keyboard[y:y + height, x:x + width] = dst

    # Draw a green border around the icon
    cv.rectangle(keyboard, (x, y), (x + width, y + height), (0, 255, 0), 1)  # Green border

    # Add the text label above the key
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    font_thickness = 2
    text_size = cv.getTextSize(text_label, font, font_scale, font_thickness)[0]
    text_width = text_size[0]
    text_height = text_size[1]

    text_x = x + (width - text_width) // 2
    text_y = y - 10  # Position text above the key with some padding

    cv.putText(keyboard, text_label, (text_x, text_y), font, font_scale, text_color, font_thickness)

# Add smaller heading to the center of the GUI (without background)
add_heading("Eye Blink System")

# Example of calling the letter function with text labels
letter(100, 200, 'images/eat.jpg', 'Eat')
letter(300, 200, 'images/water.jpg', 'Water')
letter(500, 200, 'images/Toilet.jpg', 'Toilet')
letter(700, 200, 'images/write.jpg', 'Message')
letter(900, 200, 'images/Mytv.jpg', 'Watch TV')
letter(1100,200, 'images/music.jpg', 'Music')
letter(100, 450, 'images/call.jpg', 'Call')
letter(300, 450, 'images/dress.jpg', 'Dressing')
letter(500, 450, 'images/Gson.jpg', 'Grandchild')
letter(700, 450, 'images/book.jpg', 'Reading Book')
letter(900, 450, 'images/emer.jpg', 'Emergency')
letter(1100, 450, 'images/exit.png', 'Close App')

# Display the keyboard image
cv.imshow("EyeBlinkSoFtware", keyboard)
cv.waitKey(0)
cv.destroyAllWindows()
