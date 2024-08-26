import pytest
import subprocess
import time
import signal
import httpx
import pytest_asyncio

from fastapi.testclient import TestClient
from main import app


# It does not work with TestClient or ASGI framework
@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


# Define a pytest fixture to start and stop the FastAPI server
@pytest_asyncio.fixture(scope="session")
def start_fastapi_server():
    # Start FastAPI server in a separate process
    # Assume your FastAPI main file is named `main.py` and the app instance is named `app`
    # Also assume you're using uvicorn with default host and port (127.0.0.1:8000)
    command = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("TEST")

    # Wait for the server to start (you might adjust this sleep time based on your server's start-up time)
    time.sleep(5)  # Wait for the server to ensure it's up and running

    # Yield control back to the test function
    yield

    print("END")
    # After the tests complete, shut down the server
    process.send_signal(
        signal.SIGINT
    )  # Send interrupt signal to gracefully shut down the server
    process.wait()  # Wait for the process to finish

    # Cleanup tasks
    stdout, stderr = process.communicate()
    if stderr:
        print("Server STDERR:", stderr.decode())
    if stdout:
        print("Server STDOUT:", stdout.decode())


@pytest.mark.asyncio
async def test_background_working(start_fastapi_server):
    # Assuming httpx_client is another fixture that provides an HTTP client
    start_time = time.time()
    async with httpx.AsyncClient(base_url="http://0.0.0.0:8001") as client:
        response = await client.get("/start-task/")
    # print time
    print(time.time(), "ANSWER HERE")
    assert response.status_code == 200
    end_time = time.time()
    assert end_time - start_time <= 1.0  # it should be answered immediately


# https://fastapi.tiangolo.com/advanced/async-tests/#example
# https://github.com/fastapi/fastapi/issues/1273#issuecomment-648170128
@pytest.mark.asyncio
async def test_async_not_working():
    # It does nto work with the AsyncClient
    start_time = time.time()
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/start-task/")
    # print time
    print(time.time(), "ANSWER HERE")
    assert response.status_code == 200
    end_time = time.time()
    assert (
        end_time - start_time >= 5.0
    )  # it should be answered immediately but takes 5 seconds


def test_sync_not_working(test_client: TestClient):
    start_time = time.time()
    response = test_client.get("/start-task/")
    # print time
    print(time.time(), "ANSWER HERE")
    assert response.status_code == 200
    end_time = time.time()

    assert (
        end_time - start_time >= 5.0
    )  # it should be answered immediately but takes 5 seconds
