import re

def extract_episode(text):
    patterns = [
        r"S(\d+)[\s._-]?E(\d+)",
        r"Season\s*(\d+)\s*Episode\s*(\d+)",
        r"E(\d+)"
    ]

    for p in patterns:
        m = re.search(p, text or "", re.IGNORECASE)
        if m:
            if len(m.groups()) == 2:
                return f"S{int(m.group(1)):02d}E{int(m.group(2)):02d}"
            else:
                return f"E{int(m.group(1)):02d}"
    return None


def glow_bar(done, total, speed, status):
    percent = int((done / total) * 100) if total else 0
    blocks = percent // 10

    bar = ""
    for i in range(10):
        if i < blocks:
            bar += "🟩"
        elif i == blocks:
            bar += "🟨"
        else:
            bar += "⬜"

    return f"""**{status}**

{bar} **{percent}%**

⚡ Speed: {speed:.2f} MB/s
📦 {done}/{total}
"""
