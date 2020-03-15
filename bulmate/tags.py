import logging
import dominate
import dominate.tags
from dominate.dom_tag import dom_tag
from dominate.dom1core import dom1core


class html_tag(dom_tag, dom1core):

    def __init__(self, *args, **kwargs):

        # children should be a kwarg if so desired
        children = kwargs.pop("children", [])
        if isinstance(children, str):
            children = [children]
        args = children + list(args) 

        # give css classes as list if co desired
        css_classes = []
        for cn in ["_class", "cls", "className", "class_name"]:
            cls = kwargs.pop(cn,[])
            if isinstance(cls, str):
                cls = cls.split(" ")
            css_classes.extend(cls)

        # assemble all css classes again, if any
        if css_classes:
            kwargs["cls"] = " ".join(css_classes)

        # bypass autowash for dominate tags
        if not self.__class__.__name__ in allbulmate:
            super(html_tag, self).__init__(*args, **kwargs)
            return

        # for nameclashes and general disorderly manually set tagname
        tagname = kwargs.pop("tagname", None)
        if tagname is not None:
            setattr(self, "tagname", tagname)

        # find required classes, you can do: tag.clsnames=[] to avoid
        clsnames = [
            x.replace("_","-")
            for x in getattr(self, "clsnames",[self.__class__.__name__])
        ]

        # set first of the probable classes if none set
        if clsnames and not set(clsnames) & set(css_classes):
            # it must have one of these classes - first is default
            css_classes[0:0] = [clsnames[0]]
            kwargs["cls"] = " ".join(css_classes)
        
        super(html_tag, self).__init__(*args, **kwargs)

for thing in dir(dominate.tags):
    attr = getattr(dominate.tags, thing)
    if not getattr(attr, "__bases__", False):
        continue
    if attr.__bases__ == (dominate.tags.html_tag,):
        globals()[thing] = type(thing, (html_tag,), {})
        globals()[thing].is_single = attr.is_single


bulmatespecific = {
    "div": [
        "columns", "column", "container", "notification", "section",
        "tabs", "hero", "navbar_brand", "navbar_start", "navbar_end",
        "buttons", "modal", "modal_background", "modal_content",
        "message_header", "message_body" "dropdown", "dropdown_trigger",
        "dropdown_menu", "dropdown_content", "card", "card_image", "media",
        "media_left", "media_right", "card_content", "media_content", "content",
        "card_footer", "box", "file", "control", "select", "field", "tile",
        "hero_body"
    ], 
    "label": [
        "file_label", "checkbox", "label", 
    ],
    "input":[
        "file_input", "radio", "input", "_input", "input_"
    ],
    "p": [
        "panel_heading", "panel_tabs", "menu_label", "title", "subtitle",
        "card_header_title", 
    ],
    "a": [
        "panel_block","pagination_previous", "pagination_next", "pagination_link",
        "navbar_item", "card_footer_item", "card_header_icon", 
    ],
    "nav":[
        "pagination", "navbar", "breadcrumb"
    ],
    "ul":[
        "pagination_list", "menu_list",
    ],
    "span":[
        "pagination_ellipsis", "icon", "tag", "file_cta", "file_icon", "file_name", 
    ],
    "article":[
        "panel", "message"
    ],
    "button": [
        "modal_close", "delete"
    ],
    "aside":[
        "menu", 
    ],
    "hr": [
        "dropdown_divider",
    ],
    "figure":[
        "image",
    ],
    "progress":[
        "progress",
    ],
    "textarea":[
        "textarea",
    ],
    "footer": [
        "footer",
    ],
    "section":[
        "section", "hero", 
    ],
    "object":[
        "object_", "_object",
    ],
    "time":[
        "_time", "time_"
    ]
}

"""
TODO: complex rendering for checkbox label with checkbox input inside
      select and so on
"""


allbulmate = []
for tagname, items in bulmatespecific.items():
    for thing in items:
        globals()[thing] = type(thing, (html_tag,), {})
        globals()[thing].tagname = tagname
    allbulmate.extend(items)
allbulmate = set(allbulmate)


class time_(html_tag):
    tagname = "time"
    clsnames = []


class _time(html_tag):
    tagname = "time"
    clsnames = []


class object_(html_tag):
    tagname = "object"
    clsnames = []


class _object(html_tag):
    tagname = "object"
    clsnames = []


class input_(html_tag):
    tagname = "input"
    clsnames = [tagname]


class _input(html_tag):
    tagname = "input"
    clsnames = [tagname]

from dominate.tags import comment
