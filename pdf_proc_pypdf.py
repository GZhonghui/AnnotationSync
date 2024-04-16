# there is a bug of pypdf
# do NOT use pdf_proc_pypdf for now

'''
import pypdf, pickle, os, tqdm, message
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import FreeText
from pypdf.annotations import Highlight
from pypdf.generic import ArrayObject, FloatObject

# save annotations to local file
def save_annotations(filepath:str, filename:str):
    filepath = os.path.expanduser(filepath)
    file_fullpath = os.path.join(filepath, filename)
    if not os.path.isfile(file_fullpath) or not file_fullpath.endswith(".pdf"):
        return
    
    reader = PdfReader(file_fullpath)

    data = dict()
    for page in reader.pages:
        pagelist = []
        if "/Annots" not in page:
            continue
        for annot in page["/Annots"]:
            obj = annot.get_object()
            subtype = obj["/Subtype"]
            annotation = {"subtype": subtype, "rect": obj["/Rect"]}

            if subtype == "/FreeText":
                annotation["da"] = obj["/DA"]
                annotation["contents"] = obj["/Contents"]
            elif subtype == "/Highlight":
                annotation["quadpoints"] = obj["/QuadPoints"]

            pagelist.append(annotation)
        data[page.page_number] = pagelist

    with open(file_fullpath[:-3]+"pkl", "wb") as file:        
        pickle.dump(data, file)

# load annotations from local file
# make sure the target pdf file is writable
# make sure you have downloaded the annotations file
def load_annotations(filepath:str, filename:str):
    filepath = os.path.expanduser(filepath)

    # make sure pdf file exist
    file_fullpath = os.path.join(filepath, filename)
    if not os.path.isfile(file_fullpath) or not file_fullpath.endswith(".pdf"):
        return
    
    # make sure data file exist
    datafile_fullpath = file_fullpath[:-3]+"pkl"
    if not os.path.isfile(datafile_fullpath):
        return
    
    data = dict()
    with open(datafile_fullpath, "rb") as file:
        data = pickle.load(file)
    
    writer = PdfWriter()
    writer.append(file_fullpath)

    def make_annotation(source_data):
        annotation = None
        if source_data["subtype"] == "/FreeText":
            font, fontsize, Tf, level, g = source_data["da"].split(" ")
            annotation = FreeText(
                text=source_data["contents"],
                rect=source_data["rect"],
                font=font[2:],
                bold=True,
                italic=True,
                font_size=fontsize+"pt",
                font_color="000000",
                border_color="000000",
                background_color="ffffff",
            )
        elif source_data["subtype"] == "/Highlight":
            annotation = Highlight(
                rect=source_data["rect"],
                quad_points=ArrayObject([FloatObject(p) for p in source_data["quadpoints"]]),
            )
        return annotation

    for page_number, pagelist in tqdm.tqdm(data.items(), desc="loading annotations"):
        for source_annotation in pagelist:
            annotation = make_annotation(source_annotation)
            if annotation:
                writer.add_annotation(page_number=page_number, annotation=annotation)

    # Write the annotated file to disk
    # with open("annotated-pdf.pdf", "wb") as fp:
    #    writer.write(fp)
'''

if __name__=='__main__':
    pass