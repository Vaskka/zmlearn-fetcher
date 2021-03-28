from core.api import ZmTool


def main():
    zm_tool = ZmTool("xxx", "yyy")
    r = [1191595, ]
    for i in r:
        zm_tool.process_question(i, 1)
        zm_tool.process_question(i, 0)
    pass


if __name__ == '__main__':
    main()
