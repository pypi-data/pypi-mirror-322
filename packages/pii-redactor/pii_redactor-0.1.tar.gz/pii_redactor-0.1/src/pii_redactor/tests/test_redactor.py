import pytest
from pii_redactor.pii_redactor import PIIRedactor  # Correct module path

def test_email_redaction():
    redactor = PIIRedactor()
    text = "Contact: john@example.com"
    pii_data = redactor.detect_pii(text)
    assert "email" in pii_data
    assert len(pii_data["email"]) == 1

def test_phone_redaction():
    redactor = PIIRedactor()
    text = "Call +1 (555) 123-4567"
    pii_data = redactor.detect_pii(text)
    assert "phone" in pii_data
    assert len(pii_data["phone"]) == 1