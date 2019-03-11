import socket
from flask import Flask, request
from healthcheck import HealthCheck, EnvironmentDump

application = Flask(__name__)

# wrap the flask app and give a heathcheck url
health = HealthCheck(application, "/healthcheck")
envdump = EnvironmentDump(application, "/environment")


@application.route("/")
def hello():
    return "Hello from {} to {}".format(socket.gethostname(), request.remote_addr)

# not sure if this is needed or if /healthcheck is magic
def check_health():
    return True, "ok"

health.add_check(check_health)

if __name__ == "__main__":
    application.run()
