from ._base import SarvModule
from ._mixins import UrlMixins

class Accounts(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Accounts'
    _label_en = 'Accounts'
    _label_pr = 'حساب ها'