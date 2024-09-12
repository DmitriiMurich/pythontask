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
        report["text_comparison"] = f"Missing key phrases: {missing_phrases}"
    else:
        report["text_comparison"] = "Text structure passed."

    # Compare barcodes
    reference_barcodes = reference_info["barcodes"]
    test_barcodes = test_info["barcodes"]

    if len(reference_barcodes) != len(test_barcodes):
        report["barcode_comparison"] = "Number of barcodes not passed."
    else:
        report["barcode_comparison"] = "Number of barcodes passed."

    # Compare metadata
    reference_metadata = reference_info["metadata"]
    test_metadata = test_info["metadata"]

    if reference_metadata != test_metadata:
        report["metadata_comparison"] = "Metadata not passed."
    else:
        report["metadata_comparison"] = "Metadata passed."

    return report