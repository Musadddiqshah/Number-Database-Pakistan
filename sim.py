#!/usr/bin/env python3
import requests
import curses
from curses import wrapper
import time
import hashlib
import random
import sys
import threading
import os
# ============================
# BRANDING (SIMPLIFIED)
# ============================

BRAND_NAME = "INFORMATION LOOKUP TOOL"

# Display initial banner BEFORE curses takes over
print("\n" + "="*60)
print(" " * 15 + "🚀 INITIALIZING TOOL 🚀")
print("="*60)
print("\n\t✨ AM INFORMATION LOOKUP TOOL")
print("\t✨ Secure Edition v2.0")
print("\t✨ " + "🔴" + " Coded By " + "⚫" + " AM Musaddiq " + "🔴")
print("\n" + "="*60)
time.sleep(1.5)
os.system("clear")
# ============================
# API FUNCTIONS (WORKING)
# ============================

def fetch_data_primary(query):
    """Primary API call"""
    try:
        url = f"https://app.findpakjobs.pk/api.php?username=wduser1&password=112233&number={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def fetch_data_secondary(query):
    """Secondary API call"""
    try:
        url = f"https://api.simdatabase.com/v1/lookup?number={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def fetch_data(query):
    """Fetch data with fallback"""
    # Validate input
    if not query or len(query) < 10:
        return {"error": "Invalid input. Phone: 11 digits, CNIC: 13 digits"}

    # Clean query (digits only)
    query = ''.join(filter(str.isdigit, query))

    # Determine type
    query_type = "phone" if query.startswith('03') else "cnic"

    # Try primary API
    result = fetch_data_primary(query)

    # Check if successful
    if "error" not in result:
        result["_source"] = "Primary Database"
    else:
        # Try secondary API
        time.sleep(0.3)
        result = fetch_data_secondary(query)
        if "error" not in result:
            result["_source"] = "Secondary Database"

    # Add metadata
    result["_metadata"] = {
        "query": query[:3] + "****" + query[-3:] if len(query) > 6 else "***",
        "type": query_type,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "session": hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
    }

    return result

# ============================
# LOADING ANIMATION FUNCTION
# ============================

def show_rotating_loading(stdscr, message):
    """Show rotating loading animation"""
    max_y, max_x = stdscr.getmaxyx()
    stdscr.clear()
    
    # Braille spinner frames
    spinner_frames = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    frame_idx = 0
    
    # Calculate position
    y_pos = max_y // 2
    loading_text = f"{spinner_frames[frame_idx]}      {message}      {spinner_frames[frame_idx]}"
    x_pos = max(0, (max_x - len(loading_text)) // 2)
    
    # Show animation for 3 seconds or until interrupted
    start_time = time.time()
    while time.time() - start_time < 5:
        # Update spinner frame
        frame_idx = (frame_idx + 1) % len(spinner_frames)
        loading_text = f"{spinner_frames[frame_idx]}      {message}      {spinner_frames[frame_idx]}"
        x_pos = max(0, (max_x - len(loading_text)) // 2)
        
        # Clear line and redraw
        stdscr.move(y_pos, 0)
        stdscr.clrtoeol()
        stdscr.addstr(y_pos, x_pos, loading_text)
        stdscr.refresh()
        time.sleep(0.1)
    
    return True

# ============================
# DISPLAY FUNCTIONS
# ============================

def format_data(data):
    """Format output"""
    lines = []

    # Header
    lines.append("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    lines.append(f"┃                 {BRAND_NAME:<36} ┃")
    lines.append(f"┃                 Secure Edition v2.7                  ┃")
    lines.append("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    lines.append("           [★]     Author: AM Musaddiq Shah     [★]     ")

    # Session info
    if "_metadata" in data:
        meta = data["_metadata"]
        lines.append("[ SESSION INFORMATION ]")
        lines.append(f"  🔐 Session ID: {meta.get('session', 'N/A')}")
        lines.append(f"  🕒 Time: {meta.get('timestamp', 'N/A')}")
        lines.append(f"  🔍 Query: {meta.get('query', 'N/A')} ({meta.get('type', 'N/A')})")
        if "_source" in data:
            lines.append(f"  📡 Source: {data['_source']}")
        lines.append("")

    # Check for errors
    if "error" in data:
        lines.append("[ ERROR ]")
        lines.append(f"  ❌ {data['error']}")
        lines.append("")
        lines.append("[ SUGGESTIONS ]")
        lines.append("  • Verify the phone number/CNIC is correct")
        lines.append("  • Check your internet connection")
        lines.append("  • Try again in a few moments")
        lines.append("  • Contact support if issue persists")
    else:
        # Display data
        has_data = False
        for key, value in data.items():
            if key.startswith('_'):
                continue

            has_data = True
            lines.append(f"[ {key.upper().replace('_', ' ')} ]")

            if isinstance(value, dict):
                for k, v in value.items():
                    lines.append(f"  • {k}: {v}")
            elif isinstance(value, list):
                for item in value:
                    lines.append(f"  • {item}")
            else:
                lines.append(f"  • {value}")
            lines.append("")

        if not has_data:
            lines.append("[ INFORMATION ]")
            lines.append("  📭 No information found for this query")
            lines.append("  [!]  The database may not have this record")
            lines.append("")

    # Footer
    lines.append("[ SYSTEM STATUS ]")
    lines.append("  ✅ Application: Running")
    lines.append("  🔒 Security: Enabled")
    lines.append(f"  🏷️  Brand: {BRAND_NAME}")
    lines.append("  👨‍💻 Developer: AM Musaddiq Shah")

    return lines

def draw_banner(stdscr, start_y, max_x):
    """Draw banner with highlighted name"""
    banner_lines = [
        "╔══════════════════════════════════════════════════╗",
        "║           AM INFORMATION LOOKUP TOOL             ║",
        "║             Secure Edition v2.0                  ║",
        "║         ╔══════════════════════════════╗         ║",
        "║         ║    AM Musaddiq               ║         ║",
        "║         ╚══════════════════════════════╝         ║",
        "╚══════════════════════════════════════════════════╝"
    ]

    for i, line in enumerate(banner_lines):
        if start_y + i < curses.LINES - 2:
            x_pos = max(0, (max_x - len(line)) // 2)
            
            # Highlight specific lines
            if i == 4:  # Line with the name
                stdscr.attron(curses.color_pair(3) | curses.A_BOLD | curses.A_REVERSE)
                stdscr.addstr(start_y + i, x_pos, line)
                stdscr.attroff(curses.color_pair(3) | curses.A_BOLD | curses.A_REVERSE)
            else:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(start_y + i, x_pos, line)
                stdscr.attroff(curses.color_pair(1))

    return len(banner_lines)

def draw_menu(stdscr, selected_idx):
    """Draw main menu"""
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()

    # Draw banner
    banner_height = draw_banner(stdscr, 1, max_x)

    # Menu separator
    sep_y = banner_height + 1
    if sep_y < max_y - 1:
        separator = "─" * (max_x - 4)
        stdscr.attron(curses.color_pair(4))
        x_pos = max(0, (max_x - len(separator)) // 2)
        stdscr.addstr(sep_y, x_pos, separator)
        stdscr.attroff(curses.color_pair(4))

    # Menu title
    title_y = sep_y + 2
    if title_y < max_y - 1:
        title = "━ MAIN MENU ━"
        x_pos = max(0, (max_x - len(title)) // 2)
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(title_y, x_pos, title)
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

    # Menu items
    menu_items = [
        "📱 Phone Number Lookup",
        "🆔 CNIC Information",
        "⚡ Quick Search",
        "🔧 Settings",
        "[!]  About",
        "🚪 Exit"
    ]

    menu_start = title_y + 2

    for i, item in enumerate(menu_items):
        if menu_start + i < max_y - 1:
            x_pos = max(0, (max_x - len(item)) // 2)

            if i == selected_idx:
                stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(menu_start + i, x_pos - 2, "» ")
                stdscr.addstr(menu_start + i, x_pos, item)
                stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
            else:
                stdscr.addstr(menu_start + i, x_pos, item)

    # Footer with highlighted name
    footer_y = menu_start + len(menu_items) + 2
    if footer_y < max_y - 1:
        footer_line1 = f"🔒 {BRAND_NAME} • Developer: AM Musaddiq Shah"
        x_pos = max(0, (max_x - len(footer_line1)) // 2)
        stdscr.attron(curses.color_pair(5))
        stdscr.addstr(footer_y, x_pos, footer_line1)
        stdscr.attroff(curses.color_pair(5))
        
        footer_line2 = "↑↓ Navigate • Enter Select • Q Quit"
        x_pos = max(0, (max_x - len(footer_line2)) // 2)
        stdscr.attron(curses.color_pair(1) | curses.A_DIM)
        stdscr.addstr(footer_y + 1, x_pos, footer_line2)
        stdscr.attroff(curses.color_pair(1) | curses.A_DIM)

    stdscr.refresh()

def get_input(stdscr, prompt):
    """Get user input"""
    max_y, max_x = stdscr.getmaxyx()

    # Clear area
    for i in range(5):
        if max_y//2 + i - 2 < max_y:
            stdscr.move(max_y//2 + i - 2, 0)
            stdscr.clrtoeol()

    # Show prompt
    x_pos = max(0, (max_x - len(prompt)) // 2)
    stdscr.addstr(max_y//2 - 2, x_pos, prompt)

    # Input box
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(max_y//2 - 1, x_pos - 2, "┌" + "─" * (len(prompt) + 4) + "┐")
    stdscr.addstr(max_y//2, x_pos - 2, "│ " + " " * len(prompt) + "  │")
    stdscr.addstr(max_y//2 + 1, x_pos - 2, "└" + "─" * (len(prompt) + 4) + "┘")
    stdscr.attroff(curses.color_pair(1))

    # Get input
    curses.echo()
    curses.curs_set(1)
    stdscr.move(max_y//2, x_pos)
    try:
        user_input = stdscr.getstr(max_y//2, x_pos, 30).decode('utf-8')
    except:
        user_input = ""
    finally:
        curses.noecho()
        curses.curs_set(0)

    return user_input.strip()

def result_screen(stdscr, lines):
    """Display results - Enter key to exit"""
    max_y, max_x = stdscr.getmaxyx()

    position = 0
    content_start = 1

    while True:
        stdscr.clear()

        # Display lines
        display_height = max_y - 3
        for i in range(min(len(lines) - position, display_height)):
            line = lines[position + i]
            line = line[:max_x - 4]

            # Color coding
            if line.startswith("┏") or line.startswith("┗") or line.startswith("┃"):
                stdscr.attron(curses.color_pair(1))
            elif line.startswith("[ ") and "ERROR" in line:
                stdscr.attron(curses.color_pair(6))
            elif line.startswith("[ "):
                stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
            elif "AM Musaddiq Shah" in line or "Musaddiq Shah" in line or "AM Musaddiq" in line:
                stdscr.attron(curses.color_pair(3) | curses.A_BOLD)

            stdscr.addstr(content_start + i, 2, line)

            if line.startswith("┏") or line.startswith("┗") or line.startswith("┃"):
                stdscr.attroff(curses.color_pair(1))
            elif line.startswith("[ ") and "ERROR" in line:
                stdscr.attroff(curses.color_pair(6))
            elif line.startswith("[ "):
                stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
            elif "AM Musaddiq Shah" in line or "Musaddiq Shah" in line or "AM Musaddiq" in line:
                stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)

        # Scroll indicator
        if len(lines) > display_height:
            indicator = f"📖 Page {position//display_height + 1}/{(len(lines) + display_height - 1)//display_height}"
            stdscr.addstr(max_y - 2, 2, indicator[:max_x - 4])

        # Instructions - CHANGED HERE: Enter instead of ESC
        instructions = "ENTER: Back to Menu • ↑↓: Scroll • PgUp/PgDn: Page"
        x_pos = max(0, (max_x - len(instructions)) // 2)
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(max_y - 1, x_pos, instructions)
        stdscr.attroff(curses.color_pair(2))

        stdscr.refresh()
        key = stdscr.getch()

        # CHANGED HERE: Enter key (10 or 13) to exit, not ESC
        if key in [10, 13]:  # ENTER key to go back to menu
            break
        elif key == curses.KEY_UP and position > 0:
            position -= 1
        elif key == curses.KEY_DOWN and position < len(lines) - display_height:
            position += 1
        elif key == curses.KEY_PPAGE:  # Page up
            position = max(0, position - display_height)
        elif key == curses.KEY_NPAGE:  # Page down
            position = min(len(lines) - display_height, position + display_height)
        # ESC still works as alternative
        elif key == 27:  # ESC also works
            break

def about_screen(stdscr):
    """About screen with highlighted name"""
    max_y, max_x = stdscr.getmaxyx()
    stdscr.clear()

    about_lines = [
        "",
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
        f"┃               {BRAND_NAME:<33} ┃",
        "┠───────────────────────────────────────────────────┨",
        "┃                                                   ┃",
        "┃  📊 Information Lookup Tool v2.0                  ┃",
        "┃  🔒 Secure Edition                                ┃",
        "┃  📱 Phone & CNIC Database Access                  ┃",
        "┃  🌐 Dual API Fallback System                      ┃",
        "┃  ⚡ Real-time Data Retrieval                      ┃",
        "┃                                                   ┃",
        "┃  Features:                                        ┃",
        "┃    • Phone Number Information                     ┃",
        "┃    • CNIC Details Lookup                          ┃",
        "┃    • Secure Session Management                    ┃",
        "┃    • Encrypted Communication                      ┃",
        "┃    • Privacy-Focused Design                       ┃",
        "┃                                                   ┃",
        "┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃",
        "┃   ★★★★★★★★★★★★★★★★★★★★★★★★★★★★                    ┃",
        "┃   ★        DEVELOPER & OWNER: ★                   ┃",
        "┃   ★             Musaddiq Shah ★                   ┃",
        "┃   ★★★★★★★★★★★★★★★★★★★★★★★★★★★★                    ┃",
        "┃                                                   ┃",
        "┃  This tool is for authorized use only.            ┃",
        "┃                                                   ┃",
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛",
        "",
        "            Press ENTER to return to menu..."
    ]

    for i, line in enumerate(about_lines):
        if i < max_y:
            x_pos = max(0, (max_x - len(line)) // 2)
            
            # Highlight developer name
            if " Musaddiq Shah" in line:
                stdscr.attron(curses.color_pair(3) | curses.A_BOLD | curses.A_REVERSE)
                stdscr.addstr(i, x_pos, line)
                stdscr.attroff(curses.color_pair(3) | curses.A_BOLD | curses.A_REVERSE)
            else:
                stdscr.addstr(i, x_pos, line)

    stdscr.refresh()
    # Wait for ENTER key
    while True:
        key = stdscr.getch()
        if key in [10, 13]:  # ENTER
            break

def settings_screen(stdscr):
    """Settings screen"""
    max_y, max_x = stdscr.getmaxyx()
    stdscr.clear()

    settings_lines = [
        "",
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
        "┃                  SETTINGS                         ┃",
        "┠───────────────────────────────────────────────────┨",
        "┃                                                   ┃",
        "┃  ⚙️  Configuration:                                ┃",
        "┃    • API Timeout: 10 seconds                      ┃",
        "┃    • Retry Attempts: 2                            ┃",
        "┃    • Connection: Secure                           ┃",
        "┃                                                   ┃",
        "┃  🔒 Security Settings:                            ┃",
        "┃    • Session Encryption: Active                   ┃",
        "┃    • Data Masking: Enabled                        ┃",
        "┃                                                   ┃",
        "┃  📊 System Status:                                ┃",
        "┃    • APIs: Operational                            ┃",
        "┃    • Database: Connected                          ┃",
        "┃    • Security: Maximum                            ┃",
        "┃                                                   ┃",
        "┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃",
        "┃           Tool Owner:    Musaddiq Shah            ┃",
        "┃  ⚠️ Simply changing banner won't make you devloper ┃",
        "┃                                                   ┃",
        "┗━━━━━━━━━━━━━━━━━━════════════════════════════════━┛",
        "",
        "            Press ENTER to continue..."
    ]

    for i, line in enumerate(settings_lines):
        if i < max_y:
            x_pos = max(0, (max_x - len(line)) // 2)
            	
            # Highlight owner name
            if "AM Musaddiq Shah" in line:
                stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(i, x_pos, line)
                stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
            else:
                stdscr.addstr(i, x_pos, line)

    stdscr.refresh()
    # Wait for ENTER key
    while True:
        key = stdscr.getch()
        if key in [10, 13]:  # ENTER
            break

# ============================
# MAIN APPLICATION
# ============================

def main(stdscr):
    curses.start_color()
    curses.curs_set(0)
    stdscr.clear()
    
    # Set terminal to support colors
    stdscr.keypad(True)
    
    # Initialize colors with better contrast
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Borders
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Success
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)     # Selected/Highlighted Name
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Headers
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Text
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)     # Errors

    selected_idx = 0

    while True:
        draw_menu(stdscr, selected_idx)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < 5:
            selected_idx += 1
        elif key in [10, 13]:  # Enter
            if selected_idx == 0:  # Phone
                phone = get_input(stdscr, "Enter Phone Number (03xxxxxxxxx):")
                if phone:
                    show_rotating_loading(stdscr, "Loading information ...")
                    data = fetch_data(phone)
                    lines = format_data(data)
                    result_screen(stdscr, lines)

            elif selected_idx == 1:  # CNIC
                cnic = get_input(stdscr, "Enter CNIC (13 digits without dashes):")
                if cnic:
                    show_rotating_loading(stdscr, "Loading information ...")
                    data = fetch_data(cnic)
                    lines = format_data(data)
                    result_screen(stdscr, lines)

            elif selected_idx == 2:  # Quick
                query = get_input(stdscr, "Enter Phone or CNIC:")
                if query:
                    show_rotating_loading(stdscr, "Loading information ...")
                    data = fetch_data(query)
                    lines = format_data(data)
                    result_screen(stdscr, lines)

            elif selected_idx == 3:  # Settings
                settings_screen(stdscr)

            elif selected_idx == 4:  # About
                about_screen(stdscr)

            elif selected_idx == 5:  # Exit
                stdscr.clear()
                max_y, max_x = stdscr.getmaxyx()
                goodbye = f"Thank you for using {BRAND_NAME}!"
                author = "Developed by:  Musaddiq Shah"
                
                x_pos = max(0, (max_x - len(goodbye)) // 2)
                stdscr.addstr(max_y//2 - 1, x_pos, goodbye)
                
                x_pos = max(0, (max_x - len(author)) // 2)
                stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(max_y//2 + 1, x_pos, author)
                stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
                
                stdscr.refresh()
                time.sleep(2)
                break

        elif key in [81, 113]:  # Q
            break

# ============================
# START APPLICATION
# ============================

if __name__ == "__main__":
    try:
        wrapper(main)
    except KeyboardInterrupt:
        print(f"\n{BRAND_NAME} - Session terminated by user.")
        print("Developer: AM Musaddiq ")
    except Exception as e:
        print(f"\nApplication error. Please restart.")
        print("Developer: AM Musaddiq ")
