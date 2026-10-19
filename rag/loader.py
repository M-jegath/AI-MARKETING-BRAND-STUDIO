
from pypdf import PdfReader
from io import BytesIO


def load_brand_guide(uploaded_file):
    """
    Read a PDF or TXT brand guide uploaded through Streamlit.
    Return the extracted text.
    """

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        pdf = PdfReader(BytesIO(uploaded_file.getvalue()))

        pages = []

        for page in pdf.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        content = "\n".join(pages)

    elif filename.endswith(".txt"):
        content = uploaded_file.getvalue().decode(
            "utf-8",
            errors="replace"
        )

    else:
        raise ValueError("Please upload a PDF or TXT file.")

    if not content.strip():
        raise ValueError(
            "No readable text found in the brand guide."
        )

    return content
