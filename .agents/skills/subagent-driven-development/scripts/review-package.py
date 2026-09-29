import sys
import os
import subprocess

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("usage: review-package BASE HEAD [OUTFILE]", file=sys.stderr)
        sys.exit(2)
        
    base = sys.argv[1]
    head = sys.argv[2]
    
    # Verify git refs
    try:
        subprocess.check_call(["git", "rev-parse", "--verify", "--quiet", base], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"bad BASE: {base}", file=sys.stderr)
        sys.exit(2)
        
    try:
        subprocess.check_call(["git", "rev-parse", "--verify", "--quiet", head], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"bad HEAD: {head}", file=sys.stderr)
        sys.exit(2)
        
    if len(sys.argv) == 4:
        outfile = sys.argv[3]
    else:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
        sdd_dir = os.path.join(root, ".superpowers", "sdd")
        os.makedirs(sdd_dir, exist_ok=True)
        with open(os.path.join(sdd_dir, ".gitignore"), "w", encoding="utf-8") as f:
            f.write("*\n")
            
        base_short = subprocess.check_output(["git", "rev-parse", "--short", base]).decode("utf-8").strip()
        head_short = subprocess.check_output(["git", "rev-parse", "--short", head]).decode("utf-8").strip()
        outfile = os.path.join(sdd_dir, f"review-{base_short}..{head_short}.diff")
        
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(f"# Review package: {base}..{head}\n\n")
        
        f.write("## Commits\n")
        commits_log = subprocess.check_output(["git", "log", "--oneline", f"{base}..{head}"]).decode("utf-8")
        f.write(commits_log)
        f.write("\n")
        
        f.write("## Files changed\n")
        diff_stat = subprocess.check_output(["git", "diff", "--stat", f"{base}..{head}"]).decode("utf-8")
        f.write(diff_stat)
        f.write("\n")
        
        f.write("## Diff\n")
        diff_u10 = subprocess.check_output(["git", "diff", "-U10", f"{base}..{head}"]).decode("utf-8")
        f.write(diff_u10)
        f.write("\n")
        
    commits_count = subprocess.check_output(["git", "rev-list", "--count", f"{base}..{head}"]).decode("utf-8").strip()
    bytes_count = os.path.getsize(outfile)
    print(f"wrote {outfile}: {commits_count} commit(s), {bytes_count} bytes")

if __name__ == "__main__":
    main()
