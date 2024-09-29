
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from imagekit.admin import AdminThumbnail

from backend.models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, \
    Contact, ConfirmEmailToken


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """
    model = User


    fieldsets = (
        (None, {'fields': ('email', 'password', 'type', 'avatar')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'avatar_thumbnail')
    avatar_thumbnail = AdminThumbnail(image_field='avatar_thumbnail')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):



    model = Shop

    fieldsets = (
        (None, {'fields': ('name', 'state','url','user')}),
    )
    list_display = ('name', 'state')
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    list_display = ('name', 'get_shops')

    def get_shops(self, obj):
        return ', '.join([shop.name for shop in obj.shops.all()])
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product

    fieldsets = (
        (None, {'fields': ('name', 'category')}),
    )
    list_display = ('name', 'category')
    pass


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    model = ProductInfo

    fieldsets = (
        (None, {'fields': ('product', 'model','image', 'quantity', 'price', 'price_rrc','shop','external_id')}),
    )
    list_display = ('product', 'model', 'quantity', 'price', 'price_rrc','shop','external_id','image_thumbnail')
    image_thumbnail = AdminThumbnail(image_field='image_thumbnail')


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    model = Parameter

    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    list_display = ('name',)
    pass


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    model = ProductParameter

    fieldsets = (
        (None, {'fields': ('parameter', 'product_info', 'value')}),
    )
    list_display = ('id', 'parameter', 'product_info', 'value')


    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order

    fieldsets = (
        (None, {'fields': ('user', 'state', 'contact', )}),
    )
    list_display = ('user', 'dt', 'state', 'contact')
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem

    fieldsets = (
        (None, {'fields': ('order', 'product_info', 'quantity')}),
    )
    list_display = ('order', 'product_info', 'quantity')
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    model = Contact

    fieldsets = (
        (None, {'fields': ('user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')}),
    )
    list_display = ('user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')
    pass


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)

