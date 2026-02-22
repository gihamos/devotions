from authMiddleware import AuthMiddlawre
from currentUserMiddleware import CurrentUserMiddleware
from errorHandlerMiddleware import ErrorHandlerMiddleware
from timing import TimingMiddleware

def register_middlewares(app):
    app.add_middleware(ErrorHandlerMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(AuthMiddlawre)
    app.add_middleware(CurrentUserMiddleware)
