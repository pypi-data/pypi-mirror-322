from ._base import SarvModule
from ._mixins import UrlMixins

class KnowledgeBase(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Knowledge_Base'
    _label_en = 'Knowledge Base'
    _label_pr = 'پایگاه دانش'