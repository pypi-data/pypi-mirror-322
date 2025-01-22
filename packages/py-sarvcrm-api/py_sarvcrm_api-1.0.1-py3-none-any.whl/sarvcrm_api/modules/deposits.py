from ._base import SarvModule
from ._mixins import UrlMixins

class Deposits(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Deposits'
    _label_en = 'Deposits'
    _label_pr = 'ودیعه'