import itertools
import os
import re
import pdfkit
from PyPDF2 import PdfMerger


PAGE_ITERATOR = itertools.count(start=1, step=1)

SNAPSHOTS_FOLDER = 'snapshots'
PDF_FOLDER = 'pdf'
OTREE_SERVER_URL = "http://127.0.0.1:8000"


def save_html(html_content):
    file_path = os.path.join(SNAPSHOTS_FOLDER, f"{next(PAGE_ITERATOR)}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def adjust_image_paths(html_file_path):
    # Read the HTML file content
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Replace all references to /static/ with the oTree server URL
    updated_content = re.sub(r'(["\'])/static/([^"\']+)', rf'\1{OTREE_SERVER_URL}/static/\2', html_content)

    # Save the updated content back to the same file
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"Paths adjusted for: {html_file_path}")


def generate_pdf(output_pdf="experiment_snapshot.pdf"):
    """Combine all HTML files in 'snapshots/' directory into a single PDF."""
    os.makedirs(name=SNAPSHOTS_FOLDER, exist_ok=True)
    os.makedirs(name=PDF_FOLDER, exist_ok=True)
    html_files = sorted(
        [os.path.join(SNAPSHOTS_FOLDER, f) for f in os.listdir(SNAPSHOTS_FOLDER) if f.endswith(".html")],
        key=lambda x: int(os.path.basename(x).split(".")[0])
    )

    pdf_files = []
    for html_file_path in html_files:
        print(html_file_path)
        adjust_image_paths(html_file_path)
        pdf_file = os.path.join(PDF_FOLDER, os.path.splitext(os.path.basename(html_file_path))[0] + ".pdf")
        pdfkit.from_file(html_file_path, pdf_file, options={"enable-local-file-access": ""})
        pdf_files.append(pdf_file)

    output_pdf = os.path.join(PDF_FOLDER, "combined_output.pdf")
    merger = PdfMerger()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(output_pdf)
    merger.close()

    print(f"PDF created at: {output_pdf}")


if __name__ == "__main__":
    generate_pdf()
