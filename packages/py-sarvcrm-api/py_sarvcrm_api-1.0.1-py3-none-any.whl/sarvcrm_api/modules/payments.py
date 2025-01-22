from ._base import SarvModule
from ._mixins import UrlMixins

class Payments(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Payments'
    _label_en = 'Payments'
    _label_pr = 'پرداخت ها'