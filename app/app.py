import fastapi
import schema
from crud import add_item, delete_item, get_item, search_items
from dependencies import SessionDependency
from fastapi import HTTPException
from lifespan import lifespan
from models import Advertisement

app = fastapi.FastAPI(
    title="Сервис объявления",
    description="Поиск, получение, создание, обновление и удаление объявлений",
    version="0.1",
    lifespan=lifespan
)


@app.get("/advertisement")
async def get_advertisement_from_qs(
        session: SessionDependency, id=None, title=None, description=None,
        price=None, owner=None, created_at=None
):
    """View-функция получения объявления из query string"""
    qs_params = {}
    for k, v in locals().items():
        if k not in ('session', 'qs_params') and v is not None:
            qs_params.setdefault(k, v)
        # Ограничение: поиск возможен только по одному параметру
        if len(qs_params) > 1:
            raise HTTPException(status_code=400,
                                detail='Too many parameters in query string')
    if len(qs_params) == 0:
        raise HTTPException(status_code=404,
                            detail="Invalid query parameters")
    field = list(qs_params.keys())[0]
    value = list(qs_params.values())[0]
    res = await search_items(session, Advertisement, field, value)
    return res


@app.get("/advertisement/{advertisement_id}",
         response_model=schema.GetAdvertisementResponse)
async def get_advertisement(advertisement_id: int, session: SessionDependency):
    """View-функция получения объявления по id"""
    item = await get_item(advertisement_id, Advertisement, session)
    return item.dict


@app.post("/advertisement", response_model=schema.CreateAdvertisementResponse)
async def create_advertisement(
        advertisement_json: schema.CreateAdvertisementRequest,
        session: SessionDependency
):
    item = Advertisement(**advertisement_json.dict())
    await add_item(item, session)
    return item.id_dict


@app.patch("/advertisement/{advertisement_id}",
           response_model=schema.UpdateAdvertisementResponse)
async def update_advertisement(
        advertisement_id: int,
        advertisement_json: schema.UpdateAdvertisementRequest,
        session: SessionDependency
):
    item = await get_item(advertisement_id, Advertisement, session)
    item_update = advertisement_json.dict(exclude_unset=True)
    for k, v in item_update.items():
        setattr(item, k, v)
    await add_item(item, session)
    return item.id_dict


@app.delete("/advertisement/{advertisement_id}",
            response_model=schema.DeleteAdvertisementResponse)
async def delete_advertisement(
        advertisement_id: int,
        session: SessionDependency
):
    await delete_item(advertisement_id, Advertisement, session)
    return {'status': 'success'}
