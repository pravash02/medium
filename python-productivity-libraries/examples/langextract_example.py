import re
from collections import Counter, defaultdict
from datetime import datetime


class Extractor:
    def __init__(self, patterns: dict):
        self.patterns = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in patterns.items()
        }

    def extract(self, text: str) -> list:
        results = []
        for entity_type, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                results.append({
                    'type': entity_type,
                    'value': match.group(),
                    'span': match.span(),
                })
        # Sort by position in text
        results.sort(key=lambda x: x['span'][0])
        return results


try:
    from langextract import Extractor as LangExtractor

    Extractor = LangExtractor
    print("Using langextract library")
except ImportError:
    print("langextract not installed — using built-in fallback (same API)")

SUPPORT_TICKET_PATTERNS = {
    'ticket_id': r'TICK-\d{5}',
    'order_id': r'ORD-[A-Z0-9]{8}',
    'date': r'\b\d{4}-\d{2}-\d{2}\b',
    'email': r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b',
    'amount': r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
    'phone': r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b',
    'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
}

LOG_PATTERNS = {
    'timestamp': r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}',
    'log_level': r'\b(ERROR|WARNING|INFO|DEBUG|CRITICAL)\b',
    'error_code': r'\b[A-Z]{2,6}_\d{3,6}\b',
    'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    'duration_ms': r'\b\d+ms\b',
    'http_status': r'\b[45]\d{2}\b',
}


def parse_support_ticket(ticket_text: str) -> dict:
    extractor = Extractor(patterns=SUPPORT_TICKET_PATTERNS)
    raw = extractor.extract(ticket_text)

    entities = defaultdict(list)
    for item in raw:
        entities[item['type']].append(item['value'])

    return {k: list(dict.fromkeys(v)) for k, v in entities.items()}


def analyze_logs(log_content: str) -> dict:
    extractor = Extractor(patterns=LOG_PATTERNS)
    results = extractor.extract(log_content)

    levels = [r['value'] for r in results if r['type'] == 'log_level']
    codes = [r['value'] for r in results if r['type'] == 'error_code']
    statuses = [r['value'] for r in results if r['type'] == 'http_status']
    durations = []

    for r in results:
        if r['type'] == 'duration_ms':
            try:
                durations.append(int(r['value'].replace('ms', '')))
            except ValueError:
                pass

    level_counts = Counter(levels)

    return {
        'total_log_lines': log_content.count('\n') + 1,
        'level_counts': dict(level_counts),
        'error_rate': f"{(level_counts.get('ERROR', 0) / max(len(levels), 1)) * 100:.1f}%",
        'top_error_codes': Counter(codes).most_common(3),
        'http_errors': Counter(statuses).most_common(3),
        'avg_duration_ms': round(sum(durations) / len(durations), 1) if durations else None,
        'max_duration_ms': max(durations) if durations else None,
    }


INVOICE_PATTERNS = {
    'invoice_number': r'INV-\d{6}',
    'date': r'\b\d{4}-\d{2}-\d{2}\b',
    'amount': r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
    'po_number': r'PO-\d{5}',
    'vat_number': r'VAT[:\s]*[A-Z]{2}\d{9,12}',
}


def parse_invoice(invoice_text: str) -> dict:
    extractor = Extractor(patterns=INVOICE_PATTERNS)
    results = extractor.extract(invoice_text)

    entities = defaultdict(list)
    for item in results:
        entities[item['type']].append(item['value'])

    amounts = entities.get('amount', [])

    def parse_amount(s):
        return float(s.replace('$', '').replace(',', ''))

    total = max(amounts, key=parse_amount) if amounts else None

    return {
        'invoice_number': entities.get('invoice_number', [None])[0],
        'invoice_date': entities.get('date', [None])[0],
        'total_amount': total,
        'all_amounts': amounts,
        'po_number': entities.get('po_number', [None])[0],
        'vat_number': entities.get('vat_number', [None])[0],
    }


def main():
    print("=" * 60)
    print("Langextract: Structured Data from Unstructured Text")
    print("=" * 60)

    print("\n--- Demo 1: Support Ticket Parser ---")
    ticket = """
    Customer Jane Doe (jane.doe@example.com) called on 2026-02-08
    regarding order ORD-A1B2C3D4. She was charged $1,245.99 but
    expected $1,145.99. Ticket TICK-12345 opened.
    Follow-up scheduled: 2026-02-10. Contact: 555-123-4567
    Server IP at time of issue: 10.0.0.42
    """
    entities = parse_support_ticket(ticket)
    print(f"\nExtracted entities:")
    for etype, values in entities.items():
        print(f"  {etype:<20}: {values}")

    print("\n--- Demo 2: Log File Analysis ---")
    logs = """
    2026-02-09 10:30:01 INFO  Request from 192.168.1.1 completed in 145ms
    2026-02-09 10:30:02 ERROR DB_ERR_503 Connection refused from 10.0.0.5
    2026-02-09 10:30:03 WARNING High latency detected: 890ms
    2026-02-09 10:30:04 ERROR AUTH_ERR_401 Invalid token - status 401
    2026-02-09 10:30:05 INFO  Processed 50 records in 320ms
    2026-02-09 10:30:06 CRITICAL DB_ERR_503 Database unreachable from 10.0.0.5
    2026-02-09 10:30:07 ERROR  HTTP 500 returned to 192.168.1.10 after 1200ms
    2026-02-09 10:30:08 INFO  Health check OK in 12ms
    """
    analysis = analyze_logs(logs)
    print(f"\nLog Analysis:")
    for key, value in analysis.items():
        print(f"  {key:<25}: {value}")

    print("\n--- Demo 3: Invoice Parser ---")
    invoice = """
    INVOICE
    Invoice Number : INV-204851
    Invoice Date   : 2026-02-01
    PO Reference   : PO-98231
    VAT Number     : VATGB123456789

    Line Items:
      Software Licence  x 5  $250.00
      Support Package   x 1  $500.00
      Setup Fee              $125.99

    Subtotal : $875.99
    VAT (20%): $175.20
    TOTAL    : $1,051.19
    """
    parsed = parse_invoice(invoice)
    print(f"\nParsed Invoice:")
    for key, value in parsed.items():
        print(f"  {key:<20}: {value}")

    print("\n💡 TIP:")
    print("  Langextract is fastest for known patterns (dates, IDs, amounts).")
    print("  For variable / contextual extraction, consider spaCy or Hugging Face.")


if __name__ == '__main__':
    main()
