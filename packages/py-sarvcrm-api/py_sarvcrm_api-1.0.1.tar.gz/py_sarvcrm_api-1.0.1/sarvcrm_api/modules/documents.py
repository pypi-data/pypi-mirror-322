from ._base import SarvModule
from ._mixins import UrlMixins

class Documents(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Documents'
    _label_en = 'Documents'
    _label_pr = 'اسناد'