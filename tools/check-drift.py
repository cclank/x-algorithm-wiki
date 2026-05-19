#!/usr/bin/env python3
"""检测 x-algorithm-wiki 相对上游源码的漂移。

wiki 的所有结论锚定在 xai-org/x-algorithm @ commit 0bfc279。
本脚本检查两件事:
  1. 上游源码仓库是否已超出该锚定 commit;
  2. 每个 `文件:行号` 源码锚点是否仍落在对应文件的行数范围内。

用法:  python3 tools/check-drift.py [x-algorithm 仓库路径]
       默认源码仓库为 wiki 同级目录的 ../x-algorithm
退出码:0 = 无漂移;1 = 发现漂移 / 源码仓库缺失。
"""
import re, glob, os, sys, subprocess

PINNED = "0bfc279"
WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 \
      else os.path.join(os.path.dirname(WIKI), "x-algorithm")


def git(*args, timeout=60):
    try:
        r = subprocess.run(["git", "-C", SRC, *args],
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


print(f"wiki  : {WIKI}")
print(f"source: {SRC}")
if not os.path.isdir(os.path.join(SRC, ".git")):
    print(f"\n!! 未找到源码仓库。用法:python3 tools/check-drift.py /path/to/x-algorithm")
    sys.exit(1)

drift = False

# ---- 1. 上游 commit 检查 ----
print(f"\n[1] 上游版本")
head = git("rev-parse", "--short", "HEAD")
print(f"  wiki 锚定 : {PINNED}")
print(f"  本地 HEAD : {head or '(未知)'}")
subprocess.run(["git", "-C", SRC, "fetch", "--quiet"],
               capture_output=True, timeout=120)
remote = git("rev-parse", "--short", "origin/main") or \
         git("rev-parse", "--short", "origin/master")
print(f"  上游最新 : {remote or '(无法获取,可能离线)'}")

changed = []
def same(a, b):
    return bool(a) and bool(b) and (a.startswith(b) or b.startswith(a))

if head and not same(head, PINNED):
    changed = [l for l in git("diff", "--name-only", f"{PINNED}..HEAD").splitlines() if l]
    print(f"  ⚠ 本地源码已超出锚定版本 —— {len(changed)} 个文件相对 {PINNED} 有变动")
    drift = True
elif remote and not same(remote, PINNED):
    print(f"  ⚠ 上游有新提交(本地仍在 {PINNED})")
    print(f"     `git -C {SRC} pull` 后重跑本脚本,即可看锚点是否漂移")
else:
    print(f"  ✓ 与锚定版本一致")

# ---- 2. 源码锚点行号有效性 ----
print(f"\n[2] 源码锚点")
allsrc = []
for root, _, files in os.walk(SRC):
    if os.sep + ".git" in root:
        continue
    for fn in files:
        if fn.endswith((".rs", ".py")):
            allsrc.append(os.path.relpath(os.path.join(root, fn), SRC))

anchor_re = re.compile(r"([A-Za-z0-9_][A-Za-z0-9_./\-]*\.(?:rs|py)):(\d+)(?:[-–](\d+))?")
pages = glob.glob(os.path.join(WIKI, "concepts", "*.md")) \
      + glob.glob(os.path.join(WIKI, "entities", "*.md")) \
      + glob.glob(os.path.join(WIKI, "guide", "*.md"))
total = bad = 0
issues = []
linecache = {}
for page in pages:
    txt = open(page, encoding="utf-8").read()
    for m in anchor_re.finditer(txt):
        path, l1, l2 = m.group(1), int(m.group(2)), m.group(3)
        total += 1
        hi = int(l2) if l2 else l1
        cands = [s for s in allsrc if s == path or s.endswith("/" + path)]
        if not cands:
            bad += 1
            issues.append((os.path.basename(page), m.group(0), "源码文件已不存在"))
            continue
        mx = 0
        for c in cands:
            if c not in linecache:
                linecache[c] = len(open(os.path.join(SRC, c),
                                       encoding="utf-8", errors="ignore").readlines())
            mx = max(mx, linecache[c])
        if hi > mx:
            bad += 1
            issues.append((os.path.basename(page), m.group(0),
                            f"行 {hi} 超出文件(现有 {mx} 行)"))
print(f"  共 {total} 个锚点,{bad} 个失效")
for pg, anc, why in issues:
    print(f"  ⚠ {pg}: `{anc}` —— {why}")
if bad:
    drift = True

# ---- 3. 变动文件 → 受影响 wiki 页 ----
if changed:
    print(f"\n[3] 受上游变动影响、建议复核的 wiki 页")
    srcbn = {os.path.basename(c): c for c in changed}
    hit = {}
    for page in pages:
        txt = open(page, encoding="utf-8").read()
        for bn in srcbn:
            if bn in txt:
                hit.setdefault(os.path.basename(page), set()).add(bn)
    if hit:
        for pg, bns in sorted(hit.items()):
            print(f"  · {pg} —— 引用了变动文件:{', '.join(sorted(bns))}")
    else:
        print(f"  (变动文件均未被任何 wiki 页引用)")

print(f"\n{'⚠ 发现漂移,见上。' if drift else '✓ 无漂移,wiki 与锚定源码一致。'}")
sys.exit(1 if drift else 0)
