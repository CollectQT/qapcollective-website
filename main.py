'''
__name__ = main.py
__desc__ = Routing and content generation file
__sign__ = Lynn Cyrin

Use:
[Production] '$ foreman start'
[Developement] '$ python main.py' (runs in debug mode)
'''

# builtin
import glob
# external
import yaml
import flask
import flask.ext.scss
# custom
from scripts import cms

# shortcuts
render = flask.render_template
build = cms.build_html

# start app and set configuration
app = flask.Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(__name__)
for key, value in yaml.load(file('config/config.yaml','r')).items():
    app.config[key] = value

# Views! i.e. what the user gets when they type in our url

# the homepage is special because it reads in the readme
@app.route('/')
def index ():
    return render('post.html', html_content=build("readme"))

# every other path reads from paths/<url_input>
# ex: website.com/cats -> firestarter/paths/cats
@app.route('/<path>')
def dynamic_path(path):
    # frist check that path is empty, if so then 404
    if len(glob.glob('paths/'+path+'*')) == 0: return page_not_found(404)
    return render('post.html', html_content=build("paths/"+path))

# except for /static/* in which case we render the file itself
@app.route('/static/<path:filename>')
def base_static(filename):
    return flask.send_from_directory(app.root_path + '/static/', filename)

# 404 is special because it needs @app.errorhandler(404)
@app.errorhandler(404)
def page_not_found (e):
    return render('post.html', html_content=build("paths/404"))

# debug mode start options

if __name__ == '__main__':
    app.config['DEBUG'] = True
    flask.ext.scss.Scss(app)
    app.run()