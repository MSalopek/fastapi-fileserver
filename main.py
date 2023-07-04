import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from file_browser import search_files, rename, zip_files, exists

from model import RenameRequest, SearchResponse

# could be made configurable
__DEFAULT_DATA_DIR = "./data/"

app = FastAPI()


@app.get("/search/{pathname}", response_model=SearchResponse)
async def search(pathname: str) -> SearchResponse:
    """
    Search for files matching the pattern argument starting from the base directory.
    * in case of no match, return empty list
    * in case of invalid pathname, return empty list
    """
    res = search_files(__DEFAULT_DATA_DIR, pathname)
    return {
        "files": res
    }


@app.post("/rename")
async def rename(rename_in: RenameRequest):
    """
    Rename a file. The file must be under the same directory as the original file.
    * move operations using rename are not allowed
    * in case of invalid pathname or rename operation failure, return 400
    """
    success = rename(__DEFAULT_DATA_DIR, rename_in.from_name, rename_in.to_name)
    if not success:
        raise HTTPException(status_code=400, detail="File could not be renamed")

@app.get("/download")
async def download(q: str):
    """
    Download one or multiple files specified by the "q" string.
    "q" is parsed into string to a list of paths. The paths are relative to the base directory.
    * if multiple files are requested -> download as zip called files.zip (as StreamingResponse)
    * if single file is requested -> download the file (as FileResponse)
    * in case of download operation failure, return 500
    * in case file does not exist, return 404 with a list of files that do not exist
    """
    fnames = q.split(",")
    not_exits = []
    for f in fnames:
        if not exists(__DEFAULT_DATA_DIR, f):
            not_exits.append(f)

    if len(not_exits):
        return HTTPException(status_code=404, detail=f"File(s) not found: {not_exits}")

    try:
        if len(fnames) == 1:
            return FileResponse(
                path=os.path.join(__DEFAULT_DATA_DIR, fnames[0]),
                media_type='application/octet-stream', filename=fnames[0]
            )
        
        # if multiple files -> download zip
        io_buffer = zip_files(__DEFAULT_DATA_DIR, fnames)
        return StreamingResponse(
            iter([io_buffer.getvalue()]),
            media_type="application/x-zip-compressed",
            headers = { "Content-Disposition":f"attachment;filename=files.zip"}
        )
    except Exception as e:
        return HTTPException(status_code=500, detail="File(s) could not be downloaded %s" % e)
