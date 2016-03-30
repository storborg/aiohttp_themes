default_sentinel = object()


class SafeLiteral:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    __html__ = __str__


class Asset:
    pass


class SASSAsset(Asset):
    def __init__(self, relpath, sassc_path='sassc'):
        self.relpath = relpath
        self.sassc_path = sassc_path

    def __repr__(self):
        return '<SASSAsset %s>' % self.relpath

    def tag_development(self, url):
        return SafeLiteral('<link rel="stylesheet" href="%s">' % url)

    def tag_production(self, url):
        raise NotImplementedError

    def serve(self):
        return 'body { font-family: "Lucida Grande", sans-serif; }'


class RequireJSAsset(Asset):
    def __init__(self, relpath, require_config_path=default_sentinel):
        self.relpath = relpath

    def __repr__(self):
        return '<RequireJSAsset %s>' % self.relpath

    def tag_development(self, url):
        return SafeLiteral('<script src="%s"></script>' % url)

    def tag_production(self, url):
        pass

    def serve(self):
        return 'console.log("hello");'
