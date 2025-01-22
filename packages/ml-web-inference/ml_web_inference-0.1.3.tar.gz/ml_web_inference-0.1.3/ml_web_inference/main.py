import asyncio
from typing import Callable, Awaitable
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import Response
import uvicorn
from datetime import datetime
import pynvml
from torch.nn import Module


def expose(
    api_name: str,
    inference_function: Callable[[Request], Awaitable[Response]],
    port: int = 10000,
    init_function: Callable[[], None] = None,
    hangup_function: Callable[[], None] = None,
    hangup_timeout_sec: int = 1800,
    hangup_interval_sec: int = 60,
    init_on_expose: bool = True,
):
    """
    Expose an inference API using FastAPI with initialization and hangup management.

    Sets up a FastAPI application with a specified API endpoint for handling inference requests.
    Manages the initialization of resources and gracefully shuts down (hangup) after a period of inactivity.

    Args:
        api_name (str): The name of the API endpoint.
        inference_function (Callable[[Request], Awaitable[Response]]):
            The asynchronous function that processes inference requests.
        port (int, optional): The port number on which the FastAPI app will run. Defaults to 10000.
        init_function (Callable[[], None], optional):
            A function to initialize resources before handling the first request. Defaults to None.
        hangup_function (Callable[[], None], optional):
            A function to clean up resources after a period of inactivity. Defaults to None.
        hangup_timeout_sec (int, optional):
            The duration in seconds of inactivity after which the hangup_function is triggered. Defaults to 1800 seconds (30 minutes).
        hangup_interval_sec (int, optional):
            The interval in seconds at which the system checks for inactivity. Defaults to 60 seconds.

    Returns:
        None
    """
    host = "localhost"
    app = FastAPI()
    initialized = False
    last_inference_time = datetime.now()

    def init():
        nonlocal initialized
        if init_function is not None:
            init_function()
        initialized = True

    if init_on_expose:
        init()

    async def check_hangup():
        nonlocal initialized
        while True:
            await asyncio.sleep(hangup_interval_sec)
            if initialized:
                time_since_last_call = datetime.now() - last_inference_time
                if time_since_last_call.total_seconds() > hangup_timeout_sec:
                    if hangup_function is not None:
                        hangup_function()
                    initialized = False

    @app.post(f"/{api_name}")
    async def inference(request: Request, background_tasks: BackgroundTasks):
        nonlocal initialized, last_inference_time
        if not initialized:
            init()
        last_inference_time = datetime.now()
        background_tasks.add_task(check_hangup)

        return await inference_function(request)

    uvicorn.run(app, host=host, port=port, log_level="info")


pynvml.nvmlInit()


def get_proper_device(gpu_threshold_mb: float) -> int:
    """
    Select the most suitable GPU device based on available memory and utilization.

    Utilizes NVIDIA's NVML library to identify GPU devices that meet the specified memory threshold.
    Among eligible devices, selects the one with the lowest GPU utilization. If no devices meet
    the memory threshold, selects the device with the highest available memory.

    Args:
        gpu_threshold_mb (float): The minimum required available GPU memory in megabytes.

    Returns:
        int: The index of the selected GPU device.
    """
    deviceCount = pynvml.nvmlDeviceGetCount()
    devices_meet_threshold = []
    devices_all = []
    for i in range(deviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        memInfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        available_memory = (memInfo.total - memInfo.used) / 1024 / 1024
        devices_all.append((i, available_memory))
        if available_memory > gpu_threshold_mb:
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            gpu_util = utilization.gpu
            devices_meet_threshold.append((i, gpu_util))
    pynvml.nvmlShutdown()
    if devices_meet_threshold:
        device = min(devices_meet_threshold, key=lambda x: x[1])
        return device[0]
    else:
        device = max(devices_all, key=lambda x: x[1])
        return device[0]


def get_model_size_mb(model: Module) -> float:
    """
    Calculate the size of a machine learning model in megabytes.

    Computes the total memory footprint of the model by summing the sizes of all its parameters
    and buffers.

    Args:
        model: The machine learning model (e.g., a PyTorch `nn.Module`).

    Returns:
        float: The size of the model in megabytes (MB).
    """
    param_size = sum(
        param.nelement() * param.element_size() for param in model.parameters()
    )
    buffer_size = sum(
        buffer.nelement() * buffer.element_size() for buffer in model.buffers()
    )
    size_all_mb = (param_size + buffer_size) / (1024**2)
    return size_all_mb
