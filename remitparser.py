from lxml import etree
import re
from collections import ChainMap


class RemitParser(object):

    STATIC_FIELDS = {
        'REPORT_DATE': None,
        'REPORT_RUN_DATE': None,
        'SENDER_NAME': '/ns:REMITTable2/ns:reportingEntityID/ns:ace/text()',
        'SENT_TO_ACER_UK_TIME': None,
        'DOCUMENT_TYPE': None,
        'FILENAME': None,
        'RECORD': None
    }

    CONTRACT_FIELDS = {
        'UTI': 'ns:contractId/text()',
        'LINKED_ORDER': None,
        'LINKED_TRANSACTION_ID': None,
        'TRADE_DATE': 'ns:contractDate/text()',
        'TRANSACTION_TIMESTAMP_UTC': None,
        'ACTION': 'ns:actionType/text()',
        'ERR_STATUS': None,
        'OMP_NAME': None,
        'MP_NAME': None,
        'MP_ACER_CODE': 'ns:idOfMarketParticipant/ns:ace/text()',
        'OTHER_MP_CODE': 'ns:otherMarketParticipant/ns:ace/text()',
        'CONTRACT_TYPE': 'ns:contractType/text()',
        'CONTRACT_NAME': None,
        'COMMODITY': 'ns:energyCommodity/text()',
        'BS': 'ns:buySellIndicator/text()',
        'DELIVERY_POINT': 'ns:deliveryPointOrZone/text()',
        'DEL_START': 'ns:deliveryStartDate/text()',
        'DEL_END': 'ns:deliveryEndDate/text()',
        'QUANTITY': 'ns:totalNotionalContractQuantity/ns:value/text()',
        'UNIT': 'ns:totalNotionalContractQuantity/ns:unit/text()',
        'PRICE': 'ns:priceOrPriceFormula/ns:price/ns:value/text()',
        'CURR': 'ns:priceOrPriceFormula/ns:price/ns:currency/text()',
        'TOTAL_QUANTITY': 'ns:totalNotionalContractQuantity/ns:value/text()',
        'TOTAL_UNIT': 'ns:totalNotionalContractQuantity/ns:unit/text()',
        'NOTIONAL_AMOUNT': 'ns:estimatedNotionalAmount/ns:value/text()',
        'NOT_CURR': 'ns:estimatedNotionalAmount/ns:currency/text()'
    }

    TRADELIST = '/*/ns:TradeList/*'

    def __init__(self, xml):
        #from io import StringIO
        self._parser = etree.XMLParser(ns_clean=True)
        self._tree = etree.parse(xml, parser=self._parser)
        self._xmlns = {'ns': re.findall(
            '\{(.*)\}', self.tree.getroot().tag)[0]}

    def _get_doc_header(self):
        return {k: (self.get_at(self.tree.xpath(v, namespaces=self._xmlns), 0, '') if v else '') for (k, v) in self.STATIC_FIELDS.items()}

    def _get_doc_body(self):
        return [{k: (self.get_at(trd.xpath(v, namespaces=self._xmlns), 0, '') if v else '')
                 for (k, v) in self.CONTRACT_FIELDS.items()} for trd in self.tree.xpath(self.TRADELIST, namespaces=self._xmlns)]

    def get_document(self):
        hdr = self._get_doc_header()
        bdy = self._get_doc_body()
        return [ChainMap(*[hdr, dct]) for dct in bdy]

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
