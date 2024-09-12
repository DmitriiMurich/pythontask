# task1
1. Add a pdf file to **reference_file** directory (if not there yet) 
2. Run task1.py

# task2
**The pytest structure**

test_pdf_comparison.py

reference_file/test_task.pdf

test_files/

1. Add tested files for different scenario to test_files directory, if not there yet.
- **positive scenario** test_file1.pdf and test_file2.pdf are the same as test_task.pdf.

- Add test files for **negative scenario** test_file_with_missing_text.pdf, test_file_with_wrong_barcode.pdf, test_file_with_wrong_metadata.pdf, test_file_with_text_and_barcode_mismatch.pdf, test_minimal_valid_file.pdf, test_file_missing_barcodes.pdf, test_file_missing_all_key_phrases.pdf, test_invalid_format.txt, empty.pdf, invalid_file.docx, test_partial_data.pdf, large_test_file.pdf, test_file_multiple_barcodes.pdf, test_file_special_characters.pdf, corrupted_file.pdf

2. Run **test_pdf_comparison.py** or run **pytest -v** in a root project directory

# task3

Run task3.py
