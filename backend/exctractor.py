import os
import pandas as pd
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
import pypdf


def iter_block_items(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("Unsupported parent type")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def extract_docx(path):
    doc = Document(path)
    full_text = []
    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            if block.text.strip():
                full_text.append(block.text)
        elif isinstance(block, Table):
            full_text.append("[TABLE]")
            for row in block.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells)
                full_text.append(row_text)
            full_text.append("[/TABLE]")
    return "\n".join(full_text)


def extract_pdf(path):
    reader = pypdf.PdfReader(path)
    full_text = []
    for i, page in enumerate(reader.pages):
        full_text.append(f"[PAGE {i+1}]\n{page.extract_text()}")
    return "\n".join(full_text)


def extract_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_excel(path):
    """
    Returns row-by-row text, one 'record' per row, so each row
    can later become its own chunk (e.g. one RFI, one schedule task).
    """
    df = pd.read_excel(path)
    records = []
    for i, row in df.iterrows():
        row_text = " | ".join(f"{col}: {row[col]}" for col in df.columns)
        records.append(row_text)
    return "\n".join(records)


def extract_file(path):
    """
    Universal entry point. Detects file type by extension,
    returns normalized text + metadata dict.
    """
    ext = os.path.splitext(path)[1].lower()

    if ext == ".docx":
        text = extract_docx(path)
        doc_type = "unstructured"
    elif ext == ".pdf":
        text = extract_pdf(path)
        doc_type = "unstructured"
    elif ext in [".txt", ".md"]:
        text = extract_txt(path)
        doc_type = "unstructured"
    elif ext in [".xlsx", ".xls", ".csv"]:
        text = extract_excel(path)
        doc_type = "structured"
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return {
        "filename": os.path.basename(path),
        "filetype": ext,
        "doc_type": doc_type,   # "structured" vs "unstructured" — you'll use this to route later
        "text": text,
    }