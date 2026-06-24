from decouple import config
import mercadopago


def get_mp_client():
    access_token = config('MERCADO_PAGO_ACCESS_TOKEN', default='')
    return mercadopago.SDK(access_token)


def create_payment_preference(order, request):
    sdk = get_mp_client()
    items = []
    for item in order.items.all():
        items.append({
            'title': item.product.name,
            'quantity': item.quantity,
            'unit_price': float(item.unit_price),
            'currency_id': 'MXN',
        })

    if order.shipping_cost > 0:
        items.append({
            'title': 'Envío',
            'quantity': 1,
            'unit_price': float(order.shipping_cost),
            'currency_id': 'MXN',
        })

    preference_data = {
        'items': items,
        'payer': {
            'name': order.user.first_name or order.user.username,
            'email': order.user.email,
        },
        'back_urls': {
            'success': request.build_absolute_uri(f'/orders/mp-success/{order.pk}/'),
            'failure': request.build_absolute_uri(f'/orders/mp-failure/{order.pk}/'),
            'pending': request.build_absolute_uri(f'/orders/mp-pending/{order.pk}/'),
        },
        'auto_return': 'approved',
        'external_reference': str(order.order_number),
        'notification_url': request.build_absolute_uri('/orders/mp-webhook/'),
        'statement_descriptor': 'ANGELOW STORE',
    }

    preference = sdk.preference().create(preference_data)
    return preference.get('response', {})


def handle_mp_webhook(data):
    sdk = get_mp_client()
    payment_id = data.get('data', {}).get('id')
    if not payment_id:
        return False

    payment_info = sdk.payment().get(payment_id)
    payment_response = payment_info.get('response', {})
    status = payment_response.get('status')
    external_reference = payment_response.get('external_reference')

    if status == 'approved' and external_reference:
        from .models import Order
        try:
            order = Order.objects.get(order_number=external_reference)
            order.payment_status = 'paid'
            order.status = 'confirmed'
            order.transaction_id = str(payment_id)
            order.payment_method = 'Mercado Pago'
            order.save()
            return True
        except Order.DoesNotExist:
            return False
    return False
