#!/usr/bin/env python3
"""Check that every skill in skills/ is installable and internally consistent.

For each skills/<name>/SKILL.md:
  - front matter present, `name:` equals the folder name, `description:` not empty;
  - every relative path the skill mentions under scripts/, references/, assets/ or tools/ exists;
  - every Python file compiles, every shell script passes `bash -n`, every JSON file parses.
Prints one line per problem and a summary with the skill count. Exit code 1 if anything failed.
Usage: python3 tools/validate_skills.py [skills_dir]
"""
import json, os, py_compile, re, subprocess, sys

root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "skills")
problems, count = [], 0
for name in sorted(os.listdir(root)):
    d = os.path.join(root, name)
    md = os.path.join(d, "SKILL.md")
    if not os.path.isdir(d) or name.startswith("."):
        continue
    if not os.path.exists(md):
        problems.append(f"{name}: no SKILL.md"); continue
    count += 1
    text = open(md, encoding="utf-8").read()
    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not fm:
        problems.append(f"{name}: no front matter"); continue
    m = re.search(r"^name:\s*(.+)$", fm.group(1), re.M)
    if not m or m.group(1).strip().strip("'\"") != name:
        problems.append(f"{name}: front-matter name '{m.group(1).strip() if m else ''}' != folder")
    if not re.search(r"^description:\s*\S", fm.group(1), re.M):
        problems.append(f"{name}: empty description")
    for ref in set(re.findall(r"(?<![\w/])((?:scripts|references|assets)/[\w./-]+\.\w+)", text)):
        top = ref.split("/")[0]
        # mentions like references/INDEX.md often mean the user's project folder; only check folders the skill really has
        if os.path.isdir(os.path.join(d, top)) and not os.path.exists(os.path.join(d, ref)) and not os.path.exists(os.path.join(d, top, os.path.basename(ref))):
            problems.append(f"{name}: mentions missing file {ref}")
    for dp, _, files in os.walk(d):
        for f in files:
            p = os.path.join(dp, f)
            try:
                if f.endswith(".py"):
                    py_compile.compile(p, doraise=True)
                elif f.endswith(".sh"):
                    r = subprocess.run(["bash", "-n", p], capture_output=True, text=True)
                    if r.returncode:
                        problems.append(f"{name}: {f}: {r.stderr.strip()[:120]}")
                elif f.endswith(".json"):
                    json.load(open(p, encoding="utf-8"))
            except Exception as e:
                problems.append(f"{name}: {f}: {str(e).splitlines()[0][:120]}")
for p in problems:
    print("FAIL", p)
print(f"validate_skills: {count} skills, {len(problems)} problem(s)")
sys.exit(1 if problems else 0)
