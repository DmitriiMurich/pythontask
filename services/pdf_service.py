import fitz
from PIL import Image
import io
from pyzbar.pyzbar import decode
import PyPDF2


def extract_images_from_pdf(pdf_path):
    """extract imaged from PDF"""
    images = []
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        page = doc.load_page(i)
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    return images

def decode_barcodes(images):
    """Decode barcodes"""
    barcodes = []
    for image in images:
        decoded_objects = decode(image)
        for obj in decoded_objects:
            barcode_data = {
                "type": obj.type,
                "data": obj.data.decode("utf-8"),
                "rect": obj.rect
            }
            barcodes.append(barcode_data)
    return barcodes

def extract_text_from_pdf(file_path):
    """Estract text and metadata from PDF"""
    result = {
        "text": "",
        "metadata": {}
    }
    # Open and read tha pdf file
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        # Extract text
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        result["text"] = text

        # Extract metadata
        metadata = reader.metadata
        if metadata:
            for key, value in metadata.items():
                result["metadata"][key] = value

    return result

def extract_all_info_from_pdf(pdf_path):
    # Extract text and metadata
    text_and_metadata = extract_text_from_pdf(pdf_path)

    # extract images and barcodes
    images = extract_images_from_pdf(pdf_path)
    barcodes = decode_barcodes(images)

    result = {
        "text": text_and_metadata["text"],
        "metadata": text_and_metadata["metadata"],
        "barcodes": barcodes
    }

    return result