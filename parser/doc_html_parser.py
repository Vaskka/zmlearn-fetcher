from utils.common import *


class DocParser:
    @classmethod
    def parse_page(cls, page_obj: dict):
        """
        处理page类型的obj
        1. 如果存在content，直接用
        2. 不存在content，遍历elements，组装
        3. 组装后整体附加containStyle
        :param page_obj: page obj
        :return: html str
        """

        style_attr = cls._process_style(page_obj["containerStyle"])

        result = ""
        if "content" in page_obj:
            result = add_p_text(page_obj["content"], style_attr)
        else:
            elements = page_obj["elements"]
            for element in elements:
                sub_style_attr = cls._process_style(element["style"])
                if element["type"] == "text":
                    content = filter_p_text(element["content"])
                    result += add_p_text(content, sub_style_attr)
                    pass
                elif element["type"] == "image":
                    result += add_img_tag(element["src"], sub_style_attr)
                    pass
                pass
            result = add_p_text(result, style_attr)
        return result
        pass

    @staticmethod
    def _process_style(contain_style_raw_dict: dict):
        """
        raw style to {"style": "..."} dict
        :param contain_style_raw_dict:
        :return:
        """
        style_line = ""
        for k, v in contain_style_raw_dict.items():
            if v == "":
                continue
            if k in ("top", "bottom", "left", "right", "width", "height"):
                v = str(v) + "%"

            style_line += chg_to_short_line(k)
            if k == "backgroundImage":
                style_line += (": url(" + str(v) + ");")
            else:
                style_line += (": " + str(v) + ";")
            pass
        return {"style": style_line}
        pass
    pass
