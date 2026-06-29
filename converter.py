import sys
import os

def main():
    if len(sys.argv) != 3:
        print("Sposób użycia: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)
    
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    print(f"Wczytywanie: {in_file} -> Zapis: {out_file}")

if __name__ == "__main__":
    main()
