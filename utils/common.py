import copy
import html


from parser import ZmTagParser
from utils.settings import *


def get_html_file_name(resource_id: int, resource_name: str, _type: str):
    if not os.path.exists(OUTPUT_HTML_SAVE_DIR):
        os.mkdir(OUTPUT_HTML_SAVE_DIR)
    prefix = OUTPUT_HTML_PREFIX + _can_insert_short_line(OUTPUT_HTML_PREFIX) + _type + _can_insert_short_line(_type)
    domain = str(resource_id) + "-" + str(resource_name) + ".html"
    return OUTPUT_HTML_SAVE_DIR + prefix + domain


def get_pdf_file_name(resource_id: int, resource_name: str,  _type: str):
    resource_name = resource_name.replace(".html", "")
    if not os.path.exists(OUTPUT_PDF_SAVE_DIR):
        os.mkdir(OUTPUT_PDF_SAVE_DIR)
    prefix = OUTPUT_PDF_PREFIX + _can_insert_short_line(OUTPUT_PDF_PREFIX) + _type + _can_insert_short_line(_type)
    domain = str(resource_id) + "-" + str(resource_name) + ".pdf"
    return OUTPUT_PDF_SAVE_DIR + prefix + domain


def _can_insert_short_line(test_name):
    return "-" if len(test_name) != 0 else ""
    pass


def fix_html(_html: str):
    """
    处理zmsubline等标签
    :param _html: html
    :return: 处理后的html
    """
    hp = ZmTagParser()
    hp.feed(_html)
    hp.close()
    return hp.to_string()
    pass


def filter_p_text(s: str):
    process = copy.copy(s)
    if s.startswith("<p>"):
        process = process[3:]

    if s.endswith("</p>"):
        process = process[:-4]
    return process
    pass


def add_p_text(s: str, attr: dict = None):
    """
    add p tag with attr
    :param s: content text
    :param attr: attr dict e.g. {"a": 1, "b": "string"}
    :return:
    """
    if attr is None:
        return "<p>" + s + "</p>"
    else:
        attr_line = ""
        for k, v in attr.items():
            attr_line += (" " + k + '="' + html.escape(v) + '"')
            pass
        return "<p" + attr_line + ">" + s + "</p>"
    pass


def add_img_tag(url: str, attr: dict = None):
    if attr is None:
        return '<img alt="zm-tool" src="%s"/>' % url
    else:
        attr_line = ""
        for k, v in attr.items():
            attr_line += " "
            attr_line += (k + '="' + html.escape(v) + '"')
            pass
        return '<img alt="zm-tool" src="%s"' % url + attr_line + "/>"
    pass


def chg_to_short_line(hump: str):
    """
    类驼峰转短线连接
    简化问题，除了大写字母均认为是小写字母（符号数字等）
    思路：
    1. 查找大写的位置，相邻的位置合并，被合并的大写位置变小写 O(n)
    2. 剩下的大写索引位置插入'-'，并大写变小写 O(n_{big})
    :param hump: 类驼峰名
    :return: 短线连接名
    """
    if hump is None:
        raise TypeError("""'NoneType' object is not convertible.""")
        pass
    # 扫描大写位置
    process_hump = list(hump)
    # big idx stack
    big_idx = []
    i = 0

    # 是否相邻的标志位
    between = False
    # 如果相邻用来暂存上一个大写的索引
    between_val = None

    for c in process_hump:
        if 65 <= ord(c) <= 90:
            if len(big_idx) != 0:
                # 判断相邻而决定待比较的<上一个>应该为 <栈顶> 还是 <大写相邻的特殊情况>
                if between:
                    pre = between_val
                    pass
                else:
                    # 没相邻则为big_idx栈顶
                    pre = big_idx[-1]
                    pass

                if i - pre == 1:
                    # 出现相邻则合并 原位置调整为小写
                    process_hump[i] = c.lower()
                    # 标记相邻
                    between = True
                    between_val = i
                    pass
                else:
                    # 不相邻的情况重置标志位
                    between = False
                    between_val = None
                    big_idx.append(i)
                pass
            else:
                # 栈空时不存在相邻大写的判断，直接入栈
                between = False
                between_val = None
                big_idx.append(i)
            pass
        else:
            if between and len(big_idx) != 0:
                # 如果已经处理到小写而当前标志位是True时，说明目前最后一个大写也被转换小写了，反转这一操作。
                process_hump[i - 1] = process_hump[i - 1].upper()
                big_idx.append(i - 1)
                between = False
                between_val = None
                pass
        i += 1

    # 最后big_idx处理，插入短线
    #
    # ext_pos 为首位不插入短线而占位
    ext_pos = 0
    for idx in range(len(big_idx)):
        idx_val = big_idx[idx]
        process_pos = int(idx_val + idx - ext_pos)
        process_hump[process_pos] = process_hump[process_pos].lower()

        if process_pos != 0:
            # FIXME: 这里list的数组结构影响insert效率问题
            process_hump.insert(process_pos, '-')
        else:
            ext_pos += 1
        pass

    return "".join(process_hump)
    pass
