from pathlib import Path

path = Path("AMY_Market_Context_Final.pine")
text = path.read_text(encoding="utf-8")

replacements = {
    "color.new(color.lime, 86)": "color.new(color.lime, 55)",
    "color.new(color.red, 86)": "color.new(color.red, 55)",
    "color.new(color.blue, 86)": "color.new(color.blue, 55)",
    "color.new(color.orange, 86)": "color.new(color.orange, 55)",
    "color.new(color.yellow, 78)": "color.new(color.yellow, 45)",
    "color.new(color.lime, 78)": "color.new(color.lime, 45)",
    "table.new(position.top_right, 6, 6": "table.new(position.bottom_center, 6, 6",
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f"Expected pattern not found: {old}")
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
print("Updated box opacity and moved dashboard to bottom center.")
