import time
import random
import logging
import os

from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration
from datetime import datetime
from flask import Flask, render_template

import psutil

from . import app

instrumentation_key = "<instrumentation_key>"

# Metrics
stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder
CARROTS_MEASURE = measure_module.MeasureInt("carrots",
                                            "number of carrots",
                                            "carrots")
CARROTS_VIEW = view_module.View("carrots_view",
                                "number of carrots",
                                [],
                                CARROTS_MEASURE,
                                aggregation_module.CountAggregation())

# Enable metrics
# Set the interval in seconds in which you want to send metrics
exporter = metrics_exporter.new_metrics_exporter(instrumentation_key=instrumentation_key)
view_manager.register_exporter(exporter)
view_manager.register_view(CARROTS_VIEW)

mmap = stats_recorder.new_measurement_map()
tmap = tag_map_module.TagMap()

_exporter = metrics_exporter.new_metrics_exporter(instrumentation_key=instrumentation_key)

# Logs
config_integration.trace_integrations(['logging'])
logger = logging.getLogger(__name__)
handler = AzureLogHandler(instrumentation_key=instrumentation_key)
handler.setFormatter(logging.Formatter('%(traceId)s %(spanId)s %(message)s'))
logger.addHandler(handler)

#Trace
tracer = Tracer(
    exporter=AzureExporter(instrumentation_key=instrumentation_key),
    sampler=ProbabilitySampler(1.0),
)


@app.route("/")
def home():
    with tracer.span(name='firstpage'):
        print('Hello from first page!')
        logger.warning('Before the span')
        with tracer.span(name="firstpagenestedspan") as span:
            try:
                time.sleep(0.1)
                rand_num = random.randint(1,4)
                if rand_num == 2:
                    raise Exception('spam', 'eggs')
                logger.warning('In the span')
            except:
                logger.warning('Error in the span')
        logger.warning('After the span')
    return render_template("home.html")


@app.route("/about/")
def about():
    with tracer.span(name='secondpage'):
        print('Hello from second page!')
        mmap.measure_int_put(CARROTS_MEASURE, 1000)
        mmap.record(tmap)
    return render_template("about.html")


@app.route("/contact/")
def contact():
    with tracer.span(name='thirdpage'):
        print(psutil.virtual_memory())
        time.sleep(3)
        print('Hello from the third page!')
    return render_template("contact.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
