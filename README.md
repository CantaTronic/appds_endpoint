# GRADLC data retrieval API

 This repository contains API for KCDC  MDDB for GRADLC (APPDS) project.

## Modules list:
```
 api.py
 check_auth.py
 kcdc.py
 mddb.py
 mongo2sql.py
 read_config.py
 test.py
 txtwriter.py
 ```

## Functionality:

* Every request checks authentication, currently implemented: user ```test_user``` with password ```test_pass```
* Endpoints:
    * ```/api/request/``` — accepts a request, assigns uuid to the request, writes the request to the database, initiates query to KCDC MongoDB (should become async in future), returns the request uuid; only the time cut is currently implemented
    * ```/api/my_requests/``` — returns a list of requests for the user, with the following data for each request: uuid, request status, url of a corresponding file
    * ```/api/request_status/<string:request_uuid>/``` — returns the info for a particular request
    * ```/api/data/<string:filename>``` — allows to download a file written by the request

## Future plans:

* Async query to KCDC MongoDB (RabbitMQ+Celery)
* Connection with kcdc data processing chain
* Dockering
* [Unification with APPDS]
* Updating possible requests

