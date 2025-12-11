Module triangulator.api
=======================
Flask API for the Triangulator microservice.

Functions
---------

`triangulate_endpoint()`
:   Handle triangulation requests from clients.
    
    Expects a JSON payload with a 'pointSetId' field.
    Fetches the corresponding PointSet from the PointSetManager,
    computes the triangulation, and returns the result as binary data.
    
    Returns:
        HTTP 200 with binary Triangles data on success.
        HTTP 400 for invalid input.
        HTTP 404 if PointSet not found.
        HTTP 502 if PointSetManager is unreachable or returns an error.
        HTTP 500 for data decoding or triangulation errors.