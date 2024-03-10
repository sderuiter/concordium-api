# ruff: noqa: F403, F405, E402, E501, E722, F401

import datetime as dt
from datetime import timedelta
import gc
import logging
import uuid
from functools import lru_cache
import resource
import requests
import urllib3
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_restful.tasks import repeat_every
from rich import print
from sharingiscaring.mongodb import MongoDB, MongoMotor
from prometheus_fastapi_instrumentator import Instrumentator

# from app.__chain import *
from app.state.state import *

urllib3.disable_warnings()

from fastapi import Cookie, Depends
from fastapi.concurrency import run_in_threadpool
from sharingiscaring.GRPCClient import GRPCClient

from app.console import console
from app.ENV import *
from app.routers import transaction_v1
from app.routers import account_v1

from sharingiscaring.tooter import Tooter, TooterType, TooterChannel


module_logger = logging.getLogger("ce.main")
logger = logging.getLogger("ce")
logger.setLevel(logging.DEBUG)
import asyncio

# import nest_asyncio
# nest_asyncio.apply()
# import copy
import logging

import sentry_sdk

sentry_environment = "production"

if HOSTNAME_PORT == "http://127.0.0.1:8000":
    sentry_environment = "local"

if HOSTNAME_PORT == "https://dev-api.concordium-explorer.nl":
    sentry_environment = "dev"

if HOSTNAME_PORT == "https://api.concordium-explorer.nl":
    sentry_environment = "production"

# sentry_sdk.init(
#     dsn="https://f4713c02eb5646ed84b2642b0fa1501e@o4503924901347328.ingest.sentry.io/4503924903313408",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production,
#     traces_sample_rate=1.0,
#     environment=sentry_environment,
# )


grpcclient = GRPCClient()
tooter = Tooter(ENVIRONMENT, BRANCH, NOTIFIER_API_TOKEN, API_TOKEN, FASTMAIL_TOKEN)
# fmt:off
mongodb = MongoDB({"MONGODB_PASSWORD": MONGODB_PASSWORD}, tooter)
motormongo = MongoMotor({"MONGODB_PASSWORD": MONGODB_PASSWORD}, tooter)
# fmt:on


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    app.grpcclient = grpcclient
    app.tooter = tooter
    app.mongodb = mongodb
    app.motormongo = motormongo
    yield
    # Any cleanup should happen here
    pass


app = FastAPI(lifespan=lifespan, separate_input_output_schemas=False)
instrumentator = Instrumentator().instrument(app)

# app.include_router(transaction_v1.router)
app.include_router(transaction_v1.router, prefix="/v1")
app.include_router(account_v1.router, prefix="/v1")
