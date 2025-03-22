from rest_framework import generics
from .models import SalesOrder, Invoice
from .serializers import SalesOrderSerializer, InvoiceSerializer
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from users.permissions import IsAdmin, IsTrader, IsSalesRep, IsCustomer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string

class InvoiceCreateView(generics.CreateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsTrader | IsSalesRep]

    def perform_create(self, serializer):
        sales_order_id = self.request.data.get("sales_order")
        try:
            sales_order = SalesOrder.objects.get(id=sales_order_id)
            invoice_number = get_random_string(10).upper()
            serializer.save(sales_order=sales_order, invoice_number=invoice_number)
        except SalesOrder.DoesNotExist:
            raise serializers.ValidationError("Sales order not found")

class SalesOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]


class InvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsTrader | IsSalesRep | IsCustomer]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role in ["admin", "trader", "sales_rep"]:
            return Invoice.objects.all()
        
        if user.role == "customer":
            return Invoice.objects.filter(sales_order__customer=user)

        return Invoice.objects.none()

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