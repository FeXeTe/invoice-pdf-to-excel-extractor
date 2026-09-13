# Invoice PDF to Excel Extractor

Extracts key data (invoice number, date, total, provider) from supplier invoice
PDFs and consolidates them into a single Excel file — no manual data entry.

## The problem

Small businesses that receive invoices from many suppliers usually type the
key data (invoice number, date, amount) into a spreadsheet by hand. It's slow
and error-prone, and it doesn't scale as the number of suppliers grows.

This script automates that step: point it at a folder of invoice PDFs and get
back a clean Excel file with one row per invoice.

![demo](demo.gif)

## How it works

The tricky part isn't reading the PDF — it's that **every supplier formats
their invoice differently**. The invoice number label alone shows up as
`Nº Factura:`, `Factura N°:`, `Núm. factura:`, or `Nº Fra.:` depending on the
provider, and label/value can sit on the same line or different lines.

Instead of trying to match every possible label wording, the extractor
anchors on the **shape of the data** where possible:

- Invoice numbers are matched as "letters/digits joined by `-` or `/`"
  (e.g. `FR-2026-0341`, `EN/0562/26`), combined with label alternation as a
  fallback anchor.
- Dates are matched by their `DD-MM-YYYY` / `DD/MM/YYYY` shape.
- The total is anchored to the literal `TOTAL:` label, since base amount and
  VAT appear nearby with a similar numeric shape and would otherwise be
  ambiguous.

If a field can't be found, the extractor doesn't crash the whole batch — it
records the value as missing (`None`) so the rest of the invoices still get
processed, and the row can be reviewed manually afterwards.

## Usage

```bash
pip install -r requirements.txt
python src/extract_invoices.py
```

This reads the PDFs listed in `INVOICE_FILES` (see `src/extract_invoices.py`)
and writes `facturas_extraidas.xlsx` with one row per invoice.

Sample invoices are included in `sample_invoices/` so you can try it without
any real data.

## Known limitations

- Currently reads only the first page of each PDF.
- The invoice number and date patterns are tuned to the label formats seen so
  far — a supplier using a very different format may need a new pattern
  added to `extract_invoices.py`.
- No OCR: PDFs that are scanned images rather than text won't extract
  correctly.

## Stack

Python · [pdfplumber](https://github.com/jsvine/pdfplumber) · pandas · openpyxl
