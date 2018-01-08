from app.models.category import Category
from app.models.item import Item

category_list = (
    'Kitchen', 'Entertainment', 'Storage'
)

item_list = [
    {
        'name': 'mixer',
        'description': 'Handheld electric mixer',
        'category': 'Kitchen',
    },
    {
        'name': 'skillet',
        'description': 'non-stick teflon skillet',
        'category': 'Kitchen',
    },
    {
        'name': '34inch Television',
        'description': 'Wide screen Television',
        'category': 'Entertainment'
    },
    {
        'name': '60inch Television',
        'description': 'Large Wide screen television',
        'category': 'Entertainment'
    }
]


# Initialze Categories in database
def category_init():
    for c in category_list:
        Category.create(c)


# Add items to categories
def item_init():
    for item in item_list:
        cat_name = item['category']
        c_id = Category.getIdByName(cat_name)
        # assert(c_id)
        Item.create(name=item['name'],
                    description=item['description'],
                    category_id=c_id)
