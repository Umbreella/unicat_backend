from ..graphql.loaders import Loaders


class LoaderMiddleware:
    def resolve(self, next, root, info, **kwargs):
        if not hasattr(info.context, 'loaders'):
            info.context.loaders = Loaders()

        return next(root, info, **kwargs)
