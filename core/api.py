import json

import requests

from exceptions.exception import TypeNotSupportError
from login.login import AuthCenter
from parser.doc_html_parser import DocParser
from utils.common import *
from utils.constant import DOC_TYPE_MAPPING


def save_raw_json_response(json_text: str, saving_dir: str, _id: int, _name: str, _type: str = ""):
    """
    保存原生json 接口数据
    :param saving_dir:  保存的dir path
    :param json_text: json content
    :param _id: id
    :param _name: name
    :param _type: type 可用于区分接口类型
    :return: None
    """
    if not os.path.exists(saving_dir):
        os.mkdir(saving_dir)
        pass

    path = saving_dir + _type + "-" + str(_id) + "-" + str(_name) + ".json"
    with open(path, "w") as f:
        f.write(json_text)
    pass


class ZmTool:

    def __init__(self, user_mobile, password):
        self.mobile = user_mobile
        self.password = password

        self.auth_center = AuthCenter(user_mobile, password)

        pass

    def process_question(self, resource_id: int, _type: int = 1):
        """
        整理试卷/答案
        :param resource_id: 试卷 id
        :param _type: _type 0/1
        :return: None
        """
        json_obj = json.loads(self.fetch_question_detail_by_id(resource_id))
        if _type == 0:
            # only ans
            QuestionDetailProcessor.deal_only_ans(json_obj)
        elif _type == 1:
            # only question
            QuestionDetailProcessor.deal_no_ans(json_obj)
        else:
            err = "not support type: %d" % _type
            print(err)
            raise TypeNotSupportError()
        pass

    def process_doc(self, doc_id: int):
        """
        整理课件
        :param doc_id: 课件id
        :return: None
        """
        desc, doc_obj = self.fetch_zml_json_object(doc_id)
        doc_name = desc["name"]
        doc_content_list = doc_obj["data"]
        body_html = ""
        for doc_item in doc_content_list:
            body_html += DocDetailProcessor.convert_save_doc_item_dfs(doc_item)
            body_html += "<hr/>"
            pass
        DocDetailProcessor.save_doc_html(doc_id, doc_name, body_html)
        pass

    def list_doc_dir(self, parent_id: int = 0):
        """
        ls 个人资料库 -> 课件库
        :param parent_id: 默认根目录(parent_id == 0)
        :return:
        """
        fetch_url = GET_DOC_DIR_LIST_BY_PARENT_ID_TEMPLATE % (self.auth_center.get_access_token(), parent_id)
        resp = requests.post(url=fetch_url,
                             headers=GLOBAL_HEADERS)
        raw_list = json.loads(resp.text)["data"]
        return map(lambda item: {
            "id": item["id"],
            "name": item["name"],
            "doc_type_raw_id": item["docType"],
            "doc_type": DOC_TYPE_MAPPING[item["docType"]],
            "path": item["path"],
            "name_path": item["namePath"],
            "parent_id": item["parentId"],
            "level": item["level"]
        }, raw_list)

    pass

    def fetch_question_detail_by_id(self, resource_id: int):
        """
        get resource detail raw json response.
        :param resource_id:
        :return: json text
        """
        resp = requests.post(
            url=GET_QUESTION_DETAIL_BY_ID_URL_TEMPLATE % self.auth_center.get_access_token(),
            headers=GLOBAL_HEADERS,
            json={
                "id": resource_id
            })

        return resp.text

    def fetch_zml_json_object(self, doc_id: int):
        """
        dict
        :param doc_id: doc id
        :return: get docContent parsed by json lib and desc (doc_desc, docContentObj)
        """
        resp = requests.post(url=GET_TEACHER_DOC_DESC_TEMPLATE % (self.auth_center.get_access_token(), doc_id))
        desc = json.loads(resp.text)["data"][0]
        print("fetching doc:", desc)

        zml_url = desc["docContent"]
        zml_resp = requests.get(url=zml_url, headers=GLOBAL_HEADERS)

        # saving json file
        save_raw_json_response(zml_resp.text,
                               RAW_DATA_ZML_JSON_SAVE_DIR,
                               desc["docId"], desc["name"],
                               RAW_DOC_DATA_SAVE_PREFIX)

        return desc, json.loads(zml_resp.text)
        pass


class QuestionDetailProcessor:

    @classmethod
    def deal_only_ans(cls, json_obj):
        """
        处理仅保存答案
        write result in file
        :param json_obj: json dict
        :return: None
        """
        resource_name = json_obj["data"]["name"]
        resource_id = json_obj["data"]["id"]
        # save json file
        save_raw_json_response(json.dumps(json_obj), RAW_DATA_SAVE_DIR, int(resource_id), str(resource_name),
                               RAW_QUESTION_DATA_SAVE_PREFIX + ONLY_ANS_PREFIX)

        all_que_list = json_obj["data"]["examPaperDetail"]["examPaperContentOutputDTOList"]
        output = ""
        for que_list_parent in all_que_list:
            que_list = que_list_parent["examPaperContentQuestionOutputDTOList"]
            for que_detail in que_list:
                in_id = 1
                out_id = str(que_detail["serialNumber"])
                children = que_detail["questionOutputDTO"]["children"]

                if children is None:
                    output += "%s 答案：" % out_id
                    ans_list = que_detail["questionOutputDTO"]["answerList"]
                    ans_text = ",".join(ans_list)
                    output += ans_text
                    output += "\n"
                    pass
                else:
                    for child in children:
                        output += "%s.%d 答案：" % (out_id, in_id)
                        ans_text = ",".join(child["answerList"])

                        output += ans_text
                        output += "\n"

                        in_id += 1
                        pass

                output += "\n"
                pass

        # add big title and save in html
        cls.add_big_title_and_write_file(output, resource_id, resource_name, ONLY_ANS_PREFIX, "_答案")
        pass

    @classmethod
    def deal_no_ans(cls, json_obj):
        """
        处理仅保存试题
        write result in file
        :param json_obj: json dict
        :return: None
        """
        resource_name = json_obj["data"]["name"]
        resource_id = json_obj["data"]["id"]
        # save json file
        save_raw_json_response(json.dumps(json_obj), RAW_DATA_SAVE_DIR, int(resource_id), str(resource_name),
                               RAW_QUESTION_DATA_SAVE_PREFIX + NO_ANS_PREFIX)

        main_que_list = json_obj["data"]["examPaperDetail"]["examPaperContentOutputDTOList"]
        output = ""
        for main_que in main_que_list:
            output += "<h2>" + str(main_que["serialNumber"])
            output += ". "
            output += main_que["name"] + "</h2>"
            output += "\n"
            sec_ser_num = 1
            for sub_que in main_que["examPaperContentQuestionOutputDTOList"]:
                if main_que["name"] == "选择题":
                    # 选择题
                    before_title = sub_que["questionOutputDTO"]["title"].replace("<p>", "", 1)
                    title = str(main_que["serialNumber"]) + "." + str(sec_ser_num) + "&nbsp;" + before_title
                    title = "<p>" + title
                    title = "<h4>" + title + "</h4>"

                    children = sub_que["questionOutputDTO"]["children"]
                    output += title + "\n"

                    if children is None or len(children) == 0:
                        output += cls._get_option_list(sub_que["questionOutputDTO"])
                    else:
                        sub_child_ser_num = 1
                        for child in children:
                            output += cls._get_option_list(child, sub_child_ser_num)
                            sub_child_ser_num += 1
                            pass
                    pass
                else:
                    # 解答题
                    que = sub_que["questionOutputDTO"]
                    before_title = que["title"].replace("<p>", "", 1)
                    sub_ser_num = str(main_que["serialNumber"]) + "." + str(sec_ser_num)
                    title = sub_ser_num + "&nbsp;" + before_title
                    title = "<p>" + title
                    title = "<h4>" + title + "</h4>"

                    sub_output = ""
                    inx = 1
                    if que["children"] is not None:
                        for child in que["children"]:
                            sub_title = str(child["title"])
                            sub_title = sub_title.replace("<p>", "", 1)
                            sub_title = sub_ser_num + "." + str(inx) + "&nbsp;" + sub_title
                            sub_title = "<p>" + sub_title
                            sub_title = sub_title + "<br/>"
                            sub_output += sub_title
                            inx += 1
                            pass

                    output += (title + "\n" + sub_output + "<br/>")
                    pass
                sec_ser_num += 1
                pass

            pass

        # add big title and save in html
        cls.add_big_title_and_write_file(output, resource_id, resource_name, NO_ANS_PREFIX, "_试题")
        pass

    @classmethod
    def _get_option_list(cls, child, ser_num: int = None):
        title = child["title"]

        if ser_num is not None:
            title = ("(%d). &nbsp;" % ser_num + filter_p_text(title))
            title = add_p_text(title)
            pass

        output = ""
        option_list = [filter_p_text(i) for i in child["optionList"]]
        option_text = ""
        opt_ser = 0
        for opt in option_list:
            opt = chr(65 + opt_ser) + ". " + opt
            opt = add_p_text(opt)
            opt_ser += 1
            option_text += opt
            pass

        output += (title + "\n" + option_text + "\n")
        return output

    @classmethod
    def add_big_title_and_write_file(cls, output: str, resource_id: int, resource_name: str, _type, ext_title=""):
        """
        顶部加上大标题并写入html
        :param output: output
        :param resource_id: resource id
        :param resource_name: resource name
        :param ext_title: ext_title
        :param _type:
        :return: None
        """
        output = "<hr/>" + output
        output = "<h1>" + resource_name + ext_title + "</h1>" + output

        html_file_name = get_html_file_name(resource_id, resource_name + ext_title, _type)

        # html
        html_content = fix_html(HTML_TEMPLATE_WITH_KATEX % (resource_name + ext_title, output))
        with open(html_file_name, "w") as f:
            f.write(html_content)

        pass

    pass


class DocDetailProcessor:
    @classmethod
    def convert_save_doc_item_dfs(cls, doc_item_obj: dict):
        if doc_item_obj is None:
            return ""

        if doc_item_obj["type"] == "page":
            page_html = DocParser.parse_page(doc_item_obj)
            return page_html
            pass

        if doc_item_obj["type"] == "slide" or doc_item_obj["type"] == "dir":
            res = ""
            for item in doc_item_obj["children"]:
                res += cls.convert_save_doc_item_dfs(item)
                pass
            return res
        return ""
        pass

    @classmethod
    def save_doc_html(cls, doc_id: int, title: str, body_html: str):
        final_html = HTML_TEMPLATE_WITH_KATEX % (title, body_html)
        final_html = "<hr/>" + final_html
        final_html = "<h1>" + title + "_课件" + "</h1>" + final_html
        html_file_name = get_html_file_name(doc_id, title, "_课件")

        with open(html_file_name, "w") as f:
            f.write(final_html)
        pass

    pass