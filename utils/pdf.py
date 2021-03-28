import pdfkit


def html2pdf(html_file, pdf_file):
    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
    # 生成pdf文件，to_file为文件路径
    pdfkit.from_file(html_file, pdf_file, configuration=config)
    pass
