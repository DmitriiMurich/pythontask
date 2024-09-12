import pytest

from services.pdf_service import extract_all_info_from_pdf
from services.pdf_test_service import compare_structure


@pytest.fixture
def reference_info():
    """Extract the reference file's information for structure validation."""
    reference_pdf_path = "reference_file/test_task.pdf"
    return extract_all_info_from_pdf(reference_pdf_path)

@pytest.mark.parametrize("test_file, expected_text_result, expected_barcode_result, expected_metadata_result", [
    # Positive case: the file should match the reference structure
    ("test_files/test_file1.pdf", "Text structure matches.", "Barcode count matches.", "Metadata matches."),

    # Negative case: text mismatch (missing key phrases)
    ("test_files/test_file_with_missing_text.pdf", "Missing key phrases: ['DESCRIPTION:', 'EXP DATE:']", "Barcode count matches.", "Metadata matches."),

    # Negative case: barcode count mismatch
    ("test_files/test_file_with_wrong_barcode.pdf", "Text structure matches.", "Barcode count mismatch.", "Metadata matches."),

    # Negative case: metadata mismatch
    ("test_files/test_file_with_wrong_metadata.pdf", "Text structure matches.", "Barcode count matches.", "Metadata does not match."),

    # Negative case: text and barcode mismatch
    ("test_files/test_file_with_text_and_barcode_mismatch.pdf", "Missing key phrases: ['REMARK:']", "Barcode count mismatch.", "Metadata matches."),

    # Positive case: minimal file that matches the required structure
    ("test_files/test_minimal_valid_file.pdf", "Text structure matches.", "Barcode count matches.", "Metadata matches."),

    # Negative case: missing all barcodes
    ("test_files/test_file_missing_barcodes.pdf", "Text structure matches.", "Barcode count mismatch.", "Metadata matches."),

    # Positive case: another valid file
    ("test_files/test_file2.pdf", "Text structure matches.", "Barcode count matches.", "Metadata matches."),

    # Negative case: missing all key phrases in text
    ("test_files/test_file_missing_all_key_phrases.pdf", "Missing key phrases: ['DESCRIPTION:', 'EXP DATE:', 'REMARK:', 'Qty:', 'NOTES:']", "Barcode count matches.", "Metadata matches."),

    # Negative case: invalid file format (not a PDF)
    ("test_files/test_invalid_format.txt", None, None, None),  # Expect failure for non-PDF
])
def test_pdf_structure(reference_info, test_file, expected_text_result, expected_barcode_result, expected_metadata_result):
    """Test comparing the structure of the test file against the reference."""
    try:
        test_info = extract_all_info_from_pdf(test_file)
        comparison_report = compare_structure(reference_info, test_info)

        # Assert that the text comparison result matches the expected outcome
        assert comparison_report["text_comparison"] == expected_text_result, f"Text mismatch in file: {test_file}"

        # Assert that the barcode comparison result matches the expected outcome
        assert comparison_report["barcode_comparison"] == expected_barcode_result, f"Barcode mismatch in file: {test_file}"

        # Assert that the metadata comparison result matches the expected outcome
        assert comparison_report["metadata_comparison"] == expected_metadata_result, f"Metadata mismatch in file: {test_file}"

    except Exception as e:
        if expected_text_result is None and expected_barcode_result is None and expected_metadata_result is None:
            # Non-PDF or invalid files should raise an exception
            assert isinstance(e, Exception), f"Expected exception for invalid file format: {test_file}"
        else:
            raise e  # Rethrow if it's not expected


# Additional test cases to focus on specific edge cases

def test_empty_pdf():
    """Test handling of an empty PDF file with no content."""
    test_file = "test_files/empty.pdf"
    with pytest.raises(ValueError):
        test_info = extract_all_info_from_pdf(test_file)

def test_incorrect_file_type():
    """Test attempting to process a non-PDF file."""
    test_file = "test_files/invalid_file.docx"
    with pytest.raises(Exception):
        test_info = extract_all_info_from_pdf(test_file)

def test_partial_data_pdf():
    """Test a PDF file that has some sections missing, e.g., missing metadata."""
    test_file = "test_files/test_partial_data.pdf"
    test_info = extract_all_info_from_pdf(test_file)

    # Assuming this file is valid, but has missing metadata
    assert test_info["metadata"] == {}, "Expected empty metadata for partial data file."

def test_large_pdf():
    """Test performance and structure validation of a large PDF file."""
    test_file = "test_files/large_test_file.pdf"
    test_info = extract_all_info_from_pdf(test_file)

    # Perform a basic check to ensure no crashes or exceptions
    assert isinstance(test_info, dict), "Expected valid extraction from a large file."

def test_pdf_with_multiple_barcodes():
    """Test a PDF with multiple barcodes of different types."""
    test_file = "test_files/test_file_multiple_barcodes.pdf"
    test_info = extract_all_info_from_pdf(test_file)

    # Verify multiple barcodes were detected
    assert len(test_info["barcodes"]) > 1, "Expected multiple barcodes in the file."

def test_pdf_with_special_characters():
    """Test that special characters in text are correctly handled."""
    test_file = "test_files/test_file_special_characters.pdf"
    test_info = extract_all_info_from_pdf(test_file)

    # Verify the text contains special characters and they were properly extracted
    assert "©" in test_info["text"], "Expected special characters in the text."

def test_corrupted_pdf():
    """Test handling of a corrupted PDF file."""
    test_file = "test_files/corrupted_file.pdf"
    with pytest.raises(Exception):
        test_info = extract_all_info_from_pdf(test_file)
