from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter

from enterpriseSpider.items import SZHomeSpiderItem
import logging


class EnterpriseCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter
        fields_to_export = settings.get('SZ_FIELDS_TO_EXPORT', [])
        if fields_to_export:
            kwargs['fields_to_export'] = fields_to_export
        super(EnterpriseCsvItemExporter, self).__init__(*args, **kwargs)

    def _write_headers_and_set_fields_to_export(self, item):
        self.header_map = {}
        if isinstance(item, SZHomeSpiderItem):
            self.header_map = settings.get('SZ_HEADERS', {})

        if not self.include_headers_line:
            return
            # this is the parent logic taken from parent class
        if not self.fields_to_export:
            if isinstance(item, dict):
                # for dicts try using fields of the first item
                self.fields_to_export = list(item.keys())
            else:
                # use fields declared in Item
                self.fields_to_export = list(item.fields.keys())
        headers = list(self._build_row(self.fields_to_export))

        # here we add our own extra mapping
        # map headers to our value
        headers = [self.header_map.get(header, header) for header in headers]
        self.csv_writer.writerow(headers)
