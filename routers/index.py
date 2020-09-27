from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

router = APIRouter()

# TODO - How to import a html file
def readme_response():
    html_content = """
    <html>
        <head>
            <title>TDC - Talkdesk Challengen</title>
        </head>
        <body>
            <h1>I need to do a README</h1>
            <p>If you are running in a localhost, <a href="http://127.0.0.1:8000/docs">click here</a> to test api</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router.get("/", response_class=HTMLResponse, tags=['home'])
async def list():
    return readme_response()
