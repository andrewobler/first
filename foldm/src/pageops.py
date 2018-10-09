"""
This file contains all the meaningful source code for now.
"""

import PyPDF2 as pdf2

### TODO:
### - Handle base cases (pages = 1, 2, 3)
### - Give user option to add a custom title page
### - Deploy using Flask/Django/Ajax

### NOTE: A "default user space unit" is 1/72 of an inch. ###

### Global variables
## Portrait width, in default user space units
PW = 612
## Portrait height, in default user space units
PH = 792
## Slight horizontal shift when converting -- for testing only!
# SHIFT = 0

class PageCountError(Exception):
    """
    Basic exception class to handle attempts to call functions on PDFs with
    improper page counts.
    """
    pass

def writerToReader(writer):
    """
    Converts a PdfFileWriter into an equivalent PdfFileReader by temporarily
    writing to a throwaway buffer file.
    """
    writer.write(open("buffer.pdf", 'wb'))
    reader = pdf2.PdfFileReader("buffer.pdf")
    # Overwrite buffer with a blank double-portrait page
    overwriter = pdf2.PdfFileWriter()
    overwriter.addBlankPage(PW * 2, PH)
    overwriter.write(open("buffer.pdf", 'wb'))
    return reader

def mergeTwo(p1, p2):
    """
    Given two portrait-sized pages, returns a PageObject consisting of a double-
    length page with the contents of both pages.
    """
    # Create a double-width template blank
    blank = pdf2.pdf.PageObject.createBlankPage(None, PW * 2, PH)
    # Scale pages down to portrait size
    p1.scaleTo(PW, PH)
    p2.scaleTo(PW, PH)
    # Merge scaled pages atop of template
    blank.mergePage(p1)
    blank.mergeTranslatedPage(p2, PW, 0)
    return blank

def splitMerge(reader):
    """
    Given a PdfFileReader with an even number of pages, merges every pair of
    pages from the middle outwards. Returns a PdfFileWriter. Raises an exception
    if an odd number of pages is passed.
    """
    pages = reader.getNumPages()
    if pages % 2 != 0:
        raise PageCountError("PDF has an odd number of pages!")
    writer = pdf2.PdfFileWriter()
    for i in range(pages / 2, pages):
        writer.addPage(mergeTwo(reader.getPage(pages - i - 1), reader.getPage(i)))
    return writer

def splitMerge2(reader):
    """
    Given a PdfFileReader with a page count that is a multiple of four, returns
    a PdfFileWriter with every pair of pages merged in alternating order from
    the middle outwards. Intended for double-sided printing. Raises an
    exception if the page count is not a multiple of four.
    """
    pages = reader.getNumPages()
    if pages % 4 != 0:
        raise PageCountError("PDF page count is not a multiple of four!")
    writer = pdf2.PdfFileWriter()
    for i in range(pages / 2, pages):
        if i % 2 == 0:
            # Put this page on the right
            writer.addPage(mergeTwo(reader.getPage(pages - i - 1), reader.getPage(i)))
        else:
            # Put this page on the left
            writer.addPage(mergeTwo(reader.getPage(i), reader.getPage(pages - i - 1)))
    return writer

def convert(reader, doubleSided=True):
    """
    Processes the given PdfFileReader as desired. Returns a functional
    PdfFileWriter.

    Parameter doubleSided determines whether to merge pages in an alternating
    fashion.
    """
    writer = pdf2.PdfFileWriter()
    pages = reader.getNumPages()
    if doubleSided:
        # First append blank pages until a multiple of four is reached
        writer.appendPagesFromReader(reader)
        while pages % 4 != 0:
            writer.addBlankPage(PW, PH)
            pages += 1
        newReader = writerToReader(writer)
        writer = splitMerge2(newReader)
    else:
        # Append a blank page if number of pages is odd
        writer.appendPagesFromReader(reader)
        if pages % 2 != 0:
            writer.addBlankPage(PW, PH)
        newReader = writerToReader(writer)
        writer = splitMerge(newReader)
    return writer

def convertFilename(filename, doubleSided=True):
    """
    Simply calls convert on the given filename, a string.
    """
    reader = pdf2.PdfFileReader(filename)
    return convert(reader, doubleSided)
