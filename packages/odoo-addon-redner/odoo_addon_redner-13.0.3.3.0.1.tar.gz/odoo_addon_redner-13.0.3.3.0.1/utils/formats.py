DEFAULT_MIMETYPE = "application/octet-stream"

FORMAT_WORD97 = "doc"
FORMAT_WORD2003 = "wordml"
FORMAT_PDF = "pdf"
FORMAT_DOCBOOK = "docbook"
FORMAT_HTML = "html"
FORMAT_ODT = "odt"
FORMAT_ODS = "ods"
FORMAT_XLS = "xls"
FORMAT_DOCX = "docx"


class UnkownFormatException(Exception):
    pass


class Format:
    """A format representation that contains:
        a name we use in our applications
        an ODF name (like: 'MS Word 2003 XML') which is the name you must
        use as a filter to call a renderserver or a LibreOffice server
        a mimetype that corresponds to the mimetype of the produced file
        if you ask LibreOffice to convert to the corresponding format
        and a simple flag that indicates if the format is Native or if it is
        produced by calling a LibreOffice filter to convert the native
        document to an "external format"
    """

    def __init__(self, name, odfname, mimetype=DEFAULT_MIMETYPE, native=False):
        self.name = name
        self.odfname = odfname
        self.mimetype = mimetype
        self.native = native


class Formats:
    def __init__(self):

        self._formats = {
            FORMAT_WORD97: Format(
                FORMAT_WORD97, "MS Word 97", "application/msword"
            ),
            FORMAT_WORD2003: Format(
                FORMAT_WORD2003,
                "MS Word 2003 XML",
                "application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.document",
            ),
            FORMAT_PDF: Format(
                FORMAT_PDF, "writer_pdf_Export", "application/pdf"
            ),
            FORMAT_DOCBOOK: Format(
                FORMAT_DOCBOOK, "DocBook File", "application/xml"
            ),
            FORMAT_HTML: Format(FORMAT_HTML, "HTML", "text/html"),
            FORMAT_ODT: Format(
                FORMAT_ODT,
                "writer8",
                "application/vnd.oasis.opendocument.text",
                native=True,
            ),
            FORMAT_ODS: Format(
                FORMAT_ODS,
                "calc8",
                "application/vnd.oasis.opendocument.spreadsheet",
                native=True,
            ),
            FORMAT_XLS: Format(
                FORMAT_XLS, "MS Excel 97", "application/msexcel"
            ),
            FORMAT_DOCX: Format(
                FORMAT_DOCX,
                "Office Open XML Text",
                "application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.document",
            ),
        }

    def get_format(self, name):
        """an accessor that will return a redner.formats.Format instance that
        can be used to know the LibreOffice filter name, the mimetype etc.
        :param name: the name of the LibreOffice filter (ie: format) you want
        to obtain
        :type name: string
        :returns: a redner.formats.Format instance.
        :raises: redner.formats.UnkownFormatException if the provided name does
        not correspond to a known format named
        """
        f = self._formats.get(name)

        if not f:
            raise UnkownFormatException("Format {} is unkown".format(name))

        return f

    def get_known_format_names(self, nativeonly=False):
        """return the a list of names that can be used as format names in
        redner.template.
        :param nativeonly: a boolean flag. If set to True will only return
        native formats.
        :type nativeonly: bool
        :return: list of chars
        :returntype: list
        :raises: nothing
        """
        if nativeonly:
            return [f for f in self._formats if self.get_format(f).native]
        return list(self._formats)
