from ._base import SarvModule
from ._mixins import UrlMixins

class Emails(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Emails'
    _label_en = 'Emails'
    _label_pr = 'ایمیل ها'