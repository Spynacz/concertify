from rest_framework.routers import Route, DynamicRoute, SimpleRouter


class VoteRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'delete': 'destroy',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        )
    ]
