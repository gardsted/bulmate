import flask
import bulmate
import bulmate.tags as t
import cccp
import uuid

app = flask.Flask(__name__)

def column_jack(letter):
    return t.column(
        id="coll_"+letter,
        cls=["is-primary", "has-text-centered"],
        children = [
            t.div(
                id="shine_" + letter,
            ),
            t.div(
                id="butt_" + letter,
                children= [
                    t.button(
                        cls=["is-warning"],
                        onclick=[
                            cccp.replaceHtml("/more_buttons/?letter="+letter, "butt_"+letter),
                            cccp.appendHtml("/shine/", "shine_"+letter),
                        ],
                        children=["Add some shine"],
                    ),
                ],
            )
        ])


@app.route('/shine/')
def shine():
    return "All work and no play makes Jack a dull boy. " * 10


@app.route('/')
def index():
    return t.html(
        children=[
    	    t.head([bulmate.init(cors=True)]),
    	    t.body(
                children=[
                    t.section(
                        children=[t.columns([column_jack(letter) for letter in "jack"])]
                    ),
                ],
            ),
        ]).render()


@app.route('/more_buttons/')
def more_buttons():
    letter = flask.request.args["letter"]
    return t.div(
        children=[
            t.button(
                cls=["is-danger"],
                onclick=cccp.appendHtml("/shine/", "shine_" + letter),
                children=["Add some more shine"],
            ),
            t.button(
                cls=["is-success"],
                onclick=[
                    cccp.replaceHtml("/nothing/", "shine_" + letter),
                    cccp.replaceHtml("/one_button/?letter=" + letter, "butt_" + letter),
                ],
                children=["Remove everything"],
            ),
        ]
    ).render()

@app.route('/one_button/')
def one_button():
    letter = flask.request.args["letter"]
    return t.div(
        children= [
            t.button(
                cls=["is-warning"],
                onclick=[
                    cccp.replaceHtml("/more_buttons/?letter="+letter, "butt_"+letter),
                    cccp.appendHtml("/shine/", "shine_" + letter)
                ],
                children=["Add some shine"],
            ),
        ],
    ).render()


@app.route('/nothing/')
def nothing():
    return t.comment("all has been deleted").render()


if __name__ == "__main__":
    import os
    app.run(debug=True, host=os.environ.get("HOST","127.0.0.1"))

