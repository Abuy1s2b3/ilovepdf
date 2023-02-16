# fileName : plugins/dm/callBack/file_process/combinePages.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/combinePages.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def combinePages(input_file: str, cDIR: str) -> tuple[ bool, str ]:
    try:
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            with fitz.open() as oUTPUT:        # empty output PDF
                width, height = fitz.paper_size("a4")
                r = fitz.Rect(0, 0, width, height)
                # define the 4 rectangles per page
                r1 = r / 2 # top left rect
                r2 = r1 + (r1.width, 0, r1.width, 0) # top right
                r3 = r1 + (0, r1.height, 0, r1.height) # bottom left
                r4 = fitz.Rect(r1.br, r.br) # bottom right
                r_tab = [r1, r2, r3, r4]
                # now copy input pages to output
                for pages in iNPUT:
                    if pages.number % 4 == 0: # create new output page
                        page = oUTPUT.new_page(-1, width = width, height = height)
                    # insert input page into the correct rectangle
                    page.show_pdf_page(r_tab[pages.number % 4], iNPUT, pages.number)
                    # by all means, save new file using garbage collection and compression
            oUTPUT.save(output_path, garbage = 3, deflate = True)
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
