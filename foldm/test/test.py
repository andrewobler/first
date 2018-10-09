import PyPDF2 as pdf2
import pageops

def mergeTwoTest():
    sps = pdf2.PdfFileReader("sps.pdf")
    pg4 = sps.getPage(3)
    pg5 = sps.getPage(4)
    merged = pageops.mergeTwo(pg4, pg5)
    writer = pdf2.PdfFileWriter
    writer.addPage(merged)
    writer.write(open("mergeTest.pdf", "wb"))

def operateStd(inFile, outFile):
    pageops.convertFilename(inFile, True).write(open(outFile, 'wb'))
