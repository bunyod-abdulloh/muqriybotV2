from loader import dp
from .throttling import ThrottlingMiddleware
from .media_group import AlbumMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(AlbumMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
