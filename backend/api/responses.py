from fastapi.responses import JSONResponse
import settings
class CustomJSONResponse(JSONResponse):
    
    def render(self, content):
        if isinstance(content, dict):
            content["version"] = settings.API_VERSION
        return super().render(content)