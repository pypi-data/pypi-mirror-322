from ._base import SarvModule
from ._mixins import UrlMixins

class AosQuotes(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'AOS_Quotes'
    _label_en = 'Quotes'
    _label_pr = 'پیش فاکتورها'