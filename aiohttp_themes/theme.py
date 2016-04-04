import os
import os.path
import inspect
import hashlib

from mako.lookup import TemplateLookup
from aiohttp.web import Response


THEMES_KEY = 'aiohttp_themes.themes'
THEME_STRATEGY_KEY = 'aiohttp_themes.default_theme'
DEV_RESOURCE_KEY = 'aiohttp_themes.dev'
COMPILED_RESOURCE_KEY = 'aiohttp_themes.compiled'
COMPILED_DIR_KEY = 'aiohttp_themes.compiled_dir'


class Theme:
    response_class = Response
    template_dir = 'templates'
    static_dir = 'static'

    def __init__(self, app, debug=False):
        self.app = app
        self.debug = debug
        template_dir = self.expand_fs_path(self.template_dir)
        self.lookup = TemplateLookup(
            directories=[template_dir],
            input_encoding='utf-8',
            output_encoding='utf-8',
            default_filters=['decode.utf8'],
        )

    @classmethod
    def expand_fs_path(cls, path):
        """
        Given a relative path from this theme to a file, return the full
        filesystem path where that file can be found.
        """
        theme_file = os.path.abspath(inspect.getfile(cls))
        return os.path.join(os.path.dirname(theme_file), path)

    def expand_compiled_path(self, relpath):
        return os.path.join(self.app[COMPILED_DIR_KEY], self.key, relpath)

    def compile(self):
        for asset_key, asset in self.assets.items():
            asset.compile(asset_key, self)

    def write_compiled(self, asset_key, relpath, contents):
        """
        Given a relative asset path and a file contents string, write the
        string to a file with a content-derived filename and return the
        URL that will serve that file.
        """
        hash = hashlib.sha1(contents.encode('utf8')).hexdigest()
        relpath = '%s-%s' % (hash, asset_key)
        path = self.expand_compiled_path(relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(path)
        return relpath

    def make_url(self, asset_key, path, debug):
        """
        Given a relative path from this theme to a file, return the URL path
        where that file will be served in development mode.
        """
        if debug:
            resource_key = DEV_RESOURCE_KEY
        else:
            resource_key = COMPILED_RESOURCE_KEY
        resource = self.app.router.named_resources()[resource_key]
        return resource.url(parts={
            'theme_key': self.key,
            'asset_key': asset_key,
            'path': path,
        })

    def asset_tag(self, asset_key, **kw):
        asset = self.assets[asset_key]
        if self.debug:
            return asset.tag_development(asset_key, self, **kw)
        else:
            # load tag map fromm theme dir
            path = self.expand_compiled_path(asset_key + '.tag')
            with open(path, 'r') as f:
                return f.read().strip()

    def serve_development(self, asset_key, path):
        asset = self.assets[asset_key]
        return asset.serve_development(asset_key, self, path)

    def populate_template_vars(self, request, params):
        params.update({
            'request': request,
            'theme': self,
        })

    def render_template(self, template_name, request, params):
        self.populate_template_vars(request, params)
        templ = self.lookup.get_template(template_name)
        return templ.render_unicode(**params)
