import sys
from lifemap.cli import main as cli_main
from lifemap.visualization.web import start_web_interface

def main():
    print("Welcome to the Interactive Life Map!")
    print("Choose an option:")
    print("1. Start CLI")
    print("2. Start Web Interface")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        cli_main()
    elif choice == '2':
        start_web_interface()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()