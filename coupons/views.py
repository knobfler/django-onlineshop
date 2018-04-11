from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from django.views.decorators.http import require_POST

from coupons.forms import CouponApplyForm
from coupons.models import Coupon


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            # code__iexact -> 무조건 일치하는것만 갖고온다.
            # valid_from__lte -> ~보다 작거나 같아야한다.
            # valid_from__gte -> ~보다 크거나 같아야 한다.
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')