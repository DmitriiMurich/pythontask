# Test service pytest

def compare_structure(reference_info, test_info):
    """Compare structure"""
    report = {
        "text_comparison": None,
        "barcode_comparison": None,
        "metadata_comparison": None
    }

    # Compare text structure
    reference_text = reference_info["text"]
    test_text = test_info["text"]

    # Compare by keys
    key_phrases = ["DESCRIPTION:", "EXP DATE:", "REMARK:", "Qty:", "NOTES:"]
    missing_phrases = []
    for phrase in key_phrases:
        if phrase not in test_text:
            missing_phrases.append(phrase)
    if missing_phrases:
        report["text_comparison"] = f"Отсутствуют ключевые фразы: {missing_phrases}"
    else:
        report["text_comparison"] = "Текстовая структура совпадает."

    # Compare barcodes
    reference_barcodes = reference_info["barcodes"]
    test_barcodes = test_info["barcodes"]

    if len(reference_barcodes) != len(test_barcodes):
        report["barcode_comparison"] = "Несовпадение количества штрих-кодов."
    else:
        report["barcode_comparison"] = "Количество штрих-кодов совпадает."

    # Compare metadata
    reference_metadata = reference_info["metadata"]
    test_metadata = test_info["metadata"]

    if reference_metadata != test_metadata:
        report["metadata_comparison"] = "Метаданные не совпадают."
    else:
        report["metadata_comparison"] = "Метаданные совпадают."

    return report