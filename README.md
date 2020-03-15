# bulmate 0.0.1


bulmate is a library for creation of server-rendered dynamic, responsive html-pages using bulma as the css library, dominate for tag-rendering, and cccp for the dynamic part, which consists of appending to live dom elements, prepending to live dom elements and replacing live dom elements using callbacks that fetch server rendered snippets. It uses the javascript libraries axios, jquery and fontawesome.

For more of the superpowers of cccp, refer to that project's [excellent documentation and examples](https://github.com/sloev/cccp).

In order to know more about how the inner dynamics of the tag rendering works, refer to the [brilliant documentation](https://github.com/Knio/dominate) of dominate.

Finally Bulma. There is no way You can use this library effectively without reading some of the [extraordinarily bright bulma documentation](https://bulma.io/documentation/).

## Responsive rendering

An reasonably comprehensive example in a flask view could look like this - it will showcase **section**, **hero**, **columns**, and **tile**.


### The wide version


![](example-v0.0.1.png)


### The tall version



![](example-responsive-v0.0.1.png)


Here is the current code

    @blueprint.route('/', methods=["GET"])
    def root():
        return t.html([
    	t.head([bulmate.init(cors=True)]),
    	t.body([
    	    t.hero([
    		t.hero_body([
    		    t.container([
    			t.h1("hero title", cls="title"),
    			t.h2("hero subtitle", cls="subtitle"),
    		    ])
    		]),
    	    ]),
    	    t.section([
    		t.columns([
    		    t.column([t.notification("first column", cls="is-primary has-text-centered")]),
    		    t.column([t.notification("second column", cls="is-primary has-text-centered")]),
    		    t.column([t.notification("third column", cls="is-primary has-text-centered")]),
    		    t.column([t.notification("fourth column", cls="is-primary has-text-centered")]),
    		])
    	    ]),
    	    t.section([
    		t.tile([
    		    t.tile([
    			t.tile([
    			    t.tile([
    				t.tile([
    				    t.p("vertical?", cls="title"),
    				    t.p("or what?", cls="subtitle"),
    				], cls="is-child notification is-primary", tagname="article"),
    				t.tile([
    				    t.p("vertical?", cls="title"),
    				    t.p("or what?", cls="subtitle"),
    				], cls="is-child notification is-warning", tagname="article"),
    			    ], cls="is-parent is-vertical"),
    			    t.tile([
    				t.tile([
    				    t.p("middle", cls="title"),
    				    t.p("with an image", cls="subtitle"),
    				    t.image([t.img(src="https://bulma.io/images/placeholders/640x480.png")], cls="is-4by3"),
    				], cls="is-child notification is-info", tagname="article"),
    			    ], cls="is-parent"),
    			]),
    			t.tile([
    			    t.tile([
    				t.p("wide", cls="title"),
    				t.p("aligned with right", cls="subtitle"),
    				t.content("lotsatext"),
    			    ], cls="is-child notification is-danger", tagname="article"),
    			], cls="is-parent"),
    		    ], cls="is-vertical is-8"),
    		    t.tile([
    			t.tile([
    			    t.tile([
    				t.p("tall tile", cls="title"),
    				t.p("with much more text", cls="subtitle"),
    				t.content("lotsamoretext"),
    			    ], cls="is-child notification is-success", tagname="article"),
    			] ),
    		    ], cls="is-parent"),
    		], cls="is-ancestor")
    	    ]),
    	]),
        ]).render()

## dynamic pages with server rendered snippets

### A Shining example

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
    
    

### Only the wide version shown

![](example-dynamic-v0.0.2.png)

## rendered tags, alphabetically

Here is, for each tag, how it renders with no arguments, for example:

    import bulmate.tags as t
    t.panel().render()
    t.panel(cls="is-success").render()
    t.panel(cls=["is-success", "my-own-class"]).render()
    t.panel(cls="is-success my-own-class").render()
    t.panel(cls=["is-success", "my-own-class"], children=[t.p("some text")]).render()

would produce

    '<article class="panel"></article>'
    '<article class="panel is-success"></article>'
    '<article class="panel is-success my-own-class"></article>'
    '<article class="panel is-success my-own-class"></article>'
    '<article class="panel is-success my-own-class">\n  <p>some text</p>\n</article>'

using the **children** keyword is an addition compared to vanilla dominate - it makes sense to be 
able to transfer children as a keyword argument, as the example above seems bulky for bulma,
specifying the classes always at the end of the arguments.

### bulmate.init

The **bulmate.init** function is special, because it has no outer tag of it's own, it simply appends to the surrounding tag which should be **head**.

    
    <link href="https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css" rel="stylesheet">
    <script defer="defer" src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
    <script src="https://unpkg.com/axios@0.19.0/dist/axios.min.js"></script>
    <script integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script type="text/javascript">function ReplaceHtml(url, id){
            axios.get(url)
            .then(function (response) {
                document.getElementById(id).innerHTML = response.data;
            });
        };</script>
    <script type="text/javascript">function AppendHtml(url, id){
            axios.get(url)
            .then( function (response) {
                $("#"+id).append(response.data);
            });
        };</script>
    <script type="text/javascript">function PrependHtml(url, id){
            axios.get(url)
            .then( function(response) {
                $("#"+id).prepend(response.data);
            });
        };</script>

### \_input

    <input class="input"></input>

### \_object

    <object></object>

### \_time

    <time></time>

### a

    <a></a>

### abbr

    <abbr></abbr>

### address

    <address></address>

### area

    <area>

### article

    <article></article>

### aside

    <aside></aside>

### audio

    <audio></audio>

### b

    <b></b>

### base

    <base>

### bdi

    <bdi></bdi>

### bdo

    <bdo></bdo>

### blockquote

    <blockquote></blockquote>

### body

    <body></body>

### box

    <div class="box"></div>

### br

    <br>

### breadcrumb

    <nav class="breadcrumb"></nav>

### button

    <p class="button"></p>

### buttons

    <div class="buttons"></div>

### canvas

    <canvas></canvas>

### caption

    <caption></caption>

### card

    <div class="card"></div>

### card\_content

    <div class="card-content"></div>

### card\_footer

    <div class="card-footer"></div>

### card\_footer\_item

    <a class="card-footer-item"></a>

### card\_header\_icon

    <a class="card-header-icon"></a>

### card\_header\_title

    <p class="card-header-title"></p>

### card\_image

    <div class="card-image"></div>

### checkbox

    <label class="checkbox"></label>

### cite

    <cite></cite>

### code

    <code></code>

### col

    <col>

### colgroup

    <colgroup></colgroup>

### column

    <div class="column"></div>

### columns

    <div class="columns"></div>

### command

    <command>

### comment

    <!---->

### container

    <div class="container"></div>

### content

    <div class="content"></div>

### control

    <div class="control"></div>

### datalist

    <datalist></datalist>

### dd

    <dd></dd>

### del\_

    <del></del>

### delete

    <button class="delete"></button>

### details

    <details></details>

### dfn

    <dfn></dfn>

### div

    <div></div>

### dl

    <dl></dl>

### dropdown\_content

    <div class="dropdown-content"></div>

### dropdown\_divider

    <hr class="dropdown-divider"></hr>

### dropdown\_menu

    <div class="dropdown-menu"></div>

### dropdown\_trigger

    <div class="dropdown-trigger"></div>

### dt

    <dt></dt>

### em

    <em></em>

### embed

    <embed>

### field

    <div class="field"></div>

### fieldset

    <fieldset></fieldset>

### figcaption

    <figcaption></figcaption>

### figure

    <figure></figure>

### file

    <div class="file"></div>

### file\_cta

    <span class="file-cta"></span>

### file\_icon

    <span class="file-icon"></span>

### file\_input

    <input class="file-input"></input>

### file\_label

    <label class="file-label"></label>

### file\_name

    <span class="file-name"></span>

### font

    <font></font>

### footer

    <footer class="footer"></footer>

### form

    <form></form>

### h1

    <h1></h1>

### h2

    <h2></h2>

### h3

    <h3></h3>

### h4

    <h4></h4>

### h5

    <h5></h5>

### h6

    <h6></h6>

### head

    <head></head>

### header

    <header></header>

### hero

    <section class="hero"></section>

### hero\_body

    <div class="hero-body"></div>

### hgroup

    <hgroup></hgroup>

### hr

    <hr>

### html

    <html></html>

### i

    <i></i>

### icon

    <span class="icon"></span>

### iframe

    <iframe></iframe>

### image

    <figure class="image"></figure>

### img

    <img>

### input

    <input class="input"></input>

### input\_

    <input class="input"></input>

### ins

    <ins></ins>

### kbd

    <kbd></kbd>

### keygen

    <keygen>

### label

    <label class="label"></label>

### legend

    <legend></legend>

### li

    <li></li>

### link

    <link>

### main

    <main></main>

### map\_

    <map></map>

### mark

    <mark></mark>

### media

    <div class="media"></div>

### media\_content

    <div class="media-content"></div>

### media\_left

    <div class="media-left"></div>

### media\_right

    <div class="media-right"></div>

### menu

    <aside class="menu"></aside>

### menu\_label

    <p class="menu-label"></p>

### menu\_list

    <ul class="menu-list"></ul>

### message

    <article class="message"></article>

### message\_bodydropdown

    <div class="message-bodydropdown"></div>

### message\_header

    <div class="message-header"></div>

### meta

    <meta>

### meter

    <meter></meter>

### modal

    <div class="modal"></div>

### modal\_background

    <div class="modal-background"></div>

### modal\_close

    <button class="modal-close"></button>

### modal\_content

    <div class="modal-content"></div>

### nav

    <nav></nav>

### navbar

    <nav class="navbar"></nav>

### navbar\_brand

    <div class="navbar-brand"></div>

### navbar\_end

    <div class="navbar-end"></div>

### navbar\_item

    <a class="navbar-item"></a>

### navbar\_start

    <div class="navbar-start"></div>

### noscript

    <noscript></noscript>

### notification

    <div class="notification"></div>

### object\_

    <object></object>

### ol

    <ol></ol>

### optgroup

    <optgroup></optgroup>

### option

    <option></option>

### output

    <output></output>

### p

    <p></p>

### pagination

    <nav class="pagination"></nav>

### pagination\_ellipsis

    <span class="pagination-ellipsis"></span>

### pagination\_link

    <a class="pagination-link"></a>

### pagination\_list

    <ul class="pagination-list"></ul>

### pagination\_next

    <a class="pagination-next"></a>

### pagination\_previous

    <a class="pagination-previous"></a>

### panel

    <article class="panel"></article>

### panel\_block

    <a class="panel-block"></a>

### panel\_heading

    <p class="panel-heading"></p>

### panel\_tabs

    <p class="panel-tabs"></p>

### param

    <param>

### pre

    <pre></pre>

### progress

    <progress class="progress"></progress>

### q

    <q></q>

### radio

    <input class="radio"></input>

### rp

    <rp></rp>

### rt

    <rt></rt>

### ruby

    <ruby></ruby>

### s

    <s></s>

### samp

    <samp></samp>

### script

    <script></script>

### section

    <section class="section"></section>

### select

    <div class="select"></div>

### small

    <small></small>

### source

    <source>

### span

    <span></span>

### strong

    <strong></strong>

### style

    <style></style>

### sub

    <sub></sub>

### subtitle

    <p class="subtitle"></p>

### summary

    <summary></summary>

### sup

    <sup></sup>

### table

    <table></table>

### tabs

    <div class="tabs"></div>

### tag

    <span class="tag"></span>

### tbody

    <tbody></tbody>

### td

    <td></td>

### textarea

    <textarea class="textarea"></textarea>

### tfoot

    <tfoot></tfoot>

### th

    <th></th>

### thead

    <thead></thead>

### tile

    <div class="tile"></div>

### time\_

    <time></time>

### title

    <p class="title"></p>

### tr

    <tr></tr>

### track

    <track>

### u

    <u></u>

### ul

    <ul></ul>

### var

    <var></var>

### video

    <video></video>

### wbr

    <wbr>


## History

### Version 0.0.2 - Mar 15, 2020

 * typos, additional image, onclick as list possible, more docs, examples

### Version 0.0.1 - Mar 15, 2020

 * first

