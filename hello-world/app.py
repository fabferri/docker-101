#!/usr/bin/env python3
"""
Simple Hello World application for Docker demonstration
"""

import datetime

def main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 50)
    print("Hello from Docker!")
    print(f"Current time: {current_time}")
    print("=" * 50)
    print("\nThis is a simple Python application running in a Docker container.")
    print("If you can see this message, your Docker setup is working correctly!")

if __name__ == "__main__":
    main()
