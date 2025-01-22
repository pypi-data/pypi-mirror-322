from ._base import SarvModule
from ._mixins import UrlMixins

class CommunicationsTarget(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Communications_Target'
    _label_en = 'Communications Target'
    _label_pr = 'هدف ارتباطات'