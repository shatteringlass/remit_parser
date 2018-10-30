xmlns = {'tbl1': 'http://www.acer.europa.eu/REMIT/REMITTable1_V2.xsd',
         'tbl2': 'http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd',
         'tbl3': None,
         'tbl4': None,
         'lng': None,
         'stor': None
         }

STATIC_FIELDS = {
    'REPORT_DATE': None,
    'REPORT_RUN_DATE': None,
    'SENDER_NAME': '/tbl:REMITTable2/tbl:reportingEntityID/tbl:ace/text()',
    'SENT_TO_ACER_UK_TIME': None,
    'DOCUMENT_TYPE': None,
    'FILENAME': None,
    'RECORD': None
}

CONTRACT_FIELDS = {
    'UTI': 'tbl:contractId/text()',
    'LINKED_ORDER': None,
    'LINKED_TRANSACTION_ID': None,
    'TRADE_DATE': 'tbl:contractDate/text()',
    'TRANSACTION_TIMESTAMP_UTC': None,
    'ACTION': 'tbl:actionType/text()',
    'ERR_STATUS': None,
    'OMP_NAME': None,
    'MP_NAME': None,
    'MP_ACER_CODE': 'tbl:idOfMarketParticipant/tbl:ace/text()',
    'OTHER_MP_CODE': 'tbl:otherMarketParticipant/tbl:ace/text()',
    'CONTRACT_TYPE': 'tbl:contractType/text()',
    'CONTRACT_NAME': None,
    'COMMODITY': 'tbl:energyCommodity/text()',
    'BS': 'tbl:buySellIndicator/text()',
    'DELIVERY_POINT': 'tbl:deliveryPointOrZone/text()',
    'DEL_START': 'tbl:deliveryStartDate/text()',
    'DEL_END': 'tbl:deliveryEndDate/text()',
    'QUANTITY': 'tbl:totalNotionalContractQuantity/tbl:value/text()',
    'UNIT': 'tbl:totalNotionalContractQuantity/tbl:unit/text()',
    'PRICE': 'tbl:priceOrPriceFormula/tbl:price/tbl:value/text()',
    'CURR': 'tbl:priceOrPriceFormula/tbl:price/tbl:currency/text()',
    'TOTAL_QUANTITY': 'tbl:totalNotionalContractQuantity/tbl:value/text()',
    'TOTAL_UNIT': 'tbl:totalNotionalContractQuantity/tbl:unit/text()',
    'NOTIONAL_AMOUNT': 'tbl:estimatedNotionalAmount/tbl:value/text()',
    'NOT_CURR': 'tbl:estimatedNotionalAmount/tbl:currency/text()'
}

TRADELIST = '/tbl:REMITTable2/tbl:TradeList/*'


class RemitParser(object):

    def __init__(self, xml):
        from lxml import etree
        import re
        #from io import StringIO
        self._parser = etree.XMLParser(ns_clean=True)
        self._tree = etree.parse(xml, parser=self._parser)
        self._xmlns = {'tbl' : re.findall('\{(.*)\}',self.tree.getroot().tag)[0]}

    def _get_doc_header(self):
        return {k: (self.get_at(self.tree.xpath(v, namespaces=self._xmlns), 0, '') if v else '') for (k, v) in STATIC_FIELDS.items()}

    def _get_doc_body(self):
        return [{k: (self.get_at(trd.xpath(v, namespaces=self._xmlns), 0, '') if v else '')
                 for (k, v) in CONTRACT_FIELDS.items()} for trd in self.tree.xpath(TRADELIST, namespaces=self._xmlns)]

    def get_document(self):
        hdr = self._get_doc_header()
        bdy = self._get_doc_body()
        for dct in bdy:
            hdr.update(dct)
        return bdy

    @property
    def tree(self):
        return self._tree

    @staticmethod
    def get_at(lst, idx, default=None):
        return lst[idx] if max(~idx, idx) < len(lst) else default


class RemitTable1Parser(RemitParser):
    pass


class RemitTable2Parser(RemitParser):
    pass
