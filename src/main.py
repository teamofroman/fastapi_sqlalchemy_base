import uvicorn

from api.fastapi_app import get_fastapi_app
from core.config import settings

if __name__ == '__main__':
    uvicorn.run(get_fastapi_app(), host='0.0.0.0', port=settings.app_port)
