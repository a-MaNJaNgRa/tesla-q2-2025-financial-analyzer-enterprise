def is_valid_pdf(content: bytes) -> bool:
    """
    Validates PDF using magic bytes signature.
    Enterprise-safe minimal validation layer.
    """
    return content.startswith(b"%PDF-")