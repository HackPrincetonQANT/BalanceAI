import os
from pathlib import Path
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

TARGET_URL = os.getenv("TARGET_URL", "http://localhost:3000")
READY_SELECTOR = os.getenv("READY_SELECTOR", "body")
OUT_DIR = Path("ai-agents-py/reviewer/artifacts")
REF_DIR = Path("ai-agents-py/reviewer/reference")
THRESHOLD = float(os.getenv("THRESHOLD", "0.01"))  # 1%

VIEWPORTS = [
  ("desktop", 1440, 900),
  ("mobile" , 390 , 844),
]

def mismatch_ratio(im1: Image.Image, im2: Image.Image) -> float:
  if im1.size != im2.size:
    im2 = im2.resize(im1.size)
  diff = ImageChops.difference(im1, im2).convert("L")
  total = diff.size[0] * diff.size[1]
  nonzero = sum(1 for px in diff.getdata() if px != 0)
  return nonzero / total

def screenshot(url: str, width: int, height: int, out_path: Path, ready: str):
  with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": width, "height": height, "deviceScaleFactor": 1})
    page.goto(url, wait_until="networkidle")
    page.wait_for_selector(ready, timeout=20000)
    page.screenshot(path=str(out_path), full_page=True)
    browser.close()

def main():
  OUT_DIR.mkdir(parents=True, exist_ok=True)
  report = ["# Visual Review Report\n"]
  for label, w, h in VIEWPORTS:
    actual = OUT_DIR / f"actual-{label}.png"
    diffp  = OUT_DIR / f"diff-{label}.png"
    ref    = REF_DIR / f"{label}.png"
    # take screenshot
    screenshot(TARGET_URL, w, h, actual, READY_SELECTOR)
    if not ref.exists():
      report.append(f"### {label}\nReference not found at {ref}. Skipping.\n")
      continue
    a = Image.open(actual).convert("RGBA")
    r = Image.open(ref).convert("RGBA")
    # compute mismatch
    ratio = mismatch_ratio(a, r)
    # save a visual diff
    d = ImageChops.difference(a, r)
    d.save(diffp)
    status = "❌ Fail" if ratio > THRESHOLD else "✅ Pass"
    pct = round(ratio * 100, 2)
    report.append(f"### {label}\n- Mismatch: **{pct}%** ({status})\n- Actual: {actual}\n- Reference: {ref}\n- Diff: {diffp}\n")

  report.append("\n---\n## Hints\n- Check spacing scale / container widths\n- Verify fonts and line-height vs. tokens\n- Check color tokens/border opacity\n- Ensure component variants match your design system\n")
  (OUT_DIR / "report.md").write_text("\n".join(report), encoding="utf-8")
  print(f"✅ wrote {(OUT_DIR/'report.md').as_posix()}")

if __name__ == "__main__":
  main()
