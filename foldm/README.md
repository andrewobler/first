FoldM
=====

This is the repo for the FoldM project. FoldM aims to be a simple utility that
makes it easy to convert a document containing many individual pages into a
format that can be quickly printed, assembled, and organized. It stemmed from
applications in music (e.g., converting a PDF of many separate pages into the
standard double-sided, double-wide format that can be stapled into an orchestral
part), but can be used for any situation in which such a format is desired.

FoldM is written in Python 2.7. Its only external dependency is the
[PyPDF2](https://pythonhosted.org/PyPDF2/) library for PDF manipulation.

Directories
===========

- **src** contains the main source file, _pageops.py_, as well as the "buffer"
  PDF
  file that it references.

- **pdf** will probably be thrown out at some point, but for now it contains
  some public-domain reference PDFs as well as their converted forms.

- **test** will eventually be home to some unit tests and other similar
  procedural code, but for now it does not have anything valuable.
