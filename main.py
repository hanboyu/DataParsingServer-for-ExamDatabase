
from DPServer import *
app = DPServer()


@app.route("status")
def status():
    return "online"


if __name__ == "__main__":

    HOST_ADDR = "localhost"
    HOST_PORT = 6969

    app.run(HOST_ADDR, HOST_PORT)