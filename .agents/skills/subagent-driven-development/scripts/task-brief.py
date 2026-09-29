import sys
import os
import re
import subprocess

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("usage: task-brief PLAN_FILE TASK_NUMBER [OUTFILE]", file=sys.stderr)
        sys.exit(2)
        
    plan_file = sys.argv[1]
    task_num = sys.argv[2]
    
    if not os.path.isfile(plan_file):
        print(f"no such plan file: {plan_file}", file=sys.stderr)
        sys.exit(2)
        
    if len(sys.argv) == 4:
        outfile = sys.argv[3]
    else:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
        sdd_dir = os.path.join(root, ".superpowers", "sdd")
        os.makedirs(sdd_dir, exist_ok=True)
        with open(os.path.join(sdd_dir, ".gitignore"), "w", encoding="utf-8") as f:
            f.write("*\n")
        outfile = os.path.join(sdd_dir, f"task-{task_num}-brief.md")
        
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = content.splitlines()
    in_fence = False
    in_task = False
    task_lines = []
    
    task_header_re = re.compile(r'^#+\s+Task\s+(\d+)(?:\D|$)')
    any_task_header_re = re.compile(r'^#+\s+Task\s+(\d+)')
    
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
            
        if not in_fence:
            m = task_header_re.match(line)
            m_any = any_task_header_re.match(line)
            if m:
                if m.group(1) == task_num:
                    in_task = True
                elif in_task:
                    in_task = False
            elif m_any and in_task:
                in_task = False
                
        if in_task:
            task_lines.append(line)
            
    if not task_lines:
        print(f"task {task_num} not found in {plan_file} (no heading matching 'Task {task_num}')", file=sys.stderr)
        sys.exit(3)
        
    with open(outfile, "w", encoding="utf-8") as f:
        f.write("\n".join(task_lines) + "\n")
        
    print(f"wrote {outfile}: {len(task_lines)} lines")

if __name__ == "__main__":
    main()
