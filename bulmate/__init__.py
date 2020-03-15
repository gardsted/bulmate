import logging
from . import tags as t
import cccp

class init(t.html_tag):
    def __init__(self, *args, **kwargs):
        self.attributes = {}
        self.children   = []
        self.parent     = None
        self.document   = None
        cors = kwargs.pop("cors", False)
        bulma = kwargs.pop("bulma", "https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css")
        fa = kwargs.pop("fa", "https://use.fontawesome.com/releases/v5.3.1/js/all.js")
        axios = kwargs.pop("axios", "https://unpkg.com/axios@0.19.0/dist/axios.min.js")
        jquery =kwargs.pop("jquery", "https://code.jquery.com/jquery-3.3.1.slim.min.js")
        jquery_verify = kwargs.pop("jquery_verify","sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo")
        corsargs={}
        verify_args={}
        if cors:
            corsargs={"crossorigin":cors}
        if jquery_verify:
            verify_args={"integrity": jquery_verify}
        initargs = [
            t.link(rel='stylesheet', href=bulma),
            t.script(defer=True, src=fa),
            t.script(src=axios, **corsargs),
            t.script(src=jquery, **corsargs, **verify_args),
            cccp.CreateReplaceHtmlFunc(),
            cccp.CreateAppendHtmlFunc(),
            cccp.CreatePrependHtmlFunc(),
        ] + list(args)
        super(init, self).__init__(*initargs, **kwargs)

    def _render(self, sb, indent_level, indent_str, pretty, xhtml):
        pretty = pretty and self.is_pretty
        self._render_children(sb, indent_level + 1, indent_str, pretty, xhtml)
        return sb
