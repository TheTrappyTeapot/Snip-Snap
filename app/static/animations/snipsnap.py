import turtle
import math

# --- Configuration ---

COLOR_MAIN = "black"
COLOR_SHADOW = "#D3D3D3"  
COLOR_ACCENT = "#FF8C00" 
BG_COLOR = "white"
TILT_ANGLE = 20           

# --- Setup Screen ---
screen = turtle.Screen()
screen.setup(width=600, height=700)
screen.bgcolor(BG_COLOR)
screen.title("Snip Snap - Dynamic Emblem")

# --- Setup Artist ---
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# --- Helper Functions ---

def jump_to(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

def rotate_coords(x, y, angle_deg):
    rad = math.radians(angle_deg)
    # Standard rotation matrix formula
    new_x = x * math.cos(rad) - y * math.sin(rad)
    new_y = x * math.sin(rad) + y * math.cos(rad)
    return new_x, new_y

def draw_angled_rect(width, height, angle):
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()

# --- The Main Logo Drawing Function ---

def draw_emblem_layer(offset_x, offset_y, color, angle):

    t.color(color)
    
    # 1. THE VERTICAL COMB (Top)
    # Calculate start position based on rotation
    start_x, start_y = rotate_coords(-15, 60, angle)
    jump_to(start_x + offset_x, start_y + offset_y)
    t.setheading(angle) # Point in the direction of the tilt
    
    # Draw the main block
    t.begin_fill()
    draw_angled_rect(30, 140, angle)
    t.end_fill()
    
    # Cut the teeth (Negative Space)
    # We only do this if it's the top layer (black), otherwise shadow looks solid
    if color == COLOR_MAIN:
        t.color(BG_COLOR)
        t.pensize(2)
        base_cut_x, base_cut_y = rotate_coords(-15, 190, angle)
        
        for i in range(20):
            # Calculate step down relative to angle
            step_dist = i * 6
            # Move 'down' the comb (which is actually backwards relative to angle + 90)
            dx = math.cos(math.radians(angle + 270)) * step_dist
            dy = math.sin(math.radians(angle + 270)) * step_dist
            
            jump_to(base_cut_x + dx + offset_x, base_cut_y + dy + offset_y)
            t.setheading(angle) # Cut horizontally relative to tilt
            t.forward(15)
            
        t.color(color) # Reset to black for next steps

    # 2. THE HORIZONTAL CLIPPER (Middle)

    # This sits on top of the vertical comb
    start_x, start_y = rotate_coords(-110, 0, angle)
    jump_to(start_x + offset_x, start_y + offset_y)
    t.setheading(angle)
    
    # Draw curved body
    t.begin_fill()
    t.right(10) # Slight dip for the curve
    t.circle(600, 20) # The aesthetic curve
    t.setheading(angle + 90)
    t.forward(60)
    t.setheading(angle + 180)
    t.forward(205)
    t.setheading(angle + 270)
    t.forward(50)
    t.end_fill()
    
    # Cut the teeth
    if color == COLOR_MAIN:
        t.color(BG_COLOR)
        t.pensize(3)
        # We iterate "across" the comb
        for i in range(20):
            dist = i * 10
            # Calculate position along the tilted line
            r_x, r_y = rotate_coords(-100 + dist, 10, angle)
            jump_to(r_x + offset_x, r_y + offset_y)
            t.setheading(angle + 90) # Perpendicular to tilt
            t.forward(45)
        t.color(color)

    # 3. THE SCISSORS (Bottom)
    t.pensize(8)
    
    # Left Handle
    cx, cy = rotate_coords(-40, -100, angle)
    jump_to(cx + offset_x, cy + offset_y)
    t.setheading(angle)
    t.circle(25)
    
    # Right Handle
    cx, cy = rotate_coords(40, -100, angle)
    jump_to(cx + offset_x, cy + offset_y)
    t.setheading(angle)
    t.circle(25)
    
    # Shanks (The arms connecting up)
    t.pensize(10)
    
    # Left Arm
    sx, sy = rotate_coords(-40, -75, angle)
    jump_to(sx + offset_x, sy + offset_y)
    t.setheading(angle + 70)
    t.forward(80)
    
    # Right Arm
    sx, sy = rotate_coords(40, -75, angle)
    jump_to(sx + offset_x, sy + offset_y)
    t.setheading(angle + 110)
    t.forward(80)

def draw_aesthetic_text():
   
    t.setheading(0)
    jump_to(0, -220)
    t.color(COLOR_ACCENT) # Orange
    t.write("SNIP SNAP", align="center", font=("Impact", 40, "normal"))
    
    jump_to(0, -250)
    t.color("black")
    t.write("EST. 2026", align="center", font=("Arial", 12, "bold"))

# --- Execution ---

# 1. Draw Shadow (Offset slightly to the right and down)
# This adds the "Impressive" pop
draw_emblem_layer(10, -10, COLOR_SHADOW, TILT_ANGLE)

# 2. Draw Main Logo (Black)
draw_emblem_layer(0, 0, COLOR_MAIN, TILT_ANGLE)

# 3. Draw Text
draw_aesthetic_text()
turtle.done()