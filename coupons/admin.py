from django.conf.urls import url
from django.contrib import admin
from django.db.utils import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import FileImportForm
from .logger import ExcelLogger
from .models import Coupon
from .services import ExcelParserService


class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'distance', 'expiration_date', 'user')
    list_filter = ('user', 'expiration_date')
    search_fields = ('name', 'user__username', 'user__email')
    date_hierarchy = 'expiration_date'
    change_list_template = 'admin/coupons/coupon_change_list.html'
    MAPPING = {
        'Промокод': 'name',
        'Ціна': 'price',
        'Відстань': 'distance',
        'Дата завершення': 'expiration_date'
    }

    def upload_excel(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            form = FileImportForm(request.POST, request.FILES)
            if form.is_valid():
                logger = ExcelLogger()
                excel_file = form.cleaned_data.get('excel_file')
                parser = ExcelParserService(excel_file, self.MAPPING, logger)
                data_in_dict = parser.to_dict(sheet_index=0)
                
                for coupon in data_in_dict:
                    try:
                        Coupon.objects.update_or_create(**coupon)
                    except IntegrityError as e:
                        logger.add_info(f'Купон {coupon.get("name", None)} вже існує.')

                return render(request, 'admin/coupons/upload_coupons.html', context={"errors": logger.errors, "info": logger.info})
        
        form = FileImportForm()
        return render(request, 'admin/coupons/upload_coupons.html', context={"form": form})
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [url(r"^upload_excel/$", self.upload_excel, name='upload_excel')]
        return my_urls + urls

admin.site.register(Coupon, CouponAdmin)
