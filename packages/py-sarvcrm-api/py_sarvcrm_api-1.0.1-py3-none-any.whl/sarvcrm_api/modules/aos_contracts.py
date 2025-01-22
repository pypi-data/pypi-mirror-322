from ._base import SarvModule
from ._mixins import UrlMixins

class AosContracts(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'AOS_Contracts'
    _label_en = 'Sales Contract'
    _label_pr = 'قراردادهای فروش'