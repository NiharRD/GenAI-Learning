from fastapi import FastAPI,Query
from .rq_client.rq_client import queue
from .queues.worker import process_query
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "The server is up and running "}


@app.post("/chat")
def chat( query: str = Query( ... , description= "The chat query of user") ):
    
    job=queue.enqueue(process_query,query=query)

    return {"status": "queued", "job_id": job.id}


@app.get("/jobStatus")
def get_result( 
    job_id: str = Query(..., description="Job ID")
):
    job=queue.fetch_job(job_id=job_id)
    result= job.return_value()

    return { "result" : result}
