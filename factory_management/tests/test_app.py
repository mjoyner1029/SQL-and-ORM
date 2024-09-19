import unittest
from app import create_app, db

class FactoryManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.Config')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_create_employee(self):
        response = self.client.post('/employees', json={'name': 'John Doe', 'position': 'Engineer'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('John Doe', response.get_json()['name'])

    def test_list_employees(self):
        self.client.post('/employees', json={'name': 'John Doe', 'position': 'Engineer'})
        response = self.client.get('/employees')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()['items']), 0)

    def test_list_orders_paginated(self):
        for i in range(20):
            self.client.post('/orders', json={
                'customer_id': 1,
                'product_id': 1,
                'quantity': 1,
                'total_price': 10.0
            })
        response = self.client.get('/orders?page=1&per_page=10')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['items']), 10)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['pages'], 2)

    def test_list_products_paginated(self):
        for i in range(20):
            self.client.post('/products', json={'name': f'Product {i}', 'price': 10.0})
        response = self.client.get('/products?page=1&per_page=10')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['items']), 10)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['pages'], 2)

    def test_employee_performance(self):
        response = self.client.get('/production/employee-performance')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

    def test_top_selling_products(self):
        response = self.client.get('/production/top-selling-products')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

    def test_customer_lifetime_value(self):
        response = self.client.get('/production/customer-lifetime-value')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

    def test_production_efficiency(self):
        response = self.client.get('/production/production-efficiency?date=2024-01-01')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

if __name__ == '__main__':
    unittest.main()
