from django.test import TestCase
from eCommerceApi.models import ProductCategorie
import pdb

class ProductCategorieTestCase(TestCase):
    def setUp(self):
        ProductCategorie.objects.create(category="pc")

    def test_database_connected(self):
        """Checking Database connectivity"""
        productCategory = ProductCategorie.objects.get(category="pc")
        # pdb.set_trace()
        self.assertEqual(productCategory.category, 'pc')