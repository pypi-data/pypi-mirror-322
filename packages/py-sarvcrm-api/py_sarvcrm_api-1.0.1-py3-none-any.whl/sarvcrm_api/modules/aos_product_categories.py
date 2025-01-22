from ._base import SarvModule
from ._mixins import UrlMixins

class AosProductCategories(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'AOS_Product_Categories'
    _label_en = 'Product Categories'
    _label_pr = 'دسته های محصول'