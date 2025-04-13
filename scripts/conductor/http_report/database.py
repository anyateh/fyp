from datetime import datetime
from os import path
from typing import Callable, Optional

from ..manage_antes import gen_json_update

__base_frontend_dir = "interface"
__index_html_file = path.join(__base_frontend_dir, "index.html")

class Supplier:
	content_fx:Optional[Callable[[], bytes]]
	datemodified_fx:Optional[Callable[[], int]]

	def __init__(self, content_fx:Optional[Callable[[], bytes]], datemodified_fx:Optional[Callable[[], int]]) -> None:
		self.content_fx = content_fx
		self.datemodified_fx = datemodified_fx

	def content(self) -> bytes:
		if self.content_fx:
			return self.content_fx();

		return b''

	def modified(self) -> int:
		if self.datemodified_fx:
			return self.datemodified_fx()
		
		return int(datetime.now().timestamp())

class DB_Resource:
	cached_content:Optional[bytes] = None
	cached_datetime:Optional[int] = None
	should_cache:bool = True

	path:str

	type:str

	supplier:Supplier

	def __init__(self, path:str, type:str, supplier:Supplier, should_cache:bool = True) -> None:
		self.path = path
		self.type = type
		self.supplier = supplier
		self.should_cache = should_cache

	def cache_content(self) -> None:
		self.cached_content = self.supplier.content()
		self.cached_datetime = int(datetime.now().timestamp())

	def obtain_content(self) -> bytes:
		if not self.should_cache:
			return self.supplier.content()

		if not self.cached_content or self.supplier.modified() > self.cached_datetime:
			self.cache_content()

		return self.cached_content

db_table:dict[str, DB_Resource] = {}

def get_data_entry(resource_path:str) -> tuple[str, Optional[bytes]]:
	return (db_table[resource_path].type, db_table[resource_path].obtain_content()) \
		if resource_path in db_table else ('text/plain', None)

def index_html_supplier() -> bytes:
	with open(__index_html_file, 'rb') as f:
		d = f.read()

	return d

def index_html_supplier_time() -> int:
	return int(path.getmtime(__index_html_file))

db_table['/']           = DB_Resource("/", "text/html", Supplier(index_html_supplier, index_html_supplier_time))
db_table['/index.html'] = DB_Resource("/index.html", "text/html", Supplier(index_html_supplier, index_html_supplier_time))

def upd_json_supplier() -> bytes:
	return gen_json_update().encode(encoding = 'utf-8')

db_table['/upd.json'] = DB_Resource("/upd.json", "application/json", Supplier(upd_json_supplier, None), False)
