# run
from services.pdf_service import extract_all_info_from_pdf

pdf_path = 'reference_file/test_task.pdf'
pdf_info = extract_all_info_from_pdf(pdf_path)
print(pdf_info)
