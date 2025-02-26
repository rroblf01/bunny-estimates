from ninja import NinjaAPI

from estimates.api import router as estimates_router

api = NinjaAPI()

api.add_router("/estimates/", estimates_router)
