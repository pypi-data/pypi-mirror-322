from ._base import SarvModule
from ._mixins import UrlMixins

class Branches(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Branches'
    _label_en = 'Branches'
    _label_pr = 'شعب'