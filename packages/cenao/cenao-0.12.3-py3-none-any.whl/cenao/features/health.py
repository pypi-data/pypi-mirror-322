from aiohttp import web

from cenao.app import AppFeature
from cenao.view import View


class HealthView(View):
    ROUTE = '/internal/health'

    async def get(self):
        for ft in self.app.ft:
            try:
                result = await ft.check_health()
                if not result:
                    self.logger.error("Feature %s is not healthy", ft.NAME)
                    return web.Response(status=500, text=f"Feature {ft.NAME} is not healthy")

            except Exception as e:
                self.logger.error("Feature %s is not healthy (%r)", ft.NAME, e)
                return web.Response(status=500, text=f"Feature {ft.NAME} is not healthy")

        return web.Response()


class HealthAppFeature(AppFeature):
    NAME = 'health'
    VIEWS = [HealthView]
