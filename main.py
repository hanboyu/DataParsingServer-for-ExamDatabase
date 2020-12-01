
from DPServer import *
import service.bulk_upload_paser


app = DPServer()


@app.route("status")
def status():
    return bytearray("online", "utf-8")


@app.route("bulk_upload")
def parse_upload(b_file: bytes):
    file_name = "temp/" + service.bulk_upload_paser.generate_temp_filename() + ".doc"
    temp_file = open(file_name, "wb")
    temp_file.write(b_file)
    temp_file.close()
    return bytearray("success", "utf-8")


if __name__ == "__main__":

    HOST_ADDR = "localhost"
    HOST_PORT = 6969

    app.run(HOST_ADDR, HOST_PORT)
