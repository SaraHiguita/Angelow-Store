import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem, Cart, CartItem, Coupon, Return
from products.models import Category, Product
from inventory.models import StockMovement


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Camisas', slug='camisas', gender='M')
        self.product = Product.objects.create(
            name='Camisa Test', slug='camisa-test', sku='ANG-TST',
            category=self.category, description='Test', price=100,
            stock_quantity=20,
        )
        self.order = Order.objects.create(
            user=self.user, shipping_address='Calle 123',
            subtotal=100, shipping_cost=0, tax=16, total=116,
        )

    def test_order_number_generation(self):
        self.assertTrue(self.order.order_number.startswith('ANG'))

    def test_order_str(self):
        self.assertIn('ANG', str(self.order))

    def test_order_total_calculation(self):
        self.assertEqual(self.order.total, 116)

    def test_order_status_default(self):
        self.assertEqual(self.order.status, 'pending')


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cartuser', password='testpass123')
        self.category = Category.objects.create(name='Camisas', slug='camisas', gender='M')
        self.product = Product.objects.create(
            name='Camisa Cart', slug='camisa-cart', sku='ANG-CART',
            category=self.category, description='Test', price=200,
            stock_quantity=10,
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2, size='M', color='Negro',
        )

    def test_cart_get_total(self):
        self.assertEqual(self.cart.get_total(), 400)

    def test_cart_get_item_count(self):
        self.assertEqual(self.cart.get_item_count(), 2)

    def test_cart_item_subtotal(self):
        self.assertEqual(self.cart_item.get_subtotal(), 400)


class CouponModelTest(TestCase):
    def setUp(self):
        self.coupon = Coupon.objects.create(
            code='DESC10',
            discount_type='percentage',
            discount_value=10,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
        )

    def test_coupon_str(self):
        self.assertEqual(str(self.coupon), 'DESC10')

    def test_coupon_is_valid(self):
        self.assertTrue(self.coupon.is_valid())

    def test_expired_coupon(self):
        self.coupon.valid_to = timezone.now() - timedelta(days=1)
        self.coupon.save()
        self.assertFalse(self.coupon.is_valid())

    def test_inactive_coupon(self):
        self.coupon.is_active = False
        self.coupon.save()
        self.assertFalse(self.coupon.is_valid())

    def test_max_uses_reached(self):
        self.coupon.max_uses = 5
        self.coupon.used_count = 5
        self.coupon.save()
        self.assertFalse(self.coupon.is_valid())

    def test_percentage_discount(self):
        discount = self.coupon.apply_discount(1000)
        self.assertEqual(discount, 100)

    def test_fixed_discount(self):
        self.coupon.discount_type = 'fixed'
        self.coupon.discount_value = 50
        discount = self.coupon.apply_discount(1000)
        self.assertEqual(discount, 50)

    def test_fixed_discount_capped_at_subtotal(self):
        self.coupon.discount_type = 'fixed'
        self.coupon.discount_value = 500
        discount = self.coupon.apply_discount(100)
        self.assertEqual(discount, 100)


class ReturnModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='returnuser', password='testpass123')
        self.category = Category.objects.create(name='Camisas', slug='camisas', gender='M')
        self.product = Product.objects.create(
            name='Camisa Return', slug='camisa-return', sku='ANG-RET',
            category=self.category, description='Test', price=100,
            stock_quantity=5,
        )
        self.order = Order.objects.create(
            user=self.user, shipping_address='Calle 123',
            subtotal=100, shipping_cost=0, tax=16, total=116, status='delivered',
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1, unit_price=100, total_price=100,
        )

    def test_create_return(self):
        return_obj = Return.objects.create(
            order=self.order, reason='defective', description='Está roto',
        )
        return_obj.items.add(self.order_item)
        self.assertEqual(return_obj.status, 'requested')
        self.assertEqual(str(return_obj), f"Devolución #{return_obj.id} - Pedido {self.order.order_number}")


class StockDecrementTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='buyer', password='testpass123', email='buyer@test.com')
        self.group, _ = Group.objects.get_or_create(name='Cliente')
        self.user.groups.add(self.group)
        self.category = Category.objects.create(name='Camisas', slug='camisas', gender='M')
        self.product = Product.objects.create(
            name='Camisa Stock', slug='camisa-stock', sku='ANG-STK',
            category=self.category, description='Test', price=100,
            stock_quantity=10,
        )
        self.client.login(username='buyer', password='testpass123')
        Cart.objects.get_or_create(user=self.user)

    def test_stock_reduces_on_order(self):
        cart = Cart.objects.get(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=3, size='M', color='Negro')

        response = self.client.post(reverse('checkout'), {
            'shipping_address': 'Calle 123, Ciudad',
            'payment_method': 'cash',
        })
        self.assertEqual(response.status_code, 302)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 7)

    def test_stock_movement_created_on_order(self):
        cart = Cart.objects.get(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2, size='L', color='Blanco')

        response = self.client.post(reverse('checkout'), {
            'shipping_address': 'Calle 123, Ciudad',
            'payment_method': 'cash',
        })
        self.assertEqual(response.status_code, 302)

        movements = StockMovement.objects.filter(product=self.product, movement_type='out')
        self.assertEqual(movements.count(), 1)
        self.assertEqual(movements.first().quantity, 2)


class CancelOrderTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='canceller', password='testpass123')
        self.group, _ = Group.objects.get_or_create(name='Cliente')
        self.user.groups.add(self.group)
        self.category = Category.objects.create(name='Camisas', slug='camisas', gender='M')
        self.product = Product.objects.create(
            name='Camisa Cancel', slug='camisa-cancel', sku='ANG-CAN',
            category=self.category, description='Test', price=100,
            stock_quantity=5,
        )
        self.client.login(username='canceller', password='testpass123')

        self.order = Order.objects.create(
            user=self.user, shipping_address='Calle 123',
            subtotal=100, shipping_cost=0, tax=16, total=116,
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=2, unit_price=100, total_price=200,
        )

    def test_cancel_pending_order(self):
        response = self.client.post(reverse('cancel_order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'cancelled')

    def test_cancel_restores_stock(self):
        self.product.stock_quantity = 3
        self.product.save()
        response = self.client.post(reverse('cancel_order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 5)

    def test_cannot_cancel_non_pending_order(self):
        self.order.status = 'shipped'
        self.order.save()
        response = self.client.post(reverse('cancel_order', kwargs={'pk': self.order.pk}))
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'shipped')


class ReturnWorkflowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='returner', password='testpass123')
        self.group, _ = Group.objects.get_or_create(name='Cliente')
        self.user.groups.add(self.group)
        self.category = Category.objects.create(name='Camisas', slug='camisas', gender='M')
        self.product = Product.objects.create(
            name='Camisa Ret', slug='camisa-ret', sku='ANG-RET2',
            category=self.category, description='Test', price=100,
            stock_quantity=5,
        )
        self.client.login(username='returner', password='testpass123')

        self.order = Order.objects.create(
            user=self.user, shipping_address='Calle 123',
            subtotal=100, shipping_cost=0, tax=16, total=116, status='delivered',
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1, unit_price=100, total_price=100,
        )

    def test_return_form_view(self):
        response = self.client.get(reverse('return_create', kwargs={'order_pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)

    def test_submit_return(self):
        response = self.client.post(reverse('return_create', kwargs={'order_pk': self.order.pk}), {
            'reason': 'defective',
            'description': 'Producto llegó dañado',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Return.objects.filter(order=self.order).exists())


class CouponCheckoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='couponer', password='testpass123')
        self.group, _ = Group.objects.get_or_create(name='Cliente')
        self.user.groups.add(self.group)
        self.category = Category.objects.create(name='Camisas', slug='camisas', gender='M')
        self.product = Product.objects.create(
            name='Camisa Coup', slug='camisa-coup', sku='ANG-CUP',
            category=self.category, description='Test', price=100,
            stock_quantity=10,
        )
        self.client.login(username='couponer', password='testpass123')
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2, size='M', color='Negro')

        self.coupon = Coupon.objects.create(
            code='TEST20',
            discount_type='percentage',
            discount_value=20,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
        )

    def test_coupon_applied_at_checkout(self):
        response = self.client.post(reverse('checkout'), {
            'shipping_address': 'Calle 123, Ciudad',
            'payment_method': 'cash',
            'coupon_code': 'TEST20',
        })
        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertGreater(order.discount, 0)

    def test_coupon_used_count_incremented(self):
        response = self.client.post(reverse('checkout'), {
            'shipping_address': 'Calle 123, Ciudad',
            'payment_method': 'cash',
            'coupon_code': 'TEST20',
        })
        self.assertEqual(response.status_code, 302)
        self.coupon.refresh_from_db()
        self.assertEqual(self.coupon.used_count, 1)


class PasswordResetTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_password_reset_form_view(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_view(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)


class ProductPaginationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Camisas', slug='camisas', gender='M')
        for i in range(25):
            Product.objects.create(
                name=f'Camisa {i}', slug=f'camisa-{i}', sku=f'ANG-PG{i:03d}',
                category=self.category, description='Test', price=100,
                stock_quantity=10,
            )

    def test_pagination_on_product_list(self):
        response = self.client.get(reverse('shop_product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)

    def test_second_page(self):
        response = self.client.get(reverse('shop_product_list'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 12)


class OutOfStockFilterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Camisas', slug='camisas', gender='M')
        Product.objects.create(
            name='Activo', slug='activo', sku='ANG-ACT',
            category=self.category, description='Test', price=100,
            stock_quantity=10, status='active',
        )
        Product.objects.create(
            name='Sin Stock', slug='sin-stock', sku='ANG-OOS',
            category=self.category, description='Test', price=100,
            stock_quantity=0, status='out_of_stock',
        )

    def test_out_of_stock_excluded_from_list(self):
        response = self.client.get(reverse('shop_product_list'))
        product_names = [p.name for p in response.context['products']]
        self.assertIn('Activo', product_names)
        self.assertNotIn('Sin Stock', product_names)

    def test_out_of_stock_excluded_from_home(self):
        response = self.client.get(reverse('shop_home'))
        product_names = [p.name for p in response.context['products']]
        self.assertIn('Activo', product_names)
        self.assertNotIn('Sin Stock', product_names)