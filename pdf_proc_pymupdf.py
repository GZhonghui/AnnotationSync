import fitz  # 导入PyMuPDF库

def remove_annotations(pdf_path, output_path):
    # 打开PDF文件
    doc = fitz.open(pdf_path)

    # 遍历每一页
    for page in doc:
        # 通过列表收集所有注释
        annotations = [annot for annot in page.annots()] if page.annots() else []
        
        # 遍历收集到的所有注释并删除
        for annot in annotations:
            page.delete_annot(annot)

    # 保存修改后的PDF到新文件
    doc.save(output_path)
    doc.close()

def main():
    # 使用示例
    pdf_path = 'input.pdf'  # 输入的PDF文件路径
    output_path = 'output.pdf'  # 输出无注释的PDF文件路径
    remove_annotations(pdf_path, output_path)

main()