
import pecan
from pecan import rest

class VersionController(rest.RestController):
    @pecan.expose('json')
    def get(self):
	return {"version":"2.0.0"}
