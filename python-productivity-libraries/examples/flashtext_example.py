from flashtext import KeywordProcessor
import time


PRODUCT_VARIATIONS = {
    "iphone 14 pro max": "Apple iPhone 14 Pro Max",
    "iPhone 14 pro max": "Apple iPhone 14 Pro Max",
    "IPHONE 14 PRO MAX": "Apple iPhone 14 Pro Max",
    "i phone 14 pro max": "Apple iPhone 14 Pro Max",

    "samsung galaxy s23": "Samsung Galaxy S23 Ultra",
    "Samsung Galaxy S23": "Samsung Galaxy S23 Ultra",
    "galaxy s23": "Samsung Galaxy S23 Ultra",

    "macbook pro m2": "Apple MacBook Pro M2",
    "MacBook Pro M2": "Apple MacBook Pro M2",
    "mac book pro m2": "Apple MacBook Pro M2",
}


def create_product_processor():
    processor = KeywordProcessor(case_sensitive=False)
    
    # Add all product variations
    for variation, standard_name in PRODUCT_VARIATIONS.items():
        processor.add_keyword(variation, standard_name)
    
    return processor


def standardize_product_descriptions(descriptions, processor):
    standardized = []
    
    for desc in descriptions:
        standardized_desc = processor.replace_keywords(desc)
        standardized.append(standardized_desc)
    
    return standardized


def main():
    print("="*60)
    print("FlashText: Production Product Standardization")
    print("="*60)

    raw_descriptions = [
        "Brand new iphone 14 pro max 256GB in Space Gray",
        "Selling my iPhone 14 pro max, barely used, $900",
        "IPHONE 14 PRO MAX - Factory Unlocked - Best Price!",
        "samsung galaxy s23 with 512GB storage",
        "Galaxy S23 Ultra - Phantom Black",
        "MacBook Pro M2 - 16GB RAM - Perfect condition",
        "mac book pro m2 for sale - excellent deal",
    ]
    
    print(f"\nProcessing {len(raw_descriptions)} product descriptions...")

    processor = create_product_processor()

    start = time.time()
    standardized = standardize_product_descriptions(raw_descriptions, processor)
    elapsed = time.time() - start

    print("\nResults:")
    print("-"*60)
    for original, standardized in zip(raw_descriptions, standardized):
        if original != standardized:
            print(f"BEFORE: {original}")
            print(f"AFTER:  {standardized}")
            print()
    
    print(f"Processed {len(raw_descriptions)} descriptions in {elapsed*1000:.2f}ms")
    print(f"Average: {(elapsed*1000)/len(raw_descriptions):.2f}ms per description")
    
    # Scale test
    print("\n" + "="*60)
    print("SCALE TEST: 10,000 descriptions")
    print("="*60)
    
    large_dataset = raw_descriptions * 1429  # ~10k descriptions
    
    start = time.time()
    standardized_large = standardize_product_descriptions(large_dataset, processor)
    elapsed = time.time() - start
    
    print(f"Processed {len(large_dataset):,} descriptions in {elapsed:.2f}s")
    print(f"Throughput: {len(large_dataset)/elapsed:,.0f} descriptions/second")


if __name__ == '__main__':
    main()
