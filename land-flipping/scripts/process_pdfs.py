import sys
import os
import math
import fitz


def chunk_text(text, max_chars=30000):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            newline = text.rfind("\n", start, end)
            if newline != -1 and newline > start:
                end = newline
        chunks.append(text[start:end])
        start = end
    return chunks


def process_pdf(pdf_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    all_text = []
    for page in doc:
        all_text.append(page.get_text("text"))
    text = "\n".join(all_text)
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks, 1):
        out_path = os.path.join(out_dir, f"{base}-chunk-{i:03}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(chunk)
    print(f"Wrote {len(chunks)} chunks to {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: process_pdfs.py <pdf_path> <out_dir>")
        sys.exit(1)
    process_pdf(sys.argv[1], sys.argv[2])
