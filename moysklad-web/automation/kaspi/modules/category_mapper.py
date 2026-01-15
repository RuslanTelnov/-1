"""
Kaspi Category Mapper

Maps product names and types to Kaspi categories and generates
appropriate attributes for each category.
"""

import re
from typing import Dict, List, Optional, Tuple


class KaspiCategoryMapper:
    """Maps products to Kaspi categories and generates required attributes."""
    
    # Category mappings based on keywords
    CATEGORY_MAP = {
        # Mugs and cups
        # Mugs and cups
        'кружка': ('Master - Cups and saucers sets', 'mugs'),
        'кружки': ('Master - Cups and saucers sets', 'mugs'),
        'чашка': ('Master - Cups and saucers sets', 'mugs'),
        'чашки': ('Master - Cups and saucers sets', 'mugs'),
        'стакан': ('Master - Cups and saucers sets', 'mugs'),
        'набор чашек': ('Master - Cups and saucers sets', 'mugs'),
        
        # Toys
        'игрушка': ('Master - Stuffed toys', 'toys'),
        'плюшевая': ('Master - Stuffed toys', 'toys'),
        'мягкая игрушка': ('Master - Stuffed toys', 'toys'),
        
        # Backpacks
        'рюкзак': ('Master - Backpacks', 'backpacks'),
        
        # Power banks
        'повербанк': ('Master - Power banks', 'powerbanks'),
        'power bank': ('Master - Power banks', 'powerbanks'),
        'внешний аккумулятор': ('Master - Power banks', 'powerbanks'),
        
        # Socks
        'носки': ('Master - Men socks', 'socks'),
        
        # Keychains
        'брелок': ('Master - Key wallets', 'keychains'),

        # Ab rollers
        'ролик для пресса': ('Master - Ab rollers', 'ab_rollers'),
    }
    
    @staticmethod
    def detect_category(product_name: str, product_description: str = "") -> Tuple[str, str]:
        """
        Detect Kaspi category from product name and description.
        """
        text = (product_name + " " + product_description).lower()
        
        # Check each keyword
        for keyword, (category_id, category_type) in KaspiCategoryMapper.CATEGORY_MAP.items():
            if keyword in text:
                return category_id, category_type
        
        # Return None if no match found
        return None, None
    
    @staticmethod
    def get_required_attributes(category_type: str) -> List[str]:
        """
        Get list of required attributes for a category.
        """
        attribute_map = {
            'mugs': [
                'Cups and saucers sets*Type',
                'Cups and saucers sets*Volume',
                'Cups and saucers sets*Number of pieces',
                'Cups and saucers sets*Brand code',
                'Kitchenware*Color',
                'Kitchenware*Material',
            ],
            'toys': [
                'Stuffed toys*Type',
                'Stuffed toys*Height',
                'Stuffed toys*Filler',
                'Stuffed toys*Character',
                'Stuffed toys*View',
                'Toys*Age',
                'Toys*Gender',
                'Toys*Color',
                'Toys*Material',
            ],
            'backpacks': [
                'Backpacks*Material',
                'Backpacks*Clasp',
                'Backpacks*Style',
                'Backpacks*Depth',
                'Backpacks*Width',
                'Backpacks*Height',
                'Backpacks*Model',
                'Backpacks*Type',
                'Backpacks*Country',
                'Fashion accessories*Color',
                'Fashion accessories*For whom',
            ],
            'socks': [
                'Men socks*Type',
                'Men socks*Set',
                'Men socks*Manufacturer size',
                'Men socks*Fabric',
                'Men socks*Equipment',
                'Men socks*Notice1',
                'Clothes*Size',
                'Clothes*Colour',
                'Clothes*Manufacturer code',
            ],
            'powerbanks': [
                'Power banks*Capacity',
                'Power banks*Maximum output power',
                'Power banks*Outputs',
                'Power banks*Fast charge',
                'Power banks*Support wireless charging',
                'Power banks*Model',
                'Power banks*Color',
            ],
            'ab_rollers': [
                'Ab rollers*Wheels number',
                'Ab rollers*Max load',
                'Ab rollers*Wheels material',
                'Ab rollers*Material',
                'Ab rollers*Color',
                'Ab rollers*Vendor code',
            ]
        }
        
        return attribute_map.get(category_type, [])
    
    @staticmethod
    def generate_attributes_for_mugs(product_name: str, product_description: str = "") -> Dict[str, str]:
        """
        Generate Kaspi attributes for mugs category.
        """
        attributes = {
            "Cups and saucers sets*Type": "кружка",
            "Cups and saucers sets*Number of pieces": 1,
            "Cups and saucers sets*Brand code": "нет", # Mandatory brand code, use "нет" if unknown
        }
        
        text = (product_name + " " + product_description).lower()

        # Generate 'Cups and saucers sets*Type' attribute
        if any(word in text for word in ['набор', 'комплект']):
            attributes["Cups and saucers sets*Type"] = "набор чашек"
            attributes["Cups and saucers sets*Number of pieces"] = 2 # Default to 2 for sets if not found
        
        text = (product_name + " " + product_description).lower()
        
        # Extract material
        if any(word in text for word in ['стекл', 'glass']):
            attributes["Kitchenware*Material"] = ["стекло"]
        elif any(word in text for word in ['керам', 'ceramic']):
            attributes["Kitchenware*Material"] = ["керамика"]
        elif any(word in text for word in ['фарф', 'porcelain']):
            attributes["Kitchenware*Material"] = ["фарфор"]
        else:
            attributes["Kitchenware*Material"] = ["керамика"]
        
        # Extract volume
        volume_match = re.search(r'(\d+)\s*(мл|ml)', text)
        if volume_match:
            attributes["Cups and saucers sets*Volume"] = int(volume_match.group(1))
        else:
            attributes["Cups and saucers sets*Volume"] = 350
        
        # Extract color
        colors = {
            'белый': 'белый', 'белая': 'белый',
            'черный': 'черный', 'черная': 'черный',
            'красный': 'красный', 'красная': 'красный',
            'синий': 'синий', 'синяя': 'синий',
        }
        
        found_color = "белый"
        for color_word, color_value in colors.items():
            if color_word in text:
                found_color = color_value
                break
        attributes["Kitchenware*Color"] = [found_color]
        
        return attributes
    
    @staticmethod
    def generate_attributes_for_socks(product_name: str, product_description: str = "") -> Dict[str, str]:
        """
        Generate Kaspi attributes for socks category.
        """
        attributes = {
            "Men socks*Type": ["носки"],
            "Men socks*Set": True,
            "Men socks*Manufacturer size": "36-41",
            "Men socks*Fabric": ["хлопок"],
            "Men socks*Equipment": "1 пара",
            "Men socks*Notice1": "не маломерят",
            "Clothes*Size": ["36-41"],
            "Clothes*Colour": ["черный"],
            "Clothes*Manufacturer code": "SOCKS-BK-01"
        }
        return attributes

    @staticmethod
    def generate_attributes_for_powerbanks(product_name: str, product_description: str = "") -> Dict[str, str]:
        """
        Generate Kaspi attributes for power banks.
        """
        attributes = {
            "Power banks*Capacity": 10000,
            "Power banks*Maximum output power": 20,
            "Power banks*Outputs": ["USB Type-C"],
            "Power banks*Fast charge": True,
            "Power banks*Support wireless charging": False,
            "Power banks*Model": "PowerBank-10",
            "Power banks*Color": ["черный"]
        }
        return attributes

    @staticmethod
    def generate_attributes_for_ab_rollers(product_name: str, product_description: str = "") -> Dict[str, str]:
        """
        Generate Kaspi attributes for ab rollers.
        """
        attributes = {
            "Ab rollers*Wheels number": "1",
            "Ab rollers*Max load": 100,
            "Ab rollers*Wheels material": ["пластик"],
            "Ab rollers*Material": ["металл", "пластик"],
            "Ab rollers*Color": "черный",
            "Ab rollers*Vendor code": "AB-ROLLER-01"
        }
        return attributes

    @staticmethod
    def generate_attributes(product_name: str, product_description: str = "", 
                          category_type: str = None) -> Dict[str, str]:
        """
        Generate Kaspi attributes based on product data and category.
        """
        if category_type is None:
            _, category_type = KaspiCategoryMapper.detect_category(product_name, product_description)
        
        if category_type == 'mugs':
            return KaspiCategoryMapper.generate_attributes_for_mugs(product_name, product_description)
        elif category_type == 'socks':
            return KaspiCategoryMapper.generate_attributes_for_socks(product_name, product_description)
        elif category_type == 'powerbanks':
            return KaspiCategoryMapper.generate_attributes_for_powerbanks(product_name, product_description)
        elif category_type == 'ab_rollers':
            return KaspiCategoryMapper.generate_attributes_for_ab_rollers(product_name, product_description)
        
        return {}
    
    @staticmethod
    def validate_attributes(attributes: Dict[str, str], category_type: str) -> Tuple[bool, List[str]]:
        """
        Validate that all required attributes are present.
        """
        required = KaspiCategoryMapper.get_required_attributes(category_type)
        missing = [attr for attr in required if attr not in attributes]
        
        return len(missing) == 0, missing


if __name__ == "__main__":
    # Test the mapper
    test_cases = [
        "Кружка керамическая 350 мл белая",
        "Стеклянная чашка 250мл",
        "Игрушка плюшевая мишка",
        "Рюкзак школьный",
    ]
    
    for name in test_cases:
        category_id, category_type = KaspiCategoryMapper.detect_category(name)
        attributes = KaspiCategoryMapper.generate_attributes(name)
        print(f"\n{name}")
        print(f"  Category: {category_id} ({category_type})")
        print(f"  Attributes: {attributes}")
