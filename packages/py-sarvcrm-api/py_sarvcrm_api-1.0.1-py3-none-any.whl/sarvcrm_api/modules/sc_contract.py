from ._base import SarvModule
from ._mixins import UrlMixins

class ScContract(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'sc_Contract'
    _label_en = 'Support Contracts'
    _label_pr = 'قراردادهای پشتیبانی'