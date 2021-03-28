from html.parser import HTMLParser


class ZmTagParser(HTMLParser):
    """
    zm特有标签，目前能够处理：zmsubline
    """
    def error(self, message):
        print("err:" + message)
        pass

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.is_zm = False

    def handle_starttag(self, tag, attrs):
        if tag == "zmsubline":
            self.is_zm = True

        self.data.append(self.from_attr_get_full_tag_text_no_ending(tag, attrs) + ">")

    def handle_endtag(self, tag):
        if tag == "zmsubline":
            self.is_zm = False
        self.data.append('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        self.data.append(self.from_attr_get_full_tag_text_no_ending(tag, attrs) + "/>")

    def handle_data(self, data):
        if self.is_zm:
            self.data.append("____")
            pass
        else:
            self.data.append(data)

    def handle_comment(self, data):
        self.data.append('<!--' + data + '-->')

    def handle_entityref(self, name):
        self.data.append('&%s;' % name)

    def handle_charref(self, name):
        self.data.append('&#%s;' % name)

    @staticmethod
    def from_attr_get_full_tag_text_no_ending(tag, attrs):
        output = "<" + tag
        for k, v in attrs:
            output += " "
            output += k + '="'
            output += v + '"'
            pass
        return output

    def to_string(self):
        """
        HTMLParser.close() 后使用 HTMLParser.to_string() 拿到处理结果
        :return:
        """
        return "<!DOCTYPE html>" + "".join(self.data)
        pass
