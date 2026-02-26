mkdir -p app/utils
cat > app/utils/pdf_validator.py << 'EOF'
def is_valid_pdf(content: bytes) -> bool:
    return content.startswith(b"%PDF-")
EOF
