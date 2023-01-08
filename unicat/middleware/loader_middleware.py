from ..graphql.loaders import Loaders


class LoaderMiddleware:
    def resolve(self, next, root, info, **args):
        if not hasattr(info.context, 'loaders'):
            info.context.loaders = Loaders()

        return next(root, info, **args)
