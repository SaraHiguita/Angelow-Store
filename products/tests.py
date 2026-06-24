import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Category, Product, ProductImage


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Camisas',
            slug='camisas',
            gender='M'
        )
        self.product = Product.objects.create(
            name='Camisa Premium',
            slug='camisa-premium',
            sku='ANG-001',
            category=self.category,
            description='Camisa de alta calidad',
            price=599.99,
            stock_quantity=10,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Camisa Premium')
        self.assertEqual(self.product.sku, 'ANG-001')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Camisa Premium')

    def test_get_final_price_no_discount(self):
        self.assertEqual(self.product.get_final_price(), 599.99)

    def test_get_final_price_with_discount(self):
        self.product.discount_price = 499.99
        self.product.save()
        self.assertEqual(self.product.get_final_price(), 499.99)

    def test_is_on_sale(self):
        self.assertFalse(self.product.is_on_sale())
        self.product.discount_price = 499.99
        self.product.save()
        self.assertTrue(self.product.is_on_sale())

    def test_negative_stock_raises_error(self):
        with self.assertRaises(Exception):
            Product.objects.create(
                name='Test',
                slug='test',
                sku='ANG-999',
                category=self.category,
                description='Test',
                price=100,
                stock_quantity=-5,
            )


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Camisas',
            slug='camisas',
            gender='M'
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Camisas')

    def test_gender_choices(self):
        self.assertEqual(self.category.gender, 'M')


class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin', password='admin12345', email='admin@test.com'
        )
        self.group, _ = Group.objects.get_or_create(name='Admin')
        self.admin_user.groups.add(self.group)

    def test_public_shop_home(self):
        response = self.client.get(reverse('shop_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/home.html')

    def test_public_product_list(self):
        response = self.client.get(reverse('shop_product_list'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200)

    def test_admin_dashboard_authenticated(self):
        self.client.login(username='admin', password='admin12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class CustomerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='cliente', password='cliente123', email='cliente@test.com'
        )
        self.group, _ = Group.objects.get_or_create(name='Cliente')
        self.user.groups.add(self.group)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        data = {
            'username': 'nuevo_user',
            'email': 'nuevo@test.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Juan',
            'last_name': 'Pérez',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='nuevo_user').exists())

    def test_cart_requires_login(self):
        response = self.client.get(reverse('cart'))
        self.assertNotEqual(response.status_code, 200)

    def test_cart_authenticated(self):
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertNotEqual(response.status_code, 200)

    def test_profile_authenticated(self):
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)


class RoleBasedAccessTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_user = User.objects.create_superuser(
            username='admin', password='admin12345', email='admin@test.com'
        )
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.admin_user.groups.add(admin_group)

        self.cliente_user = User.objects.create_user(
            username='cliente', password='cliente123', email='cliente@test.com'
        )
        cliente_group, _ = Group.objects.get_or_create(name='Cliente')
        self.cliente_user.groups.add(cliente_group)

    def test_cliente_cannot_access_admin_panel(self):
        self.client.login(username='cliente', password='cliente123')
        urls = ['dashboard', 'product_list', 'inventory_dashboard']
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            self.assertIn(response.status_code, [302, 403],
                          f'{url_name} should not be accessible by cliente')

    def test_admin_can_access_admin_panel(self):
        self.client.login(username='admin', password='admin12345')
        urls = ['dashboard', 'product_list', 'inventory_dashboard']
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200,
                             f'{url_name} should be accessible by admin')
