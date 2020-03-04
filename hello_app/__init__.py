from flask import Flask  # Import the Flask class

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler

import uuid
import os

app = Flask(__name__)    # Create an instance of the class for our use

telemetry_key = "<telemetry_key>"

middleware = FlaskMiddleware(
    app,
    # storage path and the following code prevents an error caused by threading
    exporter=AzureExporter(instrumentation_key=telemetry_key,
        storage_path=os.path.join(
            os.path.expanduser('~'),
            '.opencensus',
            '.azure',
            str(uuid.uuid4()),
            '.console',
        )
    ),
    sampler=ProbabilitySampler(rate=1.0)
)