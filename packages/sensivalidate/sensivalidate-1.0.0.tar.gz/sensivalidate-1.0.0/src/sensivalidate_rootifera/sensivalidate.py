import re
import creditcard

"""
this script finds sensitive data in a text. the only real validation it does is the credit card number.
if you try a random 16 digit number (i.e 1234123412341234) it wouldn't catch it because this is not a 
valid credit card number. UK bank account number, sort code and UK postcode are all just pattern match. So, if 
you try 12-12-12 then this get flagged as sort code even though it is not a real sort code.

All the regex are from ChatGPT, if you have any questions I don't have the answers.  
"""


def _is_credit_card(text):
    """searches for credit card number in the text and checks if it is a valid credit card number,
    it extracts the digits from the text and make sure there is no hidden card numbers passed"""

    digits = re.findall(r'\d', text)

    for i in range(len(digits) - 15):
        card_number = ''.join(digits[i:i + 16])

        try:
            card = creditcard.CreditCard(number=card_number)
            if card.is_valid:
                return True
        except Exception as e:
            pass

    return False


def _is_uk_bank_account_and_sort_code(text):
    """searches for UK bank account number or sort code in the text. Account number is just standard 8 digits,
    sort code matches 6 digits of xxxxxx, xx-xx-xx or xx xx xx"""

    bank_account_pattern = r"\b\d{8}\b"
    sort_code_pattern = r"\b\d{2}-\d{2}-\d{2}\b|\b\d{6}\b|\b\d{2}\s\d{2}\s\d{2}\b"

    bank_accounts = re.findall(bank_account_pattern, text)
    sort_codes = re.findall(sort_code_pattern, text)

    if bank_accounts or sort_codes:
        return True

    return False


def _is_uk_postcode(text):
    """searches for UK postcodes. I got the UK postcode definition from wikipedia."""

    postcode_pattern = r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b"

    postcodes = re.findall(postcode_pattern, text)

    if postcodes:
        return True

    return False


def is_sensitive_data(text):
    """checks the given text against all validator functions. If any of the validators returns true then
      this function will return true without running rest of the validation functions"""

    if _is_credit_card(text):
        return True

    if _is_uk_bank_account_and_sort_code(text):
        return True

    if _is_uk_postcode(text):
        return True

    return False
