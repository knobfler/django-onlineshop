from decimal import Decimal
from django.conf import settings

from coupons.models import Coupon
from shop.models import Product


# Todo
# 쿠폰 기능 추가


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # Todo
        # 쿠폰을 세션에서 얻어오기
        self.coupon_id = self.session.get('coupon_id')


    def __len__(self):
        '''
        total = 0
        for item in self.cart.values():
            total = total + item['quantity']
        return total
        '''
        return sum(item['quantity'] for item in self.cart.values())


    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # update_quantity = > False: 추가
    # update_quantity = > True: 바꿔치기
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del(self.cart[product_id])
            self.save()


    # session에 바뀐 정보를 저장.
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


    def clear(self):
        self.session['coupon_id'] = None
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        '''
        total = 0
        for item in self.cart.values():
            total = total + (Decimal(item['price']) * item['quantity'])
        return total
        '''
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())



    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount/Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()


