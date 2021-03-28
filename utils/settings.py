# headers
import os

GLOBAL_HEADERS = {
    "Content-Type": "application/json;charset=utf-8",
    "Cookie": "",
    "Origin": "https://chat.zmlearn.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:86.0) Gecko/20100101 Firefox/86.0",
}

# HTML template with latex(impl by KaTeX) and <table> simple css
# (... %s ... %s ... ) % ( <title>, <相关的p标签> )
HTML_TEMPLATE_WITH_KATEX = """
<html>
<head>
    <style>
        table,table tr th, table tr td { border:1px solid #000000; }
        table {text-align: center; border-collapse: collapse;}
    </style>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.0/dist/katex.min.css" integrity="sha384-t5CR+zwDAROtph0PXGte6ia8heboACF9R5l/DiY+WZ3P2lxNgvJkQk5n7GPvLMYw" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.13.0/dist/katex.min.js" integrity="sha384-FaFLTlohFghEIZkw6VGwmf9ISTubWAVYW8tG8+w2LAIftJEULZABrF9PPFv+tVkH" crossorigin="anonymous"></script>
    <meta charset="UTF-8"> 
    <title>%s</title>
</head>
<body>%s
<script type="text/javascript">
    let nodes = document.querySelectorAll("zmlatex");
    for (let node of nodes) {
        katex.render(node.textContent, node, {
            throwOnError: false
        });
    }
</script>
</body>
</html>
"""


# 试卷接口 url template
GET_QUESTION_DETAIL_BY_ID_URL_TEMPLATE = "https://chat.zmlearn.com/gateway/zhangmen-client-qb/api/teacherExamPaper/findResourceDetailById?access_token=%s"

# 课件ls接口
# ( ... %s ... %d ...) % (access_token, parent_id: int)
GET_DOC_DIR_LIST_BY_PARENT_ID_TEMPLATE = "https://chat.zmlearn.com/gateway/zmc-courseware-teacher/teachDocTeacher/selectDocs?access_token=%s&desc=true&templateStyle=2&parentId=%d"

# 课件描述接口
# ( ... %s ... %d ...) % (access_token, doc_id: int)
GET_TEACHER_DOC_DESC_TEMPLATE = "https://chat.zmlearn.com/gateway/zmc-courseware-teacher/teachDocTeacher/getTeacherDocs?access_token=%s&docIds=%d&appid=10716"

# 原生数据保存位置
RAW_DATA_SAVE_DIR = "./raw-data/"

# 原生zml-json数据保存位置（zml课件）
if not os.path.exists(RAW_DATA_SAVE_DIR):
    os.mkdir(RAW_DATA_SAVE_DIR)
RAW_DATA_ZML_JSON_SAVE_DIR = RAW_DATA_SAVE_DIR + "zml/"

# 原生数据(试卷类)保存名字prefix
RAW_QUESTION_DATA_SAVE_PREFIX = "raw-data-que-"

# 原生数据(课件类)保存名字prefix
RAW_DOC_DATA_SAVE_PREFIX = "raw-data-doc-"

# 处理后的html文件存储路径
OUTPUT_HTML_SAVE_DIR = "./output_html/"

# 处理后的html文件名前缀
OUTPUT_HTML_PREFIX = ""

# 处理后的pdf文件存储路径
OUTPUT_PDF_SAVE_DIR = "./output_pdf/"

# 处理后的pdf文件名前缀
OUTPUT_PDF_PREFIX = ""

# 仅试题的区分名
NO_ANS_PREFIX = "no-ans"

# 仅答案的区分名
ONLY_ANS_PREFIX = "ans"

