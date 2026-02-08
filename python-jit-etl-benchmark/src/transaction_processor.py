"""
Transaction ETL Processor - Benchmarking Python JIT Performance

This module processes financial transaction records through validation,
enrichment, and normalization steps. It's designed to stress-test pure-Python
code paths that benefit from JIT compilation.

Author: Your Name
Date: February 2026
"""

import csv
import json
from datetime import datetime
from typing import Dict, Tuple, Optional
import sys

# Currency metadata
CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
}

COUNTRY_TO_REGION = {
    'US': 'North America',
    'CA': 'North America',
    'MX': 'North America',
    'GB': 'Europe',
    'DE': 'Europe',
    'FR': 'Europe',
    'JP': 'Asia',
    'CN': 'Asia',
    'IN': 'Asia',
    'BR': 'South America',
    'AU': 'Oceania',
}

TAX_RATES = {
    'US': 0.07,
    'CA': 0.13,
    'GB': 0.20,
    'DE': 0.19,
    'FR': 0.20,
    'JP': 0.10,
    'CN': 0.13,
    'IN': 0.18,
    'BR': 0.17,
    'AU': 0.10,
}


def validate_transaction(record: Dict) -> bool:
    """
    Validates transaction record against 47 business rules.
    
    This function is intentionally pure Python with lots of conditional logic,
    string manipulation, and type checking - perfect for JIT optimization.
    
    Args:
        record: Dictionary containing transaction data
        
    Returns:
        True if valid, False otherwise
    """
    
    # Rule 1-4: Currency validation
    if not record.get('currency'):
        return False
    if record.get('currency') not in ['USD', 'EUR', 'GBP', 'JPY']:
        return False
    
    # Rule 5-10: Amount validation
    try:
        amount = float(record.get('amount', 0))
    except (ValueError, TypeError):
        return False
    
    if amount <= 0:
        return False
    if amount > 1_000_000:  # Max transaction limit
        return False
    if amount != round(amount, 2):  # Must have max 2 decimal places
        return False
    
    # Rule 11-15: Date/timestamp validation
    try:
        date_str = record.get('timestamp', '')
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        # Must be within last 2 years
        days_old = (datetime.now() - parsed_date).days
        if days_old < 0 or days_old > 730:
            return False
    except (ValueError, TypeError, AttributeError):
        return False
    
    # Rule 16-20: Merchant ID validation
    merchant_id = record.get('merchant_id', '')
    if not merchant_id:
        return False
    if len(merchant_id) != 12:
        return False
    if not merchant_id.isalnum():
        return False
    if not merchant_id[0].isupper():  # Must start with uppercase
        return False
    
    # Rule 21-25: Customer ID validation
    customer_id = record.get('customer_id', '')
    if not customer_id:
        return False
    if len(customer_id) < 8 or len(customer_id) > 20:
        return False
    
    # Rule 26-30: Transaction type validation
    txn_type = record.get('transaction_type', '').lower()
    valid_types = ['purchase', 'refund', 'authorization', 'capture', 'void']
    if txn_type not in valid_types:
        return False
    
    # Rule 31-35: Country code validation
    country = record.get('country', '')
    if not country:
        return False
    if len(country) != 2:
        return False
    if not country.isupper():
        return False
    
    # Rule 36-40: Payment method validation
    payment_method = record.get('payment_method', '').lower()
    valid_methods = ['credit_card', 'debit_card', 'bank_transfer', 'digital_wallet']
    if payment_method not in valid_methods:
        return False
    
    # Rule 41-43: Status validation
    status = record.get('status', '').lower()
    if status not in ['pending', 'completed', 'failed', 'cancelled']:
        return False
    
    # Rule 44-45: Refund validation
    if txn_type == 'refund':
        original_txn = record.get('original_transaction_id', '')
        if not original_txn or len(original_txn) < 10:
            return False
    
    # Rule 46: Email format basic check
    email = record.get('customer_email', '')
    if '@' not in email or '.' not in email:
        return False
    
    # Rule 47: Card last 4 digits validation (if credit/debit card)
    if payment_method in ['credit_card', 'debit_card']:
        last4 = record.get('card_last4', '')
        if not last4 or len(last4) != 4 or not last4.isdigit():
            return False
    
    return True


def enrich_transaction(record: Dict) -> Dict:
    """
    Enriches transaction record with additional metadata.
    
    Lots of string formatting, lookups, and calculations - all pure Python.
    
    Args:
        record: Validated transaction record
        
    Returns:
        Enriched record with additional fields
    """
    enriched = record.copy()
    
    # Add processing metadata
    enriched['processed_at'] = datetime.utcnow().isoformat()
    enriched['processor_version'] = '1.0.0'
    
    # Currency formatting
    currency = record.get('currency', 'USD')
    symbol = CURRENCY_SYMBOLS.get(currency, '$')
    amount = float(record.get('amount', 0))
    enriched['currency_symbol'] = symbol
    enriched['amount_formatted'] = f"{symbol}{amount:,.2f}"
    
    # Geographic enrichment
    country_code = record.get('country', 'US')
    enriched['region'] = COUNTRY_TO_REGION.get(country_code, 'Unknown')
    enriched['tax_rate'] = TAX_RATES.get(country_code, 0.0)
    enriched['tax_amount'] = round(amount * enriched['tax_rate'], 2)
    enriched['total_amount'] = round(amount + enriched['tax_amount'], 2)
    
    # Risk scoring (simplified model)
    risk_score = 0
    
    # High amount increases risk
    if amount > 10000:
        risk_score += 30
    elif amount > 5000:
        risk_score += 20
    elif amount > 1000:
        risk_score += 10
    
    # New customer increases risk
    customer_age_days = int(record.get('customer_age_days', 365))
    if customer_age_days < 30:
        risk_score += 40
    elif customer_age_days < 90:
        risk_score += 20
    
    # International transaction increases risk
    if country_code not in ['US', 'CA', 'GB']:
        risk_score += 15
    
    # Payment method risk
    payment_method = record.get('payment_method', '')
    if payment_method == 'digital_wallet':
        risk_score += 5
    
    # Assign risk level
    if risk_score > 50:
        enriched['risk_level'] = 'high'
    elif risk_score > 20:
        enriched['risk_level'] = 'medium'
    else:
        enriched['risk_level'] = 'low'
    
    enriched['risk_score'] = risk_score
    
    # Transaction categorization
    amount_category = 'micro' if amount < 10 else \
                     'small' if amount < 100 else \
                     'medium' if amount < 1000 else \
                     'large' if amount < 10000 else 'enterprise'
    enriched['amount_category'] = amount_category
    
    # Add hash for deduplication (simple implementation)
    hash_input = f"{record.get('merchant_id')}{record.get('customer_id')}{amount}{record.get('timestamp')}"
    enriched['transaction_hash'] = str(hash(hash_input))
    
    return enriched


def process_batch(input_file: str, output_file: str, verbose: bool = False) -> Tuple[int, int, float]:
    """
    Processes a batch of transactions from CSV input to CSV output.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        verbose: Whether to print progress
        
    Returns:
        Tuple of (valid_count, invalid_count, elapsed_seconds)
    """
    valid_count = 0
    invalid_count = 0
    
    start_time = datetime.now()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            
            reader = csv.DictReader(infile)
            
            # Prepare output fieldnames (input fields + enriched fields)
            output_fields = list(reader.fieldnames) + [
                'processed_at', 'processor_version', 'currency_symbol',
                'amount_formatted', 'region', 'tax_rate', 'tax_amount',
                'total_amount', 'risk_level', 'risk_score', 'amount_category',
                'transaction_hash'
            ]
            
            writer = csv.DictWriter(outfile, fieldnames=output_fields)
            writer.writeheader()
            
            for idx, record in enumerate(reader, 1):
                if validate_transaction(record):
                    enriched = enrich_transaction(record)
                    writer.writerow(enriched)
                    valid_count += 1
                else:
                    invalid_count += 1
                
                if verbose and idx % 10000 == 0:
                    print(f"Processed {idx:,} records...")
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing batch: {e}")
        sys.exit(1)
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    return valid_count, invalid_count, elapsed


def main():
    """Main entry point for the transaction processor."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process transaction ETL pipeline')
    parser.add_argument('--input', default='data/transactions_input.csv',
                       help='Input CSV file path')
    parser.add_argument('--output', default='data/transactions_output.csv',
                       help='Output CSV file path')
    parser.add_argument('--verbose', action='store_true',
                       help='Print progress messages')
    
    args = parser.parse_args()
    
    # Check if JIT is enabled
    jit_status = "DISABLED"
    if hasattr(sys, '_jit') and hasattr(sys._jit, 'is_enabled'):
        if sys._jit.is_enabled():
            jit_status = "ENABLED"
    
    print(f"Python {sys.version}")
    print(f"JIT Status: {jit_status}")
    print(f"Processing: {args.input} -> {args.output}")
    print("-" * 60)
    
    valid, invalid, elapsed = process_batch(args.input, args.output, args.verbose)
    
    total = valid + invalid
    throughput = total / elapsed if elapsed > 0 else 0
    
    print("-" * 60)
    print(f"Processed {total:,} records in {elapsed:.2f}s")
    print(f"Valid: {valid:,} | Invalid: {invalid:,}")
    print(f"Throughput: {throughput:,.0f} records/second")
    print(f"JIT Status: {jit_status}")


if __name__ == '__main__':
    main()
