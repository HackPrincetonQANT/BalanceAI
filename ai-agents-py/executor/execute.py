import json, re
from lib.files import read_text, write_text

PLAN_PATH = "ai-agents-py/planner/plans/plan.md"

"""
Minimal executor: looks for a JSON array fenced block in plan.md like:
```json
[
  {"path": "executor/out/pages/archive.py", "contents": "# stub"},
  {"path": "executor/out/lib/queue.py", "contents": "# stub"}
]
```
and writes those files. Keep it safe and additive.
"""
def extract_json_blocks(text: str):
    # Capture content inside fenced JSON code blocks: ```json ... ```
    blocks = re.findall(r"```json\s*(.*?)```", text, flags=re.S)
    return blocks

def main():
    plan = read_text(PLAN_PATH)
    blocks = extract_json_blocks(plan)
    if not blocks:
        print("No JSON scaffold block found in plan.md. Nothing to do.")
        return

    for blk in blocks:
        try:
            arr = json.loads(blk)
        except json.JSONDecodeError:
            continue
        if not isinstance(arr, list):
            continue

        for item in arr:
            p = item.get("path")
            c = item.get("contents", "")
            if p:
                write_text(f"ai-agents-py/{p}", c)
                print("✍️ wrote", f"ai-agents-py/{p}")

if __name__ == "__main__":
    main()
