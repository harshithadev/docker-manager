import uvicorn
from docker import DockerClient
from docker.errors import DockerException, NotFound
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi


app = FastAPI() #FastAPI object

#OPENAPI schema for looks of the docs
def my_schema():
   openapi_schema = get_openapi(
       title="Docker Manager Application",
       version="1.0",
       description="Control your Docker Applications in here !",
       routes=app.routes,
   )
   app.openapi_schema = openapi_schema
   return app.openapi_schema

app.openapi = my_schema

client =  DockerClient()   #Docker client to extract all info from docker daemon

#Docker version check API
@app.get("/", tags=["Default"])
async def version():
    return {"Docker version" : client.version()}

### CONTAINER APIs

#List all containers
@app.get("/container_list", tags=["Container APIs"])
async def container_list():
    try:
        containers_list = client.containers.list(all=True)
        containers = []
        for container in containers_list:
            containers.append(
                {"container_id" : container.id, 
                 "container_name" : container.name, 
                 "container_status" : container.status
                }
            )
        return {"containers":containers}
    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))

#Start a container with specific container ID
@app.post("/container/{container_id}/start", tags=["Container APIs"])
async def container_start(container_id:str):
    try:
        container = client.containers.get(container_id)
        container.start()
        return f"Container with {container_id} started successfully !"
    except NotFound:
        raise HTTPException(status_code=404, detail="Container not found")
    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Stop a container with specific container ID
@app.post("/container/{container_id}/stop", tags=["Container APIs"])
async def container_start(container_id:str):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Container with {container_id} stopped successfully !"
    except NotFound:
        raise HTTPException(status_code=404, detail="Container not found")
    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Rename a container with specific container ID
@app.post("/container/{container_id}/rename", tags=["Container APIs"])
async def container_start(container_id:str, newName):
    try:
        container = client.containers.get(container_id)
        container.rename(newName)
        return f"Container with {container_id} Renamed successfully with {newName}!"
    except NotFound:
        raise HTTPException(status_code=404, detail="Container not found")
    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))

#Remove a container with specific container ID
@app.post("/container/{container_id}/remove", tags=["Container APIs"])
async def container_start(container_id:str):
    try:
        container = client.containers.get(container_id)
        container.remove()
        return f"Container with {container_id} removed successfully !"
    except NotFound:
        raise HTTPException(status_code=404, detail="Container not found")
    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Logs a container with specific container ID
@app.get("/container/{container_id}/logs", tags=["Container APIs"])
async def container_start(container_id:str):
    try:
        container = client.containers.get(container_id)
        logs = container.logs()
        return {"logs" : str(logs) }
    except NotFound:
        raise HTTPException(status_code=404, detail="Container not found")
    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))

#TODO
#Create container API 
#Image APIs
#Refactor code

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


    