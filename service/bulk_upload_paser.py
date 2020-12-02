
from datetime import date
from datetime import datetime
import random
import json


def random_name():
    today = date.today()
    now = datetime.now()
    l = random.randint(1, 26) + 96
    return today.strftime("%m%d%Y") + now.strftime("%H%M%S") + "_" + chr(l)


def parse_file(filename: str) -> str:
    """
    This function parse world document which contains multiple
    questions into Json format.
    @param filename: path to the file that is needed to be parse
    @return: a list of dictionary in Json format (string)
    """
    # this is for testing
    ############################################
    res = []
    test_question = dict()
    test_question["tags"] = ["test_tag"]
    test_question["permission"] = 0
    test_question["question_body"] = "Is this a test question?"
    test_question["question_images_addr"] = ""
    test_question["choices"] = ["choice A", "choice B",  "choice C", "choice D", "choice E"]
    test_question["choice_images_addr"] = []
    test_question["answer"] = "choice F"
    res.append(test_question)
    res_json = json.dumps(res)
    print(res_json)
    #################################################
    return res_json

