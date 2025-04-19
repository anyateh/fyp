from datetime import datetime
from os import path
from typing import Callable, Optional

from ..manage_antes import gen_json_update

__base_frontend_dir = "interface"
__index_html_file = path.join(__base_frontend_dir, "index.html")
__js_queue_js_file = path.join(__base_frontend_dir, "js", "queue.js")
__css_scrollbar_css_file = path.join(__base_frontend_dir, "css", "scrollbar.css")

__fonts_overpass_css_file = path.join(__base_frontend_dir, "fonts", "overpass.css")
__fonts_overpass_qFdB35WCmI96Ajtm81GgY93qxycJ_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdB35WCmI96Ajtm81GgY93qxycJ.woff2")
__fonts_overpass_qFdB35WCmI96Ajtm81GgY9bqxycJ_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdB35WCmI96Ajtm81GgY9bqxycJ.woff2")
__fonts_overpass_qFdB35WCmI96Ajtm81GgY9fqxycJ_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdB35WCmI96Ajtm81GgY9fqxycJ.woff2")
__fonts_overpass_qFdB35WCmI96Ajtm81GgY9nqxw_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdB35WCmI96Ajtm81GgY9nqxw.woff2")
__fonts_overpass_qFdB35WCmI96Ajtm81GgY9TqxycJ_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdB35WCmI96Ajtm81GgY9TqxycJ.woff2")
__fonts_overpass_qFdH35WCmI96Ajtm81GhU9vyww_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdH35WCmI96Ajtm81GhU9vyww.woff2")
__fonts_overpass_qFdH35WCmI96Ajtm81GlU9s_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdH35WCmI96Ajtm81GlU9s.woff2")
__fonts_overpass_qFdH35WCmI96Ajtm81GoU9vyww_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdH35WCmI96Ajtm81GoU9vyww.woff2")
__fonts_overpass_qFdH35WCmI96Ajtm81GqU9vyww_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdH35WCmI96Ajtm81GqU9vyww.woff2")
__fonts_overpass_qFdH35WCmI96Ajtm81GrU9vyww_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "overpass", "qFdH35WCmI96Ajtm81GrU9vyww.woff2")

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

def queue_js_supplier() -> bytes:
	with open(__js_queue_js_file, 'rb') as f:
		d = f.read()

	return d

def queue_js_supplier_time() -> int:
	return int(path.getmtime(__js_queue_js_file))

db_table['/js/queue.js'] = DB_Resource("/js/queue.js", "text/javascript", Supplier(queue_js_supplier, queue_js_supplier_time))

def scrollbar_css_supplier() -> bytes:
	with open(__css_scrollbar_css_file, 'rb') as f:
		d = f.read()

	return d

def scrollbar_css_supplier_time() -> int:
	return int(path.getmtime(__css_scrollbar_css_file))

db_table['/css/scrollbar.css'] = DB_Resource("/css/scrollbar.css", "text/css", Supplier(scrollbar_css_supplier, scrollbar_css_supplier_time))

def fonts_overpass_css_supplier() -> bytes:
	with open(__fonts_overpass_css_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_css_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_css_file))

db_table['/fonts/overpass.css'] = DB_Resource("/fonts/overpass.css", "text/css", Supplier(fonts_overpass_css_supplier, fonts_overpass_css_supplier_time))

def fonts_overpass_qFdB35WCmI96Ajtm81GgY93qxycJ_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdB35WCmI96Ajtm81GgY93qxycJ_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdB35WCmI96Ajtm81GgY93qxycJ_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdB35WCmI96Ajtm81GgY93qxycJ_woff2_file))

db_table['/fonts/overpass/qFdB35WCmI96Ajtm81GgY93qxycJ.woff2'] = DB_Resource("/fonts/overpass/qFdB35WCmI96Ajtm81GgY93qxycJ.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdB35WCmI96Ajtm81GgY93qxycJ_woff2_supplier, fonts_overpass_qFdB35WCmI96Ajtm81GgY93qxycJ_woff2_supplier_time))

def fonts_overpass_qFdB35WCmI96Ajtm81GgY9bqxycJ_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdB35WCmI96Ajtm81GgY9bqxycJ_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdB35WCmI96Ajtm81GgY9bqxycJ_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdB35WCmI96Ajtm81GgY9bqxycJ_woff2_file))

db_table['/fonts/overpass/qFdB35WCmI96Ajtm81GgY9bqxycJ.woff2'] = DB_Resource("/fonts/overpass/qFdB35WCmI96Ajtm81GgY9bqxycJ.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdB35WCmI96Ajtm81GgY9bqxycJ_woff2_supplier, fonts_overpass_qFdB35WCmI96Ajtm81GgY9bqxycJ_woff2_supplier_time))

def fonts_overpass_qFdB35WCmI96Ajtm81GgY9fqxycJ_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdB35WCmI96Ajtm81GgY9fqxycJ_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdB35WCmI96Ajtm81GgY9fqxycJ_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdB35WCmI96Ajtm81GgY9fqxycJ_woff2_file))

db_table['/fonts/overpass/qFdB35WCmI96Ajtm81GgY9fqxycJ.woff2'] = DB_Resource("/fonts/overpass/qFdB35WCmI96Ajtm81GgY9fqxycJ.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdB35WCmI96Ajtm81GgY9fqxycJ_woff2_supplier, fonts_overpass_qFdB35WCmI96Ajtm81GgY9fqxycJ_woff2_supplier_time))

def fonts_overpass_qFdB35WCmI96Ajtm81GgY9nqxw_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdB35WCmI96Ajtm81GgY9nqxw_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdB35WCmI96Ajtm81GgY9nqxw_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdB35WCmI96Ajtm81GgY9nqxw_woff2_file))

db_table['/fonts/overpass/qFdB35WCmI96Ajtm81GgY9nqxw.woff2'] = DB_Resource("/fonts/overpass/qFdB35WCmI96Ajtm81GgY9nqxw.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdB35WCmI96Ajtm81GgY9nqxw_woff2_supplier, fonts_overpass_qFdB35WCmI96Ajtm81GgY9nqxw_woff2_supplier_time))

def fonts_overpass_qFdB35WCmI96Ajtm81GgY9TqxycJ_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdB35WCmI96Ajtm81GgY9TqxycJ_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdB35WCmI96Ajtm81GgY9TqxycJ_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdB35WCmI96Ajtm81GgY9TqxycJ_woff2_file))

db_table['/fonts/overpass/qFdB35WCmI96Ajtm81GgY9TqxycJ.woff2'] = DB_Resource("/fonts/overpass/qFdB35WCmI96Ajtm81GgY9TqxycJ.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdB35WCmI96Ajtm81GgY9TqxycJ_woff2_supplier, fonts_overpass_qFdB35WCmI96Ajtm81GgY9TqxycJ_woff2_supplier_time))

def fonts_overpass_qFdH35WCmI96Ajtm81GhU9vyww_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdH35WCmI96Ajtm81GhU9vyww_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdH35WCmI96Ajtm81GhU9vyww_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdH35WCmI96Ajtm81GhU9vyww_woff2_file))

db_table['/fonts/overpass/qFdH35WCmI96Ajtm81GhU9vyww.woff2'] = DB_Resource("/fonts/overpass/qFdH35WCmI96Ajtm81GhU9vyww.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdH35WCmI96Ajtm81GhU9vyww_woff2_supplier, fonts_overpass_qFdH35WCmI96Ajtm81GhU9vyww_woff2_supplier_time))

def fonts_overpass_qFdH35WCmI96Ajtm81GlU9s_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdH35WCmI96Ajtm81GlU9s_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdH35WCmI96Ajtm81GlU9s_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdH35WCmI96Ajtm81GlU9s_woff2_file))

db_table['/fonts/overpass/qFdH35WCmI96Ajtm81GlU9s.woff2'] = DB_Resource("/fonts/overpass/qFdH35WCmI96Ajtm81GlU9s.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdH35WCmI96Ajtm81GlU9s_woff2_supplier, fonts_overpass_qFdH35WCmI96Ajtm81GlU9s_woff2_supplier_time))

def fonts_overpass_qFdH35WCmI96Ajtm81GoU9vyww_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdH35WCmI96Ajtm81GoU9vyww_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdH35WCmI96Ajtm81GoU9vyww_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdH35WCmI96Ajtm81GoU9vyww_woff2_file))

db_table['/fonts/overpass/qFdH35WCmI96Ajtm81GoU9vyww.woff2'] = DB_Resource("/fonts/overpass/qFdH35WCmI96Ajtm81GoU9vyww.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdH35WCmI96Ajtm81GoU9vyww_woff2_supplier, fonts_overpass_qFdH35WCmI96Ajtm81GoU9vyww_woff2_supplier_time))

def fonts_overpass_qFdH35WCmI96Ajtm81GqU9vyww_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdH35WCmI96Ajtm81GqU9vyww_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdH35WCmI96Ajtm81GqU9vyww_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdH35WCmI96Ajtm81GqU9vyww_woff2_file))

db_table['/fonts/overpass/qFdH35WCmI96Ajtm81GqU9vyww.woff2'] = DB_Resource("/fonts/overpass/qFdH35WCmI96Ajtm81GqU9vyww.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdH35WCmI96Ajtm81GqU9vyww_woff2_supplier, fonts_overpass_qFdH35WCmI96Ajtm81GqU9vyww_woff2_supplier_time))

def fonts_overpass_qFdH35WCmI96Ajtm81GrU9vyww_woff2_supplier() -> bytes:
	with open(__fonts_overpass_qFdH35WCmI96Ajtm81GrU9vyww_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_overpass_qFdH35WCmI96Ajtm81GrU9vyww_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_overpass_qFdH35WCmI96Ajtm81GrU9vyww_woff2_file))

db_table['/fonts/overpass/qFdH35WCmI96Ajtm81GrU9vyww.woff2'] = DB_Resource("/fonts/overpass/qFdH35WCmI96Ajtm81GrU9vyww.woff2", "application/font-woff2", Supplier(fonts_overpass_qFdH35WCmI96Ajtm81GrU9vyww_woff2_supplier, fonts_overpass_qFdH35WCmI96Ajtm81GrU9vyww_woff2_supplier_time))
