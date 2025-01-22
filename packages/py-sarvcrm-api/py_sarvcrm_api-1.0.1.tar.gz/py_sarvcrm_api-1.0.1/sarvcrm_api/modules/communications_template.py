from ._base import SarvModule
from ._mixins import UrlMixins

class CommunicationsTemplate(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Communications_Template'
    _label_en = 'Communications Template'
    _label_pr = 'قالب ارتباطات'