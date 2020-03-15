import unittest
import bulmate
import bulmate.tags as t
import os
import pathlib
import json
import cccp
testbase = pathlib.Path(__file__).resolve().parent
testdata = testbase / "testdata.json"

if os.environ.get("WRITE_BULMATE_ARTEFACTS",""):
    readme_in = testbase.parent / "README.in"
    readme_md = testbase.parent / "README.md"
    version = testbase.parent / "VERSION"
    history = testbase.parent / "HISTORY"
    shining = testbase.parent / "examples" / "example_dynamic.py"
    tagtests={}
    for thing in dir(t):
        attr = getattr(t, thing)
        if not getattr(attr, "__bases__", False):
            continue
        if attr.__bases__ == (t.html_tag,) or thing == "comment":
            tagtests[thing] = attr().render(indent='')
    tagtests["init"] = bulmate.init().render(indent='')
    testdata.write_text(json.dumps(tagtests, indent=4))
    tested_tags = []
    for tagname, expected in [("bulmate.init\n\n"
        "The **bulmate.init** function is special, because it has no outer "
        "tag of it's own, it simply appends to the surrounding tag which "
        "should be **head**." , tagtests.pop("init"))
    ] + sorted(tagtests.items()):
        tested_tags.append("### %s\n\n%s\n" %(
            tagname.replace("_","\\_"), "\n".join([
                "    %s" % line
                for line in expected.split("\n")
                if tagname != "init"
            ])))
    readme_md.write_text(readme_in.read_text(
    ).replace("THE_HISTORY", history.read_text()
    ).replace("THE_VERSION_STRING", version.read_text()
    ).replace("THE_RENDERED_TAGS", "\n".join(tested_tags)
    ).replace("THE_SHINING_EXAMPLE", "\n".join([
        "    %s" % line
        for line in shining.read_text().split("\n")
    ]))
    )


class Tests(unittest.TestCase):
    def test_all_tags(self):
        subtests = json.loads(testdata.read_text())
        for tagname, expected in subtests.items():
            with self.subTest("testing return value for " + tagname):
                if tagname == "init":
                    continue
                self.assertEqual(getattr(t,tagname)().render(), expected)
        self.assertEqual(bulmate.init().render(indent=''), subtests["init"])

    def test_init_render_cors(self):
        self.maxDiff = None
        init = bulmate.init(cors="z", bulma="a", fa="b", axios="c",
                            indent=0, jquery="d", jquery_verify="e")
        self.assertEqual(init.render(indent='').strip(),"\n".join([
            '<link href="a" rel="stylesheet">',
            '<script defer="defer" src="b"></script>',
            '<script crossorigin="z" src="c"></script>',
            '<script crossorigin="z" integrity="e" src="d"></script>',
            cccp.CreateReplaceHtmlFunc().render(),
            cccp.CreateAppendHtmlFunc().render(),
            cccp.CreatePrependHtmlFunc().render(),
        ]))
        
    def test_init_render_no_cors(self):
        self.maxDiff = None
        init = bulmate.init(bulma="a", fa="b", axios="c", jquery="d",
                            jquery_verify="e")
        self.assertEqual(init.render(indent='').strip(),"\n".join([
            '<link href="a" rel="stylesheet">',
            '<script defer="defer" src="b"></script>',
            '<script src="c"></script>',
            '<script integrity="e" src="d"></script>',
            cccp.CreateReplaceHtmlFunc().render(),
            cccp.CreateAppendHtmlFunc().render(),
            cccp.CreatePrependHtmlFunc().render(),
        ]))

    def test_init_render_no_cors_no_verify(self):
        self.maxDiff = None
        init = bulmate.init(bulma="a", fa="b", axios="c", jquery="d",
                            jquery_verify=False)
        self.assertEqual(init.render(indent='').strip(),"\n".join([
            '<link href="a" rel="stylesheet">',
            '<script defer="defer" src="b"></script>',
            '<script src="c"></script>',
            '<script src="d"></script>',
            cccp.CreateReplaceHtmlFunc().render(),
            cccp.CreateAppendHtmlFunc().render(),
            cccp.CreatePrependHtmlFunc().render(),
        ]))
