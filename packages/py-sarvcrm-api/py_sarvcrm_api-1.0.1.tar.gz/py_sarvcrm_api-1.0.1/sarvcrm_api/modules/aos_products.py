from ._base import SarvModule
from ._mixins import UrlMixins

class AosProducts(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'AOS_Products'
    _label_en = 'Products'
    _label_pr = 'محصولات'