from django.urls import path

from . import views

app_name = "invoices"
urlpatterns = [
    # /invoices
    path("invoices/", views.index, name="index"),
     # /invoice/create
    path("invoices/create", views.forms, name="forms"),
    # /invoice/save
    path("invoices/save", views.save, name="save"),
    # /invoice/5
    path("invoices/<int:invoice_id>/", views.detail, name="detail"),
    # /invoice/5/pdf
    path("invoices/<int:invoice_id>/pdf/", views.pdf, name="products"),

    # /invoice/clients
    path("invoices/clients", views.clients, name="clients"),
     # /invoice/clients/create
    path("invoices/clients/create", views.clientform, name="clientform"),
      # /invoice/clients/save
    path("invoices/clients/save", views.saveclient, name="saveclient"),
    # /invoice/clients/5
    path("invoices/clients/<int:client_id>/", views.clientDetail, name="clientDetail"),

      # /invoice/products
    path("invoices/products", views.products, name="products"),
     # /invoice/products/create
    path("invoices/products/create", views.productForm, name="productForm"),
      # /invoice/products/save
    path("invoices/products/save", views.productSave, name="productSave"),
    # /invoice/products/5
    path("invoices/products/<int:product_id>/", views.productDetail, name="productDetail"),
]