import subprocess
import os

def main():
    # Get git root
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
    sdd_dir = os.path.join(root, ".superpowers", "sdd")
    os.makedirs(sdd_dir, exist_ok=True)
    with open(os.path.join(sdd_dir, ".gitignore"), "w", encoding="utf-8") as f:
        f.write("*\n")
    print(os.path.abspath(sdd_dir))

if __name__ == "__main__":
    main()
