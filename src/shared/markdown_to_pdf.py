import pdfkit
import markdown2  # 替换 markdown 为 markdown2

from shared.logger import default_logger as logger


def convert_markdown_to_html(markdown_text):
    """
    将 Markdown 文本转换为带有可选 CSS 样式的 HTML
    :param markdown_text: Markdown 格式的文本
    :return: 转换后的 HTML
    """
    # 使用 markdown2 库将 Markdown 转换为 HTML
    html_body = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables", "toc"])
    # 构建完整的 HTML 文档
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Markdown to PDF</title>
         <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1, h2, h3, h4, h5, h6 {{
                page-break-after: avoid;
                color: #333;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                overflow-x: auto;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            table p {{
                margin: 0 0 0.5em;
            }}
           thead th {{
                padding: 12px 15px;
                text-align: left;
                white-space: nowrap;
                min-width: 80px;
                border: 1px solid #ccc;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 3px;
            }}

        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    return html


def markdown_to_pdf(markdown_text, output_filename):
    try:
        # 使用 markdown2 先将 Markdown 转换为 HTML
        html = convert_markdown_to_html(markdown_text)
        # 配置 pdfkit
        options = {
            'encoding': "UTF-8",
        }
        # 转换为 PDF
        pdfkit.from_string(html, output_filename, options=options)
        return True
    except Exception as e:
        logger.error(f"转换过程中发生错误: {e}")
        return False
