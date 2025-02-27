from rest_framework import generics
from .models import SalesOrder, Invoice
from .serializers import SalesOrderSerializer, InvoiceSerializer
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from users.permissions import IsAdmin, IsTrader, IsSalesRep, IsCustomer
from rest_framework.permissions import IsAuthenticated



class SalesOrderListCreateView(generics.ListCreateAPIView):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSalesRep]

class SalesOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]


class InvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

def generate_invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, f"Invoice Number: {invoice.invoice_number}")
    p.drawString(100, 730, f"Total Price: {invoice.sales_order.total_price}")
    p.showPage()
    p.save()

    return response