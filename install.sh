#!/data/data/com.termux/files/usr/bin/bash
# ===========================================
# AM INFORMATION LOOKUP TOOL - TERMUX INSTALLER
# ===========================================
# Author: AM Musaddiq Shah
# Version: 2.0
# Description: One-click installer for Termux
# ===========================================

# Colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
MAGENTA='\033[1;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
RESET='\033[0m'

# Paths
TERMUX_BIN="/data/data/com.termux/files/usr/bin"
TERMUX_HOME="/data/data/com.termux/files/home"
TOOL_NAME="sim"
SCRIPT_NAME="sim.py"

# Print functions
print_banner() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║      AM INFORMATION LOOKUP TOOL - TERMUX         ║"
    echo "║             Secure Edition v2.0                  ║"
    echo "║          Coded By: AM Musaddiq Shah              ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${RESET}"
    echo -e "${YELLOW}One-Click Installer for Termux${RESET}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${RESET} $1"
}

print_error() {
    echo -e "${RED}✗${RESET} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${RESET} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${RESET} $1"
}

print_step() {
    echo -e "${MAGENTA}▶${RESET} ${BOLD}$1${RESET}"
}

check_root() {
    if [ "$(whoami)" = "root" ]; then
        print_error "Don't run as root! Run as normal Termux user."
        exit 1
    fi
}

check_termux() {
    if [ ! -d "$TERMUX_BIN" ] || [ ! -d "$TERMUX_HOME" ]; then
        print_error "This script is for Termux only!"
        exit 1
    fi
}

update_packages() {
    print_step "Step 1: Updating Termux packages"
    print_info "This may take a few minutes..."
    
    if pkg update -y && pkg upgrade -y; then
        print_success "Termux packages updated"
    else
        print_warning "Failed to update packages, continuing..."
    fi
}

install_python() {
    print_step "Step 2: Installing Python"
    
    if command -v python3 > /dev/null 2>&1; then
        print_success "Python3 is already installed"
        python3 --version
    else
        print_info "Installing Python3..."
        if pkg install python -y; then
            print_success "Python3 installed successfully"
        else
            print_error "Failed to install Python3"
            exit 1
        fi
    fi
}

install_pip() {
    print_step "Step 3: Setting up pip"
    
    if command -v pip3 > /dev/null 2>&1; then
        print_success "pip3 is already installed"
    else
        print_info "Setting up pip..."
        python3 -m ensurepip --upgrade
        if [ $? -eq 0 ]; then
            print_success "pip setup complete"
        else
            print_warning "pip setup had issues, continuing..."
        fi
    fi
    
    # Upgrade pip
    print_info "Upgrading pip..."
    python3 -m pip install --upgrade pip --quiet
}

install_dependencies() {
    print_step "Step 4: Installing Python dependencies"
    
    # Check for requirements.txt
    if [ -f "requirements.txt" ]; then
        print_info "Found requirements.txt, installing packages..."
        if python3 -m pip install -r requirements.txt --quiet; then
            print_success "All dependencies installed from requirements.txt"
        else
            print_warning "Some dependencies failed, installing essential ones..."
            install_essential_deps
        fi
    else
        print_warning "requirements.txt not found, installing essential packages..."
        install_essential_deps
    fi
}

install_essential_deps() {
    print_info "Installing essential packages..."
    
    essential_packages=("requests" "colorama")
    for package in "${essential_packages[@]}"; do
        print_info "Installing $package..."
        if python3 -m pip install "$package" --quiet; then
            print_success "Installed: $package"
        else
            print_error "Failed to install: $package"
        fi
    done
}

install_tool() {
    print_step "Step 5: Installing the tool"
    
    # Check if sim.py exists
    if [ ! -f "$SCRIPT_NAME" ]; then
        print_error "$SCRIPT_NAME not found in current directory!"
        print_info "Please run this script in the same folder as $SCRIPT_NAME"
        exit 1
    fi
    
    # Create backup if sim already exists
    if [ -f "$TERMUX_BIN/$TOOL_NAME" ]; then
        print_info "Backing up existing $TOOL_NAME..."
        mv "$TERMUX_BIN/$TOOL_NAME" "$TERMUX_BIN/${TOOL_NAME}.bak"
        print_success "Backup created: $TERMUX_BIN/${TOOL_NAME}.bak"
    fi
    
    # Copy and make executable
    print_info "Installing $SCRIPT_NAME as $TOOL_NAME..."
    
    # Check if script has shebang
    if ! head -n 1 "$SCRIPT_NAME" | grep -q "#!/usr/bin/env python3"; then
        print_info "Adding shebang to script..."
        echo "#!/usr/bin/env python3" > temp_sim.py
        cat "$SCRIPT_NAME" >> temp_sim.py
        mv temp_sim.py "$SCRIPT_NAME"
    fi
    
    # Copy to Termux bin
    cp "$SCRIPT_NAME" "$TERMUX_BIN/$TOOL_NAME"
    
    # Make executable
    chmod +x "$TERMUX_BIN/$TOOL_NAME"
    
    if [ $? -eq 0 ]; then
        print_success "Tool installed to: $TERMUX_BIN/$TOOL_NAME"
    else
        print_error "Failed to install tool"
        exit 1
    fi
}

setup_path() {
    print_step "Step 6: Setting up PATH"
    
    # Check if Termux bin is in PATH
    if echo "$PATH" | grep -q "$TERMUX_BIN"; then
        print_success "Termux bin is already in PATH"
    else
        print_info "Adding Termux bin to PATH..."
        echo 'export PATH="$PATH:/data/data/com.termux/files/usr/bin"' >> "$TERMUX_HOME/.bashrc"
        print_success "Added to PATH in .bashrc"
    fi
}

create_shortcut() {
    print_step "Step 7: Creating shortcuts"
    
    # Create a simple launcher script
    SHORTCUT="$TERMUX_HOME/start-$TOOL_NAME.sh"
    
    cat > "$SHORTCUT" << EOF
#!/data/data/com.termux/files/usr/bin/bash
echo "Starting AM Information Lookup Tool..."
echo "Coded by: AM Musaddiq Shah"
$TOOL_NAME
EOF
    
    chmod +x "$SHORTCUT"
    print_success "Shortcut created: $SHORTCUT"
}

create_desktop_entry() {
    print_step "Step 8: Creating desktop entry (if supported)"
    
    # Try to create a desktop entry for Termux:Widget
    DESKTOP_ENTRY="$TERMUX_HOME/.shortcuts/$TOOL_NAME.sh"
    
    if [ -d "$TERMUX_HOME/.shortcuts" ]; then
        cat > "$DESKTOP_ENTRY" << EOF
#!/data/data/com.termux/files/usr/bin/bash
termux-toast "Starting AM Information Tool"
am start -n com.termux/com.termux.app.TermuxActivity
sleep 2
$TOOL_NAME
EOF
        
        chmod +x "$DESKTOP_ENTRY"
        print_success "Desktop shortcut created for Termux:Widget"
    else
        print_info "Termux:Widget not detected (optional)"
    fi
}

verify_installation() {
    print_step "Step 9: Verifying installation"
    
    # Check if tool is accessible
    if command -v "$TOOL_NAME" > /dev/null 2>&1; then
        print_success "Tool is now accessible from anywhere!"
        print_success "Installation verified ✓"
        return 0
    else
        # Try direct path
        if [ -x "$TERMUX_BIN/$TOOL_NAME" ]; then
            print_warning "Tool installed but not in PATH"
            print_info "Run: $TERMUX_BIN/$TOOL_NAME"
            return 1
        else
            print_error "Installation failed!"
            return 2
        fi
    fi
}

show_usage() {
    print_step "Step 10: Installation Complete!"
    
    echo -e "${GREEN}${BOLD}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║          INSTALLATION SUCCESSFUL!                ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${RESET}"
    
    echo -e "${CYAN}${BOLD}📱 USAGE INSTRUCTIONS:${RESET}"
    echo -e "${WHITE}1. Open Termux anywhere${RESET}"
    echo -e "${GREEN}2. Type: ${BOLD}sim${RESET} ${GREEN}and press Enter${RESET}"
    echo -e "${WHITE}3. Use the menu to search phone numbers/CNIC${RESET}"
    
    echo -e "\n${YELLOW}${BOLD}🎯 QUICK START:${RESET}"
    echo -e "${GREEN}   $ sim${RESET}"
    
    echo -e "\n${MAGENTA}${BOLD}🔧 ALTERNATIVE METHODS:${RESET}"
    echo -e "${WHITE}   $ $TERMUX_BIN/sim${RESET}"
    echo -e "${WHITE}   $ bash ~/start-sim.sh${RESET}"
    
    echo -e "\n${CYAN}${BOLD}🚀 TEST IT NOW:${RESET}"
    echo -e "${GREEN}   Type 'sim' and press Enter${RESET}"
    
    echo -e "\n${YELLOW}${BOLD}📝 NOTES:${RESET}"
    echo -e "${WHITE}• Tool created by: AM Musaddiq Shah${RESET}"
    echo -e "${WHITE}• Version: Secure Edition v2.0${RESET}"
    echo -e "${WHITE}• Restart Termux if 'sim' command not found${RESET}"
}

cleanup() {
    print_info "Cleaning up..."
    # Remove temporary files if any
    [ -f "temp_sim.py" ] && rm -f temp_sim.py
}

main() {
    print_banner
    
    # Check environment
    check_root
    check_termux
    
    # Installation steps
    update_packages
    install_python
    install_pip
    install_dependencies
    install_tool
    setup_path
    create_shortcut
    create_desktop_entry
    
    # Verify and show results
    if verify_installation; then
        show_usage
        
        # Ask to test immediately
        echo ""
        read -p "Do you want to test the tool now? (y/n): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "\n${GREEN}Starting AM Information Lookup Tool...${RESET}\n"
            sim
        fi
    else
        print_error "There were issues with installation"
        print_info "Try running: $TERMUX_BIN/$TOOL_NAME"
    fi
    
    cleanup
}

# Handle Ctrl+C
trap 'echo -e "\n${YELLOW}Installation interrupted by user${RESET}"; exit 1' INT

# Run main function
main

# Exit with appropriate code
if [ $? -eq 0 ]; then
    exit 0
else
    exit 1
fi
