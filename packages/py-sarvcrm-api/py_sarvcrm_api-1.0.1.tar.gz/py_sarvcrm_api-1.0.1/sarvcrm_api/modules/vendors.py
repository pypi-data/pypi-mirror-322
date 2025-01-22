from ._base import SarvModule
from ._mixins import UrlMixins

class Vendors(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Vendors'
    _label_en = 'Vendors'
    _label_pr = 'تامین کنندگان'