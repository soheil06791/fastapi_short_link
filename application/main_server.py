import os
from fastapi import FastAPI, status, HTTPException, responses
from fastapi.middleware import cors
from utils.db_manager import execute
from utils.query_manger import *
from app.routers import router


app = FastAPI(docs_url='/')

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##########API##########

@app.on_event('startup')
async def before_run_server():
    await execute(create_users_table)
    await execute(create_link_table)
    


@app.get("/{slug}", status_code= status.HTTP_200_OK, tags = ['Others'])
async def return_org_url(slug: str):
    try:
        org_url = await execute(get_user_link, [slug])
        if not org_url:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Slug Not Found")
        org_url = org_url[0]
        return responses.RedirectResponse(org_url['url'], status_code= status.HTTP_308_PERMANENT_REDIRECT)
    except Exception as e:
        error = e.__class__.__name__
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)


app.include_router(router, prefix='/app')