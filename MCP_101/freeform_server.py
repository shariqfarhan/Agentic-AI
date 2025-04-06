# Standard library imports
import logging
import math
import os
import subprocess
import sys
import time

# Third-party library imports
import pyautogui
from PIL import Image as PILImage

# MCP-specific imports
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent

def setup_logging():
    """Setup logging with proper permissions and error handling"""
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(script_dir, "logs")

        # Create logs directory with proper permissions
        os.makedirs(log_dir, mode=0o755, exist_ok=True)

        # Test write permissions
        test_file = os.path.join(log_dir, "test_write.tmp")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except (IOError, OSError) as e:
            print(f"Warning: Cannot write to {log_dir}: {str(e)}", file=sys.stderr)
            # Fallback to user's home directory
            log_dir = os.path.expanduser("~/freeform_logs")
            os.makedirs(log_dir, mode=0o755, exist_ok=True)

        log_file = os.path.join(log_dir, "freeform_server.log")

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, mode='a'),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(__name__)
        logger.info(f"Logging initialized. Log file: {log_file}")
        return logger
    except Exception as e:
        print(f"Error setting up logging: {str(e)}", file=sys.stderr)
        # Fallback to basic console logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        return logging.getLogger(__name__)

# Initialize logging
logger = setup_logging()

# Create an MCP server
mcp = FastMCP("Freeform")
logger.info("Initialized Freeform MCP server")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

def ensure_freeform_open_and_front(wait: float = 1.0) -> None:
    """Ensure Freeform is running and frontmost."""
    # Check if Freeform is already running
    result = subprocess.run(
        ["osascript", "-e", 'tell application "System Events" to (name of processes) contains "Freeform"'],
        capture_output=True, text=True
    )

    if "false" in result.stdout:
        subprocess.run(["open", "-a", "Freeform"])
        time.sleep(wait + 1)

    # Bring Freeform to front
    subprocess.run(["osascript", "-e", 'tell application "Freeform" to activate'])
    time.sleep(wait)


def maximize_freeform_window():
    """Resize and position the Freeform window to fullscreen-like state."""
    applescript = '''
    tell application "System Events"
        tell application process "Freeform"
            set frontmost to true
            try
                set size of front window to {1920, 1080}
                set position of front window to {0, 0}
            end try
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])

def open_new_board():
    """Simulate ⌘+N to open a new board in Freeform."""
    applescript = '''
    tell application "System Events"
        keystroke "n" using command down
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])
    time.sleep(1)  # wait a moment for the new board to render

def draw_rectangle(x1: int, y1: int, x2: int, y2: int):
    """Draw a rectangle from (x1, y1) to (x2, y2) using mouse drag."""
    print(f"Drawing rectangle from ({x1}, {y1}) to ({x2}, {y2})...")
    pyautogui.moveTo(x1, y1, duration=0.3)
    pyautogui.mouseDown()
    pyautogui.moveTo(x2, y2, duration=0.3)
    pyautogui.mouseUp()
    print("Rectangle drawn.")

def draw_rectangle_via_insert():
    """Insert a rectangle in Freeform by clicking Insert → Shapes → Rectangle."""
    time.sleep(1)  # Give Freeform time to stabilize

    # Step 1: Click the "Insert" button (you may need to adjust these coordinates!)
    pyautogui.moveTo(250, 30, duration=0.3)  # ← estimate: Insert in toolbar
    pyautogui.click()
    time.sleep(0.5)

    # Step 2: Move to "Shapes" in Insert menu
    pyautogui.moveTo(250, 80, duration=0.3)  # ← adjust as needed for Shapes
    pyautogui.click()
    time.sleep(0.5)

    # Step 3: Click on the Rectangle option
    pyautogui.moveTo(500, 80, duration=0.3)  # ← adjust as needed for Rectangle
    pyautogui.click()
    time.sleep(0.5)

    # Step 4: Click on the canvas to place it
    pyautogui.moveTo(600, 500, duration=0.3)  # Anywhere on the board
    pyautogui.click()


def insert_text_in_rectangle(text: str):
    """Insert text inside an existing rectangle in Freeform."""
    time.sleep(0.5)

    # Step 1: Click inside the rectangle (adjust coordinates based on your layout)
    pyautogui.moveTo(700, 550, duration=0.3)  # ← center of rectangle
    pyautogui.click()
    time.sleep(0.5)

    # Step 2: Type the text
    pyautogui.write(text, interval=0.05)
    time.sleep(0.5)

    pyautogui.moveTo(900, 550, duration=0.3)  # ← outside of rectangle
    pyautogui.click()

@mcp.tool()
def add_details_in_freeform(text:str) -> dict:
    """Open Freeform, bring it to front, create a new board, draw a rectangle, and insert text."""
    ensure_freeform_open_and_front()
    maximize_freeform_window()
    open_new_board()
    draw_rectangle_via_insert()
    insert_text_in_rectangle(text)
    return {
    "content": [
        TextContent(
            type="text",
            text=f"Added new rectangle and inserted text: '{text}' into Freeform board."
        )
    ]
    }

def ensure_mail_open_and_front(wait: float = 1.0):
    """Ensure Mail.app is running and brought to front."""
    result = subprocess.run(
        ["osascript", "-e", 'tell application "System Events" to (name of processes) contains "Mail"'],
        capture_output=True, text=True
    )

    if "false" in result.stdout:
        subprocess.run(["open", "-a", "Mail"])
        time.sleep(wait + 1)

    subprocess.run(["osascript", "-e", 'tell application "Mail" to activate'])
    time.sleep(wait)

def maximize_mail_window():
    """Resize and position the Mail window."""
    applescript = '''
    tell application "System Events"
        tell application process "Mail"
            set frontmost to true
            try
                set size of front window to {1440, 900}
                set position of front window to {0, 0}
            end try
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])

def open_new_mail():
    """Opens a new mail compose window."""
    applescript = '''
    tell application "System Events"
        keystroke "n" using command down
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])
    time.sleep(1)

def compose_mail(recipient: str, subject: str, body: str):
    """Compose and open a new mail message in the Mail app with pre-filled fields."""
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{body}", visible:true}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{recipient}"}}
            activate
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])

def compose_and_send_mail(recipient: str, subject: str, body: str):
    """Compose and automatically send a mail message via macOS Mail.app."""
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{body}", visible:false}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{recipient}"}}
            send
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])

@mcp.tool()
def send_email_via_mail_app(recipient: str, subject: str, body: str):
    """Send an email using macOS Mail app via AppleScript."""
    ensure_mail_open_and_front()
    maximize_mail_window()
    open_new_mail()
    # or
    compose_and_send_mail(recipient, subject, body)
    return {
    "content": [
        TextContent(
            type="text",
            text=f"Sent email to : '{recipient}' with subject {subject} and body {body}"
        )
    ]
    }


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]


if __name__ == "__main__":
    logger.info("Starting Freeform MCP server")
    mcp.run()
