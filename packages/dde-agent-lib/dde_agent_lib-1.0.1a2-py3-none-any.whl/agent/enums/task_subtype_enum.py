from enum import Enum


class TaskSubtypeEnum(Enum):
    DEFAULT = "0"
    NORMAL_QS = "101"
    DOCUMENT_PARSING = "102"
    DATA_VISILIZATION = "103"
    PICTURE_2_TABLE = "104"
    INFORMATION_RETRIEVAL_SCHOLAR_SEARCH = "105"
    WEB_SEARCH = "106"
    CODE_AGENT = "107"

    PLUGINS_CHOSEN = "508"
    DOCUMENT_STRUCTURE_SUBMIT_TASK = "501"
    #DOCUMENT_STRUCTURE_MATHPIX = "502"
    #DOCUMENT_STRUCTURE_ZJ = "504"
    PARSER_PDF_GEN_META = "526"
    PARSER_PDF_DOC_ANALYZE = "527"
    PARSER_PDF_DOC_REORGANIZE = "528"
    PARSER_PDF_MARKDOWN_GENERATE = "529"
    EXTRACT_PDF_PLUGIN_ROUTER = "516"
    DOCUMENT_EXTRACTION = "507"
    EXTRACT_PDF_TIANRANG_SHORT = "521"
    EXTRACT_PDF_MYDATA = "523"
    EXTRACT_PDF_MYDATA_DOWNLOAD = "524"
    EXTRACT_PDF_MYDATA_RETRIEVER = "525"
    SCHOLAR_SEARCH_TOPIC_EXTRACTION = "530"
    SCHOLAR_SEARCH_SEMANTIC_SEARCH = "531"
    WEB_SEARCH_GOOGLE_SEARCH = "532"
    WEB_SEARCH_LLM_SUMMARY = "533"
    #PARAMETERS_EXTRACTION = "509"
    DOCUMENT_STRUCTURE_MATHPIX = "501"
    DOCUMENT_STRUCTURE_ZJ = "502"
    DOCUMENT_EXTRACTION_LLM = "503"
    DOCUMENT_EXTRACTION_ZJ = "504"
    PLUGIN_CHOSEN = "505"
    PARAMETERS_EXTRACTION = "506"
    EXTRACT_PDF_PLUGIN_DOWNLOAD ="517"
    EXTRACT_PDF_PLUGIN_PIPLINE = "518"
    EXTRACT_PDF_TIANRANG = "519"
    EXTRACT_PDF_TIANRANG_DOWNLOAD = "520"

