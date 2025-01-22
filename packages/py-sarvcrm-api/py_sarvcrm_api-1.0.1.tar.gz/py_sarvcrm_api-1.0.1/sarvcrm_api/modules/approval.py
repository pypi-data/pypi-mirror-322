from ._base import SarvModule
from ._mixins import UrlMixins

class Approval(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Approval'
    _label_en = 'Approval'
    _label_pr = 'تاییدیه'