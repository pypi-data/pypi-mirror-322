from ._base import SarvModule
from ._mixins import UrlMixins

class AosPdfTemplates(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'AOS_PDF_Templates'
    _label_en = 'PDF Templates'
    _label_pr = 'قالب های PDF'