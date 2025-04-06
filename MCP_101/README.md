# MCPaint

## Overview

This project implements an AI agent that solves mathematical problems and visualizes the results in Apple's Freeform application. The agent uses the Multi-Agent Communication Protocol (MCP) to call various mathematical functions and automate interactions with the Freeform app on macOS.

## Components

The project consists of three main Python files:

1. [`freeform_server.py`](freeform_server.py) - The MCP server that provides mathematical tools and Freeform interaction capabilities
2. [`talk2mcp_assignment.py`](talk2mcp_assignment.py) - The client that connects to the MCP server and handles agent iterations
3. [`testing_mac_apps.py`](testing_mac_apps.py) - A utility script for testing Freeform automation functions

## Features

- **Mathematical Operations**: Addition, subtraction, multiplication, division, power, square root, etc.
- **Advanced Functions**: Fibonacci sequence generation, ASCII value conversion, exponential sums
- **Mac OS Automation**: Control of Freeform app via PyAutoGUI and AppleScript
- **Visual Results**: Automated creation of rectangles and text insertion in Freeform

## Requirements

- macOS with Apple Freeform app installed
- Python 3.11+
- Google Gemini API key (for LLM support)

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install python-dotenv mcp pyautogui google-generativeai pillow
   ```
3. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Run the main script to start the agent:

```bash
python talk2mcp_assignment.py
```

The agent will:
1. Connect to the MCP server
2. Process the mathematical query
3. Execute multiple iterations of tool calls
4. Visualize the final result in Freeform

## Example

The default query asks the agent to:
1. Find the ASCII values of characters in "INDIA"
2. Calculate the sum of exponentials of those values
3. Visualize the result in a Freeform board

## Architecture

- The client uses the Gemini 2.0 Flash model to determine which functions to call
- Communication between client and server occurs through the MCP protocol
- The server exposes tools for both mathematical operations and Freeform automation

### [Link to Video Demo](https://youtu.be/LjgBEc43jXg)

## License

This project is for educational purposes.
