# Python Flask Application utilizing Azure Metrics

* This application contains code from the following tutorial, make sure to visit the link: [Using Flask in Visual Studio Code](https://code.visualstudio.com/docs/python/tutorial-flask). Intermediate steps are not included.
* It also contains the Dockerfile and uwsgi.ini files necessary to build a container with a production server. The resulting image works both locally and when deployed to Azure App Service. See [Deploy Python using Docker containers](https://code.visualstudio.com/docs/python/tutorial-deploy-containers).

## Navigation

The `startup.py` file, for its part, is specifically for deploying to Azure App Service on Linux without containers. Because the app code is in its own *module* in the `hello_app` folder (which has an `__init__.py`), trying to start the Gunicorn server within App Service on Linux produces an "Attempted relative import in non-package" error. The `startup.py` file, therefore, is just a shim to import the app object from the `hello_app` module, which then allows you to use startup:app in the Gunicorn command line (see `startup.txt`).

## Resources

- Log Analytics vs App Insights vs App Monitor
  - https://github.com/MicrosoftDocs/azure-docs/issues/27590

- Azure Monitor
  - https://docs.microsoft.com/en-us/azure/azure-monitor/visualizations
  - https://docs.microsoft.com/en-us/azure/azure-monitor/platform/metrics-custom-overview
  - https://github.com/Microsoft/ApplicationInsights-JS/blob/master/API-reference.md
  - https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python
  - https://github.com/census-instrumentation/opencensus-python/tree/master/contrib/opencensus-ext-flask
  - https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python-request
  - https://docs.microsoft.com/en-us/azure/azure-monitor/platform/metrics-store-custom-rest-api
  - https://www.youtube.com/watch?v=iTRILNstmFI

- Deploy Docker onto Azure
  - https://docs.microsoft.com/en-us/azure/python/tutorial-deploy-containers-01