import re
from pathlib import Path

import pandas as pd
import pdfplumber

SAMPLE_INVOICES_DIR = Path("sample_invoices")
INVOICE_FILES = [
    SAMPLE_INVOICES_DIR / "factura_transportes_ruiz.pdf",
    SAMPLE_INVOICES_DIR / "factura_suministros_delta.pdf",
    SAMPLE_INVOICES_DIR / "factura_carnica_montero.pdf",
    SAMPLE_INVOICES_DIR / "factura_limpieza_iberica.pdf",
    SAMPLE_INVOICES_DIR / "factura_embalajes_norte.pdf",
]

INVOICE_NUMBER_PATTERN = r"(?:Nº Factura|Factura N°|Núm\.? factura|Nº Fra.|Factura):?\s*\n?\s*([A-Z0-9]+(?:[-/][A-Z0-9]+)+)"
DATE_PATTERN = r"([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})"
TOTAL_PATTERN = r"TOTAL:\s*(\d+\.\d+)"


def extract_field(text, pattern):
    """Return the first captured group matching `pattern` in `text`,
    or "No match found" if the pattern isn't present."""
    match = re.search(pattern, text)
    return match.group(1) if match else "No match found"


def safe_float(value):
    """Convert `value` to float, returning None instead of raising
    when the value can't be converted (e.g. "No match found")."""
    try:
        return float(value)
    except ValueError:
        return None

def parse_invoice(filepath):
    with pdfplumber.open(filepath) as pdf:
        text = pdf.pages[0].extract_text()

    return {
        "file": filepath.name,
        "invoice_number": extract_field(text, INVOICE_NUMBER_PATTERN),
        "date": extract_field(text, DATE_PATTERN),
        "total": safe_float(extract_field(text, TOTAL_PATTERN)),
        # Assumes the provider's name is the first line of the PDF text
        "provider": text.splitlines()[0].strip() if text else "No provider found"
    }

def main():
    results = [parse_invoice(filepath) for filepath in INVOICE_FILES]

    df = pd.DataFrame(results)
    Path("output").mkdir(exist_ok=True)
    df.to_excel(Path("output") / "facturas_extraidas.xlsx", index=False)
    print(df)


if __name__ == "__main__":
    main()