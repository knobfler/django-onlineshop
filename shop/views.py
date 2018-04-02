from django.shortcuts import render, get_object_or_404
from .models import *
from cart.forms import CartAddProductForm


# Create your views here.

def product_list(request, category_slug=None):
    category = None
    # objects? Model의 매니저. 기본 매니저-> objects
    categories = Category.objects.all()

    # available = True 인 것만 갖고옴.
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories,
                                                      'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_form': cart_form})