from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', [])

    for item in cart:
        if item['product_id'] == product.id:
            item['quantity'] += 1
            item['total_price'] = item['quantity'] * float(product.price)
            break
    else:
        cart.append({
            'product_id': product.id,
            'product_name': product.name,
            'quantity': 1,
            'price': float(product.price),
            'total_price': float(product.price),
        })

    request.session['cart'] = cart
    return redirect('product_list')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['product_id'] != item_id]
    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):
    if request.method == 'POST':
        # Lógica para procesar nuestra  compra
        return redirect('product_list')
    return render(request, 'store/checkout.html')

def admin_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/admin_add_product.html', {'form': form})

def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    return render(request, 'store/product_list.html', {'products': products})

def cart(request):
    cart = request.session.get('cart', [])
    context = {'cart_items': cart}
    return render(request, 'store/cart.html', context)
