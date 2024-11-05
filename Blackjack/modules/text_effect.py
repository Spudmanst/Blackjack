import time
import sys

# Provides a divider and time to read if a lot of text
def divide_and_read():
    divide_lines()
    time.sleep(2)

# Help with splitting screen to make things easier to read where required
def divide_lines():
    print("----------")

# Helper Function for printing player money to specific format
def format_cash(player_cash_value):
    return f"${player_cash_value:.2f}"

def player_payout_format(amount):
    return f"${abs(amount):.2f}"

# Both line and minor delay, indicating new phase
def sleep_line():
    divide_lines()
    std_sleep()

# Provide appearance of computer typing instead of text instantly appearing, slightly quicker 
def slow_input(prompt, delay=0.02):
    slow_type(prompt, delay, end='')  # No newline at the end
    return input()  # Capture user input on the same line

# Provide appearance of computer typing instead of text instantly appearing        
def slow_type(text, delay=0.02, end="\n"):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Flush the output to ensure it prints immediately
        time.sleep(delay)   # Delay between each character
    # Ensure a new line at the end
    if end:
        sys.stdout.write(end)
        sys.stdout.flush() # New line should automatically flush however we will include to ensure accurate behavior

# Minor delay function for gameplay
def std_sleep():
    time.sleep(0.95)

# Longer delay function to provide "suspense"
def sus_sleep():
    time.sleep(1.5)    