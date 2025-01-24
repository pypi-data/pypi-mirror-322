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
                    return web.Response(status=500)

            except Exception as e:
                self.logger.exception('Health check failed', exc_info=e)
                return web.Response(status=500)

        return web.Response()


class HealthAppFeature(AppFeature):
    NAME = 'health'
    VIEWS = [HealthView]
