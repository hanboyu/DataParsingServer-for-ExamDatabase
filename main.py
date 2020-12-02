
from DPServer import *
import service.bulk_upload_paser

import os


app = DPServer()


@app.route("status")
def status():
    return bytearray("online", "utf-8")


@app.route("bulk_upload")
def parse_upload(b_file: bytes):
    # save file
    file_name = "temp/" + service.bulk_upload_paser.random_name() + ".doc"
    temp_file = open(file_name, "wb")
    temp_file.write(b_file)
    temp_file.close()
    # parse file
    parse_result = service.bulk_upload_paser.parse_file(file_name)
    # finished parsing, remove file
    os.remove(file_name)
    return bytearray(parse_result, "utf-8")


if __name__ == "__main__":

    HOST_ADDR = "localhost"
    HOST_PORT = 6969

    app.run(HOST_ADDR, HOST_PORT)
