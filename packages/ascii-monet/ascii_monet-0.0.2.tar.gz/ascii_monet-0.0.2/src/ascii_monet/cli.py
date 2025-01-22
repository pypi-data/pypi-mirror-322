import sys
from ascii_monet.ascii_monet import ascii_monet  # Import your implementation

def main():
    if len(sys.argv) != 2:
        print("Usage: ascii-monet <image-path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    ascii_monet.generate(image_path)  # Call your main logic
