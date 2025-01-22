from ._base import SarvModule
from ._mixins import UrlMixins

class Contacts(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Contacts'
    _label_en = 'Contacts'
    _label_pr = 'افراد'