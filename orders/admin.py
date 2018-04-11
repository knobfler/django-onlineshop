from django.contrib import admin

# Register your models here.
from orders.models import Order, OrderTransaction
from .models import OrderItem
import csv
import datetime
from django.http import HttpResponse

from django.utils.safestring import mark_safe
from django.urls import reverse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def order_detail(obj):
    return mark_safe('<a href="{}">Detail</a>'.format(reverse('orders:admin_order_detail', args=[obj.id])))

order_detail.short_description = 'Detail'

def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf', args=[obj.id])))
order_pdf.short_description = 'PDF'


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'

class OrderTransactionInline(admin.TabularInline):
    model = OrderTransaction


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','address','postal_code','city','paid','created','updated',
                    order_detail, order_pdf]
    list_filter = ['paid','created','updated']
    inlines = [OrderItemInline, OrderTransactionInline]
    actions = [export_to_csv]
admin.site.register(Order, OrderAdmin)