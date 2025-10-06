"""
Product category definitions and keyword mappings.
"""

from enum import Enum
from typing import Dict, List


class ProductCategory(Enum):
    # Product categories
    FRUITS = "Fruits"
    VEGETABLES = "Vegetables"
    HERBS = "Herbs"
    GRAINS = "Grains"
    LEGUMES = "Legumes"
    NUTS = "Nuts"
    SPICES = "Spices"
    DAIRY = "Dairy"
    MEAT = "Meat"
    SEAFOOD = "Seafood"
    BEVERAGES = "Beverages"
    SNACKS = "Snacks"
    BAKERY = "Bakery"
    FROZEN = "Frozen"
    CANNED = "Canned"
    OTHER = "Other"


def get_category_keywords() -> Dict[ProductCategory, List[str]]:
    # Build keyword mappings for each category, returns dict mapping categories to their keyword lists
    return {
        ProductCategory.FRUITS: [
            # English
            'apple', 'banana', 'orange', 'grape', 'strawberry', 'blueberry', 'raspberry',
            'cherry', 'peach', 'pear', 'plum', 'mango', 'pineapple', 'watermelon',
            'lemon', 'lime', 'grapefruit', 'pomegranate', 'kiwi', 'papaya', 'avocado',
            'fig', 'date', 'coconut', 'passion fruit', 'dragon fruit', 'lychee',
            # Arabic transliterations
            'tamarind', 'jujube', 'loquat', 'quince', 'medlar',
            # Varieties
            'gala', 'fuji', 'granny smith', 'honeycrisp', 'red delicious', 'golden delicious',
            'pink lady', 'braeburn', 'jonagold', 'empire', 'cortland', 'macintosh',
            'valencia', 'navel', 'blood orange', 'mandarin', 'clementine', 'tangerine'
        ],
        
        ProductCategory.VEGETABLES: [
            # English
            'tomato', 'potato', 'carrot', 'onion', 'garlic', 'pepper', 'cucumber',
            'lettuce', 'spinach', 'kale', 'cabbage', 'broccoli', 'cauliflower',
            'asparagus', 'celery', 'radish', 'beet', 'turnip', 'leek', 'scallion',
            'ginger', 'turmeric', 'squash', 'pumpkin', 'eggplant', 'corn',
            'green bean', 'snap bean', 'peas', 'artichoke', 'okra', 'jicama',
            'brussels sprouts', 'kohlrabi', 'daikon', 'horseradish', 'wasabi',
            'bamboo shoots', 'water chestnut'
        ],
        
        ProductCategory.HERBS: [
            'basil', 'oregano', 'thyme', 'rosemary', 'sage', 'parsley', 'cilantro',
            'dill', 'mint', 'chives', 'tarragon', 'marjoram', 'bay leaves',
            'curry leaves', 'lemongrass', 'lavender', 'chamomile', 'fennel seeds',
            'caraway', 'anise', 'chervil', 'borage', 'sorrel', 'watercress',
            'arugula', 'mizuna', 'tatsoi', 'mitsuba', 'shiso', 'perilla'
        ],
        
        ProductCategory.GRAINS: [
            'rice', 'wheat', 'barley', 'oats', 'quinoa', 'buckwheat', 'millet',
            'rye', 'corn', 'sorghum', 'amaranth', 'teff', 'bulgur', 'couscous',
            'farro', 'spelt', 'kamut', 'freekeh', 'wild rice', 'brown rice',
            'white rice', 'jasmine rice', 'basmati rice', 'arborio rice'
        ],
        
        ProductCategory.LEGUMES: [
            'beans', 'lentils', 'chickpeas', 'peas', 'soybeans', 'black beans',
            'kidney beans', 'pinto beans', 'navy beans', 'lima beans', 'fava beans',
            'split peas', 'black-eyed peas', 'adzuki beans', 'mung beans',
            'cannellini beans', 'garbanzo beans', 'red lentils', 'green lentils',
            'brown lentils', 'yellow lentils', 'black lentils', 'beluga lentils'
        ],
        
        ProductCategory.NUTS: [
            'almonds', 'walnuts', 'pecans', 'cashews', 'pistachios', 'hazelnuts',
            'macadamia', 'brazil nuts', 'pine nuts', 'pumpkin seeds', 'sunflower seeds',
            'sesame seeds', 'chia seeds', 'flax seeds', 'hemp seeds', 'peanuts',
            'chestnuts', 'acorns', 'pili nuts', 'kukui nuts', 'candlenuts'
        ],
        
        ProductCategory.SPICES: [
            'pepper', 'salt', 'cinnamon', 'nutmeg', 'cloves', 'cardamom',
            'vanilla', 'ginger', 'turmeric', 'cumin', 'coriander', 'paprika',
            'cayenne', 'chili powder', 'garlic powder', 'onion powder',
            'allspice', 'juniper berries', 'saffron', 'sumac', 'zaatar',
            'harissa', 'berbere', 'ras el hanout', 'garam masala', 'curry powder'
        ],
        
        ProductCategory.DAIRY: [
            'milk', 'cheese', 'yogurt', 'butter', 'cream', 'sour cream',
            'buttermilk', 'kefir', 'cottage cheese', 'ricotta', 'mozzarella',
            'cheddar', 'swiss', 'parmesan', 'feta', 'goat cheese', 'cream cheese',
            'mascarpone', 'gouda', 'brie', 'camembert', 'blue cheese'
        ],
        
        ProductCategory.MEAT: [
            'beef', 'pork', 'lamb', 'chicken', 'turkey', 'duck', 'veal',
            'bacon', 'ham', 'sausage', 'chorizo', 'salami', 'pepperoni',
            'prosciutto', 'pancetta', 'guanciale', 'liver', 'kidney', 'heart',
            'tongue', 'oxtail', 'ribs', 'chops', 'steak', 'roast'
        ],
        
        ProductCategory.SEAFOOD: [
            'fish', 'salmon', 'tuna', 'cod', 'halibut', 'bass', 'trout',
            'mackerel', 'sardines', 'anchovies', 'shrimp', 'prawns', 'lobster',
            'crab', 'scallops', 'mussels', 'clams', 'oysters', 'squid',
            'octopus', 'cuttlefish', 'eel', 'caviar', 'roe', 'seaweed', 'nori'
        ],
        
        ProductCategory.BEVERAGES: [
            'juice', 'soda', 'water', 'tea', 'coffee', 'milk', 'smoothie',
            'shake', 'wine', 'beer', 'lemonade', 'iced tea', 'energy drink',
            'sports drink', 'coconut water', 'kombucha'
        ],
        
        ProductCategory.SNACKS: [
            'chips', 'crackers', 'nuts', 'popcorn', 'pretzels', 'trail mix',
            'granola', 'cookies', 'biscuits', 'candy', 'chocolate', 'gummies',
            'jerky', 'dried fruit'
        ],
        
        ProductCategory.BAKERY: [
            'bread', 'rolls', 'bagels', 'croissants', 'muffins', 'scones',
            'cakes', 'pies', 'tarts', 'pastries', 'donuts', 'cookies',
            'biscuits', 'crackers'
        ],
        
        ProductCategory.FROZEN: [
            'frozen vegetables', 'frozen fruits', 'frozen meals', 'ice cream',
            'frozen yogurt', 'frozen pizza', 'frozen burritos', 'frozen waffles',
            'frozen berries'
        ],
        
        ProductCategory.CANNED: [
            'canned vegetables', 'canned fruits', 'canned beans', 'canned tomatoes',
            'canned soup', 'canned fish', 'canned meat', 'preserves', 'jams',
            'jellies'
        ]
    }

