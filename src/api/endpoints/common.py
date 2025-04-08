from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def main_page() -> dict:
    """Обработка обращения к главной странице."""
    return {'status': 'OK'}
