
import pecan
from pecan import rest, response

class ContainerController(rest.RestController):
 
    @pecan.expose("json")
    def get(self):
	#TODO: Returns all the containers
        return {
            "200": "It returns all the containers."
        }
 
    @pecan.expose()
    def post(self):
        # TODO: Create a new container
        response.status = 201
        return
 
    @pecan.expose()
    def put(self):
        # TODO: Edit the containers values (return 200 or 204)
        response.status = 204
        return
 
    @pecan.expose()
    def delete(self):
        # TODO: DELETE the containers
        response.status = 200
        return
