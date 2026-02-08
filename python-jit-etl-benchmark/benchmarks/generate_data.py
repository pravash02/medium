"""
Generate synthetic transaction data for benchmarking.

Creates realistic transaction records with a mix of valid and invalid data
to test validation logic.
"""

import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict

# Configuration
NUM_RECORDS = 100_000
VALID_RATIO = 0.80  # 80% valid, 20% invalid


def generate_valid_transaction() -> Dict:
    """Generate a valid transaction record."""
    currencies = ['USD', 'EUR', 'GBP', 'JPY']
    countries = ['US', 'CA', 'GB', 'DE', 'FR', 'JP', 'CN', 'IN', 'BR', 'AU']
    txn_types = ['purchase', 'refund', 'authorization', 'capture', 'void']
    payment_methods = ['credit_card', 'debit_card', 'bank_transfer', 'digital_wallet']
    statuses = ['pending', 'completed', 'failed', 'cancelled']
    
    # Generate random but valid data
    currency = random.choice(currencies)
    amount = round(random.uniform(10, 5000), 2)
    
    # Random date within last year
    days_ago = random.randint(0, 365)
    timestamp = datetime.now() - timedelta(days=days_ago, 
                                          hours=random.randint(0, 23),
                                          minutes=random.randint(0, 59),
                                          seconds=random.randint(0, 59))
    
    # Generate merchant ID (12 alphanumeric, starts with uppercase)
    merchant_id = chr(random.randint(65, 90)) + ''.join(
        random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=11)
    )
    
    # Generate customer ID (8-20 chars)
    customer_id_length = random.randint(8, 20)
    customer_id = 'CUST' + ''.join(
        random.choices('0123456789ABCDEF', k=customer_id_length - 4)
    )
    
    country = random.choice(countries)
    txn_type = random.choice(txn_types)
    payment_method = random.choice(payment_methods)
    
    record = {
        'transaction_id': f"TXN{random.randint(1000000, 9999999)}",
        'currency': currency,
        'amount': amount,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'merchant_id': merchant_id,
        'customer_id': customer_id,
        'transaction_type': txn_type,
        'country': country,
        'payment_method': payment_method,
        'status': random.choice(statuses),
        'customer_email': f"customer{random.randint(1000, 9999)}@example.com",
        'customer_age_days': random.randint(1, 1000),
    }
    
    # Add original transaction ID for refunds
    if txn_type == 'refund':
        record['original_transaction_id'] = f"TXN{random.randint(1000000, 9999999)}"
    else:
        record['original_transaction_id'] = ''
    
    # Add card last 4 for card payments
    if payment_method in ['credit_card', 'debit_card']:
        record['card_last4'] = f"{random.randint(1000, 9999)}"
    else:
        record['card_last4'] = ''
    
    return record


def generate_invalid_transaction() -> Dict:
    """Generate an invalid transaction record (violates random rules)."""
    record = generate_valid_transaction()
    
    # Randomly break 1-3 validation rules
    num_violations = random.randint(1, 3)
    violations = random.sample(range(1, 11), num_violations)
    
    for violation in violations:
        if violation == 1:
            # Invalid currency
            record['currency'] = random.choice(['XXX', 'ZZZ', '', 'INVALID'])
        elif violation == 2:
            # Invalid amount
            record['amount'] = random.choice([-100, 0, 2000000, 'invalid'])
        elif violation == 3:
            # Invalid timestamp
            record['timestamp'] = random.choice(['invalid-date', '2020-13-45', ''])
        elif violation == 4:
            # Invalid merchant ID (wrong length or format)
            record['merchant_id'] = random.choice(['ABC', 'abcdefghijkl', '12345678901!'])
        elif violation == 5:
            # Invalid customer ID (too short/long)
            record['customer_id'] = random.choice(['C1', 'VERY_LONG_CUSTOMER_ID_THAT_EXCEEDS_LIMIT'])
        elif violation == 6:
            # Invalid transaction type
            record['transaction_type'] = 'invalid_type'
        elif violation == 7:
            # Invalid country code
            record['country'] = random.choice(['USA', 'XX', 'us', ''])
        elif violation == 8:
            # Invalid payment method
            record['payment_method'] = 'invalid_method'
        elif violation == 9:
            # Invalid email
            record['customer_email'] = random.choice(['notemail', 'no@domain', '@.com'])
        elif violation == 10:
            # Missing card last 4 for card payment
            if record['payment_method'] in ['credit_card', 'debit_card']:
                record['card_last4'] = random.choice(['', '12', '12345', 'ABCD'])
    
    return record


def generate_dataset(num_records: int, valid_ratio: float) -> List[Dict]:
    """Generate a dataset with specified valid/invalid ratio."""
    num_valid = int(num_records * valid_ratio)
    num_invalid = num_records - num_valid
    
    print(f"Generating {num_records:,} transaction records...")
    print(f"  Valid: {num_valid:,} ({valid_ratio*100:.0f}%)")
    print(f"  Invalid: {num_invalid:,} ({(1-valid_ratio)*100:.0f}%)")
    
    records = []
    
    # Generate valid records
    for i in range(num_valid):
        records.append(generate_valid_transaction())
        if (i + 1) % 10000 == 0:
            print(f"  Generated {i+1:,} valid records...")
    
    # Generate invalid records
    for i in range(num_invalid):
        records.append(generate_invalid_transaction())
        if (i + 1) % 10000 == 0:
            print(f"  Generated {i+1:,} invalid records...")
    
    # Shuffle to mix valid and invalid
    random.shuffle(records)
    
    return records


def save_to_csv(records: List[Dict], output_file: str):
    """Save records to CSV file."""
    if not records:
        print("No records to save!")
        return
    
    fieldnames = list(records[0].keys())
    
    print(f"Saving to {output_file}...")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"✓ Saved {len(records):,} records to {output_file}")


def main():
    """Generate sample transaction data."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate synthetic transaction data')
    parser.add_argument('--records', type=int, default=NUM_RECORDS,
                       help=f'Number of records to generate (default: {NUM_RECORDS:,})')
    parser.add_argument('--valid-ratio', type=float, default=VALID_RATIO,
                       help=f'Ratio of valid records (default: {VALID_RATIO})')
    parser.add_argument('--output', default='data/transactions_input.csv',
                       help='Output file path')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    random.seed(args.seed)
    
    # Generate dataset
    records = generate_dataset(args.records, args.valid_ratio)
    
    # Save to file
    save_to_csv(records, args.output)
    
    print("\n✓ Data generation complete!")


if __name__ == '__main__':
    main()
