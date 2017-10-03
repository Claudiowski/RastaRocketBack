from werkzeug.datastructures import FileStorage
from ..api import api


upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

need_parser = api.parser()
need_parser.add_argument('page', required=False, type=int, help='Pagination page')
need_parser.add_argument('customer', required=False, type=str, help='Customer name')
need_parser.add_argument('title', required=False, type=str, help='Need title')
need_parser.add_argument('status', required=False, type=str, help='Need status')
need_parser.add_argument('size', required=False, type=int, help='Number of needs')

customer_autocomplete_parser = api.parser()
customer_autocomplete_parser.add_argument('name', required=True, help='Customer name')