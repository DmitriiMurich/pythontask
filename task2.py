import pytest

from services.pdf_service import extract_all_info_from_pdf
from services.pdf_test_service import compare_structure


# Tests on pytest

@pytest.fixture
def reference_info():
    """Reference file"""
    reference_pdf_path = "reference_file/test_task.pdf"
    return extract_all_info_from_pdf(reference_pdf_path)

@pytest.mark.parametrize("test_file", [
    "test_files/test_file1.pdf",
    "test_files/test_file2.pdf"
])
def test_pdf_structure(reference_info, test_file):
    test_info = extract_all_info_from_pdf(test_file)
    comparison_report = compare_structure(reference_info, test_info)

    # Assert text structure
    assert comparison_report["text_comparison"] == "Текстовая структура совпадает.", comparison_report["text_comparison"]

    # Assert barcodes
    assert comparison_report["barcode_comparison"] == "Количество штрих-кодов совпадает.", comparison_report["barcode_comparison"]

    # Assert metadata
    assert comparison_report["metadata_comparison"] == "Метаданные совпадают.", comparison_report["metadata_comparison"]