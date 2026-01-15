"""
Wildberries Product Data Enricher

This module fetches full product details from Wildberries public API
to enrich basic product data with attributes, specifications, and other details.
"""

import requests
import json
import sys
from typing import Dict, Optional, List


class WBEnricher:
    """Enriches WB product data by fetching from public API."""
    
    @staticmethod
    def fetch_wb_product_details(nm_id: int) -> Optional[Dict]:
        """
        Fetch full product details from WB using browser automation.
        
        Args:
            nm_id: Wildberries nomenclature ID (article number)
            
        Returns:
            Dictionary with product details or None if failed
        """
        from playwright.sync_api import sync_playwright
        import time
        
        url = f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx"
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    ]
                )
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page = context.new_page()
                
                print(f"🌐 Navigating to {url}...", file=sys.stderr)
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(2)  # Wait for dynamic content
                
                # Extract data from page
                data = {}
                
                # Get product name
                try:
                    data['imt_name'] = page.locator('h1.product-page__title').inner_text().strip()
                except:
                    print("⚠️  Could not extract product name", file=sys.stderr)
                    data['imt_name'] = ""
                
                # Get description
                try:
                    desc_elem = page.locator('.product-page__description-text')
                    if desc_elem.count() > 0:
                        data['description'] = desc_elem.inner_text().strip()
                except:
                    data['description'] = ""
                
                # Get attributes from specifications table
                options = []
                try:
                    # Try to find specifications table
                    spec_rows = page.locator('.product-params__table tr').all()
                    for row in spec_rows:
                        try:
                            name_elem = row.locator('th').first
                            value_elem = row.locator('td').first
                            
                            if name_elem.count() > 0 and value_elem.count() > 0:
                                name = name_elem.inner_text().strip()
                                value = value_elem.inner_text().strip()
                                
                                if name and value:
                                    options.append({
                                        'name': name,
                                        'value': value
                                    })
                        except:
                            continue
                except Exception as e:
                    print(f"⚠️  Could not extract specifications: {e}", file=sys.stderr)
                
                data['options'] = options
                data['nm_id'] = nm_id
                
                browser.close()
                
                print(f"✅ Extracted {len(options)} attributes from page", file=sys.stderr)
                return data
                
        except Exception as e:
            print(f"❌ Error fetching WB product details: {e}", file=sys.stderr)
            return None
    
    @staticmethod
    def extract_attributes(wb_data: Dict) -> Dict[str, str]:
        """
        Extract and structure attributes from WB product data.
        
        Args:
            wb_data: Raw WB product data from basket API
            
        Returns:
            Dictionary of attribute name -> value
        """
        attributes = {}
        
        # Extract from options (main attributes)
        if 'options' in wb_data:
            for option in wb_data['options']:
                name = option.get('name', '')
                value = option.get('value', '')
                if name and value:
                    attributes[name] = value
        
        # Extract description
        if 'description' in wb_data:
            attributes['Описание'] = wb_data['description']
        
        return attributes
    
    @staticmethod
    def enrich_product_data(basic_product: Dict) -> Dict:
        """
        Enrich basic product data with full WB details.
        
        Args:
            basic_product: Basic product data from database
            
        Returns:
            Enriched product data with full attributes
        """
        nm_id = basic_product.get('id')
        if not nm_id:
            print("❌ No product ID provided", file=sys.stderr)
            return basic_product
        
        print(f"🔍 Fetching details for WB product {nm_id}...", file=sys.stderr)
        wb_data = WBEnricher.fetch_wb_product_details(nm_id)
        
        if not wb_data:
            print(f"⚠️  Could not fetch WB details, using basic data", file=sys.stderr)
            return basic_product
        
        # Extract attributes
        attributes = WBEnricher.extract_attributes(wb_data)
        
        # Merge with basic product data
        enriched = basic_product.copy()
        enriched['attributes'] = attributes
        enriched['wb_full_data'] = wb_data  # Keep full data for reference
        
        # Add additional fields if available
        if 'vendor_code' in wb_data:
            enriched['vendor_code'] = wb_data['vendor_code']
        
        # Extract category info
        if 'subj_name' in wb_data:
            enriched['subject_name'] = wb_data['subj_name']
        if 'subj_root_name' in wb_data:
            enriched['subject_root_name'] = wb_data['subj_root_name']
        
        print(f"✅ Enriched product with {len(attributes)} attributes", file=sys.stderr)
        return enriched


def main():
    """CLI interface for testing."""
    if len(sys.argv) < 2:
        print("Usage: python wb_enricher.py <nm_id>")
        sys.exit(1)
    
    nm_id = int(sys.argv[1])
    
    # Fetch details
    details = WBEnricher.fetch_wb_product_details(nm_id)
    if details:
        print(json.dumps(details, indent=2, ensure_ascii=False))
    else:
        print("Failed to fetch product details")
        sys.exit(1)


if __name__ == "__main__":
    main()
