from ._base import SarvModule
from ._mixins import UrlMixins

class PurchaseOrder(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Purchase_Order'
    _label_en = 'Purchase Order'
    _label_pr = 'سفارش خرید'