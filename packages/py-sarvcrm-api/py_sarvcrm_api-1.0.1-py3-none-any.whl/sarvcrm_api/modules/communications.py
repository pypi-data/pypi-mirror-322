from ._base import SarvModule
from ._mixins import UrlMixins

class Communications(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Communications'
    _label_en = 'Communications'
    _label_pr = 'ارتباطات'