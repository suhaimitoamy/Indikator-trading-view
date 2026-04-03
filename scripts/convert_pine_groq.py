import os
from pathlib import Path
from openai import OpenAI

API_KEY = os.environ["GROQ_API_KEY"]
INPUT_FILE = os.environ["INPUT_FILE"].strip()
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", "").strip()

if not INPUT_FILE:
    raise SystemExit("INPUT_FILE kosong.")

input_path = Path(INPUT_FILE)
if not input_path.exists():
    raise SystemExit(f"File tidak ditemukan: {INPUT_FILE}")

if not OUTPUT_FILE:
    if input_path.suffix:
        OUTPUT_FILE = str(input_path.with_name(f"{input_path.stem}_v4{input_path.suffix}"))
    else:
        OUTPUT_FILE = str(input_path.with_name(f"{input_path.name}_v4.pine"))

output_path = Path(OUTPUT_FILE)
output_path.parent.mkdir(parents=True, exist_ok=True)

source_code = input_path.read_text(encoding="utf-8", errors="ignore")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

system_prompt = """You are an expert Pine Script migration assistant.
Convert Pine Script v3 code to Pine Script v4.

Rules:
- Keep behavior the same
- Return ONLY code
- No markdown
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": source_code},
    ],
    temperature=0.2,
)

result = response.choices[0].message.content.strip()

# bersihin kalau ada ```
if result.startswith("```"):
    result = "\n".join(result.splitlines()[1:-1])

output_path.write_text(result, encoding="utf-8")

print(f"Saved: {OUTPUT_FILE}")
