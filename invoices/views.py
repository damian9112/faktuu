from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Invoice, InvoiceCounter, Client, Product, InvoiceProduct
from .forms import ProductForm, ClientForm, InvoiceForm, InvoiceProductFormSet
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
# Invoices
@login_required()
def invoices(request):
    all_invoices = Invoice.objects.all()
    context = {
        "all_invoices": all_invoices,
    }
    return render(request, "invoices/invoices.html", context)
    
# Create invoice
@login_required()
def invoiceForm(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceProductFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            products = formset.save(commit=False)
            for product in products:
                product.invoice = invoice
                product.save()
            return HttpResponseRedirect(reverse("invoices:invoices"))
    else:
        form = InvoiceForm()
        formset = InvoiceProductFormSet()

    return render(request, "invoices/invoiceForm.html", {"form": form, "formset":formset})
    # return render(request, "invoices/forms.html", context)

# Save invoice
# def save(request):
#     if request.method == 'POST':

#         # compare last invoice number with current date and create new invoice number
#         current_year = datetime.now().year
#         current_month = f"{datetime.now().month:02}"
#         old_invoice_number = InvoiceCounter.objects.filter(client = "Damian").first().highest_number
#         invoice_prefix, invoice_year, invoice_month, document_number = old_invoice_number.split("/")
#         if(int(invoice_year) == int(current_year) and current_month == invoice_month):
#             new_document_number = int(document_number) + 1
#             new_invoice_number = f"FV/{current_year}/{current_month}/{new_document_number}"
#         else:
#             new_invoice_number = f"FV/{current_year}/{current_month}/1"
        
#         # save new invoice number in database
#         InvoiceCounter.objects.filter(client = "Damian").update(highest_number=new_invoice_number)
#         client = request.POST.get('client')
#         product = request.POST.get('product')
        
#         Invoice.objects.create(
#             invoice_number = new_invoice_number,
#             client = Client.objects.get(id=client),
#             product = product
#         )
#     return HttpResponseRedirect(reverse("invoices:index"))

# Detail
@login_required()
def invoiceDetail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    products = invoice.products.all()
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceProductFormSet(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            products = formset.save(commit=False)
            for product in products:
                product.invoice = invoice
                product.save()
            return HttpResponseRedirect(reverse("invoices:invoices"))
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceProductFormSet(instance=invoice)

    return render(request, "invoices/invoiceDetail.html", {"form": form, "formset":formset, "invoice":invoice})
    products = invoice.products.all()
    return render(request, "invoices/invoiceDetail.html", {"invoice": invoice, "products": products})

# Delete Invoice
@login_required()
def invoiceDelete(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == "POST":
        invoice.delete()
        return HttpResponseRedirect(reverse("invoices:invoices"))
    return render(request, "invoices/invoiceDetail.html", {"invoice": invoice})

# PDF
# def pdf(request, invoice_id):
#     return HttpResponse("Invoice download page.")

# clients
@login_required()
def clients(request):
    all_clients = Client.objects.all()
    context = {
        "all_clients": all_clients,
    }
    return render(request, "invoices/clients.html", context)

# Create New Client
@login_required()
def clientform(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("invoices:clients"))
    else:
        form = ClientForm()

    return render(request, "invoices/clientform.html", {"form": form})
    # return render(request, "invoices/clientform.html")

# Save New Client
# def saveclient(request):
#     if request.method == 'POST':

#         clientName = request.POST.get('clientName')
#         nipNumber = request.POST.get('nipNumber')
#         adress = request.POST.get('adress')
#         city = request.POST.get('city')
#         postalCode = request.POST.get('postalCode')
#         country = request.POST.get('country')
#         phoneNumber = request.POST.get('phoneNumber')
#         email = request.POST.get('email')
        
#         Client.objects.create(
#             name = clientName,
#             nip_number = nipNumber,
#             street = adress,
#             city = city,
#             postal_code = postalCode,
#             country = country,
#             phone_number = phoneNumber,
#             email = email
#         )
#     return HttpResponseRedirect(reverse("invoices:clients"))

# Client Detail
@login_required()
def clientDetail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)  
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("invoices:clients"))
    else:
        form = ClientForm(instance=client)
    return render(request, "invoices/clientDetail.html", {"form":form, "client": client})

# Delete Client
@login_required()
def clientDelete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        client.delete()
        return HttpResponseRedirect(reverse("invoices:clients"))
    return render(request, "invoices/clientDetail.html", {"client": client})

# Products
@login_required()
def products(request):
    all_products = Product.objects.all()
    context = {
        "all_products": all_products,
    }
    return render(request, "invoices/products.html", context)

# Create New Product
@login_required()
def productForm(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("invoices:products"))
    else:
        form = ProductForm()

    return render(request, "invoices/productForm.html", {"form": form})
    # return render(request, "invoices/productForm.html")

# Save New Product
# def productSave(request):
#     if request.method == 'POST':

#         productName = request.POST.get('productName')
#         vatRate = request.POST.get('vatRate')
#         priceNetto = request.POST.get('priceNetto')
#         priceBrutto = request.POST.get('priceBrutto')
        
#         Product.objects.create(
#             name = productName,
#             vat_rate = vatRate,
#             price_netto = priceNetto,
#             price_brutto = priceBrutto
#         )
#     return HttpResponseRedirect(reverse("invoices:products"))

# Product Detail
@login_required()
def productDetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)  
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("invoices:products"))
    else:
        form = ProductForm(instance=product)
    return render(request, "invoices/productDetail.html", {"form": form, "product":product})

# Delete Product
@login_required()
def productDelete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        product.delete()
        return HttpResponseRedirect(reverse("invoices:products"))
    return render(request, "invoices/productDetail.html", {"product": product})