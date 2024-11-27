import itertools
import os
import re
import pdfkit
from PyPDF2 import PdfMerger
import datetime

PAGE_ITERATOR = itertools.count(start=1, step=1)

SNAPSHOTS_FOLDER = 'snapshots'
PDF_FOLDER = 'pdf'
OTREE_SERVER_URL = "http://127.0.0.1:8000"


def adjust_image_paths(html_file_path: str):
    # Read the HTML file content
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Replace all references to /static/ with the oTree server URL
    updated_content = re.sub(r'(["\'])/static/([^"\']+)', rf'\1{OTREE_SERVER_URL}/static/\2', html_content)

    # Save the updated content back to the same file
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"---Paths adjusted for: {html_file_path}")


def save_html(html_content: str):
    file_path = os.path.join(SNAPSHOTS_FOLDER, f"{next(PAGE_ITERATOR)}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    adjust_image_paths(file_path)


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
        print(f"Created PDF for {html_file_path}")
        pdf_file = os.path.join(PDF_FOLDER, os.path.splitext(os.path.basename(html_file_path))[0] + ".pdf")
        pdfkit.from_file(html_file_path, pdf_file, options={"enable-local-file-access": ""})
        pdf_files.append(pdf_file)
    time_now = datetime.datetime.now().strftime(format="%H_%M")
    output_pdf = os.path.join(PDF_FOLDER, f"combined_output_{time_now}.pdf")
    merger = PdfMerger()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(output_pdf)
    merger.close()

    print(f"Merged PDF created at: {output_pdf}")


if __name__ == "__main__":
    """
    How to use the sceenshot of the experiment:
        1. Run the tests:
            Every tests.py file should contain yield statements after which we should save an html (save_html frunction)
            It will create snapshots of each page of the experment as bot continues
            Note: save_html will already change paths to the elements and images to the corrected ones (to server)
        2. Run the server with otree zipserver (otherwise style and images will not be seen)
        3. Run this script (python ./helpers.py), that will create pdf out of html snapshots made before
    """
    generate_pdf()
