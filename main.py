from fastapi import FastAPI, BackgroundTasks
from time import sleep
import time

app = FastAPI()


def simple_print() -> None:
    # Print a number every second
    for i in range(5):
        print("Background: ", i, time.time())
        sleep(1)


@app.get("/start-task/")
async def start_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(simple_print)
    return {"message": "Background task started"}


# Start the server by running: uvicorn main:app --reload
