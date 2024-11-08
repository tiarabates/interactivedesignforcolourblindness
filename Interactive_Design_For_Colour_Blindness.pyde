# Global variables
original_img = None
color_blindness_img = None
buttons = []
active_button = None  # To track the currently active button
image_files = ["landscape.jpg", "nature.jpg", "cityscape.jpg"]  # Example list of images
current_image_index = 0  # Keep track of the current image being displayed

# Button class to create clickable buttons
class Button:
    def __init__(self, label, x, y, width, height, action):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.is_active = False
    
    def display(self):
        # Highlight the button if it is active
        if self.is_active:
            fill(150, 255, 150)  # Light green for active state
        elif self.is_hovered():
            fill(180)  # Darker gray when hovered
        else:
            fill(200)  # Normal button color
        
        rect(self.x, self.y, self.width, self.height)
        fill(0)
        textSize(12)
        textAlign(CENTER, CENTER)
        text(self.label, self.x + self.width / 2, self.y + self.height / 2)
    
    def is_pressed(self):
        return self.is_hovered()
    
    def is_hovered(self):
        return mouseX > self.x and mouseX < self.x + self.width and mouseY > self.y and mouseY < self.y + self.height

# Function to apply Deuteranopia filter (Green blindness)
def deuteranopia(img):
    img.loadPixels()
    for i in range(len(img.pixels)):
        r, g, b = red(img.pixels[i]), green(img.pixels[i]), blue(img.pixels[i])
        # Set green channel to 0 for Deuteranopia
        img.pixels[i] = color(r, 0, b)
    img.updatePixels()
    return img

# Function to apply Protanopia filter (Red blindness)
def protanopia(img):
    img.loadPixels()
    for i in range(len(img.pixels)):
        r, g, b = red(img.pixels[i]), green(img.pixels[i]), blue(img.pixels[i])
        # Set red channel to 0 for Protanopia
        img.pixels[i] = color(0, g, b)
    img.updatePixels()
    return img

# Function to apply Tritanopia filter (Blue blindness)
def tritanopia(img):
    img.loadPixels()
    for i in range(len(img.pixels)):
        r, g, b = red(img.pixels[i]), green(img.pixels[i]), blue(img.pixels[i])
        # Set blue channel to 0 for Tritanopia
        img.pixels[i] = color(r, g, 0)
    img.updatePixels()
    return img

# Set up the initial canvas and load the image
def setup():
    global original_img, color_blindness_img
    
    # Set up canvas
    size(800, 600)
    
    # Load initial image
    load_image(image_files[current_image_index])
    
    # Set up buttons
    buttons.append(Button("Deuteranopia (Green Blind)", 50, 520, 200, 40, apply_deuteranopia))
    buttons.append(Button("Protanopia (Red Blind)", 300, 520, 200, 40, apply_protanopia))
    buttons.append(Button("Tritanopia (Blue Blind)", 550, 520, 200, 40, apply_tritanopia))
    buttons.append(Button("Reset Image", 50, 570, 200, 40, reset_image))
    buttons.append(Button("Change Image", 300, 570, 200, 40, change_image))

# Draw function to update the display
def draw():
    background(255)
    
    # Display the image with current color blindness filter
    image(color_blindness_img, 0, 0)
    
    # Display all buttons
    for button in buttons:
        button.display()

# Button action functions to apply the corresponding color blindness filter
def apply_deuteranopia():
    global color_blindness_img, active_button
    color_blindness_img = deuteranopia(original_img.copy())
    set_active_button("Deuteranopia")

def apply_protanopia():
    global color_blindness_img, active_button
    color_blindness_img = protanopia(original_img.copy())
    set_active_button("Protanopia")

def apply_tritanopia():
    global color_blindness_img, active_button
    color_blindness_img = tritanopia(original_img.copy())
    set_active_button("Tritanopia")

def reset_image():
    global color_blindness_img, active_button
    color_blindness_img = original_img.copy()
    set_active_button("Reset")

def change_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(image_files)  # Loop through images
    load_image(image_files[current_image_index])  # Load the next image

def load_image(image_name):
    global original_img, color_blindness_img
    original_img = loadImage(image_name)
    if original_img is None:
        print("Error loading image: " + image_name)
    else:
        color_blindness_img = original_img.copy()  # Copy the new image for manipulation

def set_active_button(label):
    global active_button
    active_button = label
    for button in buttons:
        button.is_active = button.label.startswith(label)

# Check for button clicks on mouse press
def mousePressed():
    for button in buttons:
        if button.is_pressed():
            button.action()
