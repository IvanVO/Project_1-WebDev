from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # This lets us retireve the username without retireving any other form data
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')

            return redirect('login')

    context = {'form': form}

    return render(request, "accounts/register.html", context)

def loginPage(request):
    context = {}

    return render(request, "accounts/login.html", context)

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    # An alternative for the dictionary that is rendered in the render() we can build one inside the function and pass it to the render()
    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending}

    return render(request, "accounts/dashboard.html", context)

def products(request):
    products = Product.objects.all() # Query to the Product Model.

    return render(request, "accounts/products.html", {
    'products': products # the dictionary key is the one that can be called in the html file.
    })

"""
@param pk : this parameter is directly associated with the url path, so whatever we name we choose to pass in the str name in 'customer/<str:pk>' has to be the same name in the function parameter.
"""
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all() # 'order_set' is the way to access the objects of the Referenced Model, in this case the varaible 'customer' in the 'models.py' file is a ForeignKey, meaning that this allow us to access the Models data.
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'myFilter': myFilter}

    return render(request, "accounts/customer.html", context)

def create_order(request, pk):
    OrderFormSet =  inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}

    return render(request, "accounts/order_form.html", context)

"""
This method updates a order by getting the information of the order by its PrimaryKey and creating an instance of that information insde the OrderForm()
"""
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        #print(f"printing POST:{request.POST}")
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, "accounts/order_form.html", context)

def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}

    return render(request, "accounts/delete.html", context)
