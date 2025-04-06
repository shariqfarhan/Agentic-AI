import subprocess
import pyautogui
import time

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


def main() -> dict:
    """Open Freeform, bring it to front, and maximize the window."""
    ensure_freeform_open_and_front()
    maximize_freeform_window()
    open_new_board()
    # draw_rectangle_via_insert_check()
    draw_rectangle_via_insert()
    insert_text_in_rectangle('test')

if __name__ == '__main__':
    main()
