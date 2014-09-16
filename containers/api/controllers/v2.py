
import pecan
import wsme
from wsme import types as wtypes
import wsmeext.pecan as weme_pecan
from pecan import rest, response

class ContainerController(rest.RestController):
 
    @weme_pecan.wsexpose(Container)
    def get(self):
	#TODO: Returns all the containers
        return {
            "200": "It returns all the containers."
        }
 
    @wsme_pecan.wsexpose(Container, body=Container, status_code=201)
    def post(self):
        # TODO: Create a new container
        response.status = 201
        return
 
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        # TODO: DELETE the containers
        response.status = 200
        return
