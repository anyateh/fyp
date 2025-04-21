from datetime import datetime
from os import path
from typing import Callable, Optional

from ..manage_antes import gen_json_update

__base_frontend_dir      = "interface"
__index_html_file        = path.join(__base_frontend_dir, "index.html")
__favicon_ico_file       = path.join(__base_frontend_dir, "favicon.ico")
__js_queue_js_file       = path.join(__base_frontend_dir, "js", "queue.js")
__css_scrollbar_css_file = path.join(__base_frontend_dir, "css", "scrollbar.css")

__icons_favicon_32_png_file  = path.join(__base_frontend_dir, "icons", "favicon_32.png")
__icons_favicon_64_png_file  = path.join(__base_frontend_dir, "icons", "favicon_64.png")
__icons_favicon_72_png_file  = path.join(__base_frontend_dir, "icons", "favicon_72.png")
__icons_favicon_96_png_file  = path.join(__base_frontend_dir, "icons", "favicon_96.png")
__icons_favicon_120_png_file = path.join(__base_frontend_dir, "icons", "favicon_120.png")
__icons_favicon_128_png_file = path.join(__base_frontend_dir, "icons", "favicon_128.png")
__icons_favicon_144_png_file = path.join(__base_frontend_dir, "icons", "favicon_144.png")
__icons_favicon_152_png_file = path.join(__base_frontend_dir, "icons", "favicon_152.png")
__icons_favicon_180_png_file = path.join(__base_frontend_dir, "icons", "favicon_180.png")
__icons_favicon_192_png_file = path.join(__base_frontend_dir, "icons", "favicon_192.png")
__icons_favicon_384_png_file = path.join(__base_frontend_dir, "icons", "favicon_384.png")
__icons_favicon_512_png_file = path.join(__base_frontend_dir, "icons", "favicon_512.png")

__icons_app_icon_72_png_file = path.join(__base_frontend_dir, "icons", "app", "icon_72.png")
__icons_app_icon_96_png_file = path.join(__base_frontend_dir, "icons", "app", "icon_96.png")
__icons_app_icon_120_png_file = path.join(__base_frontend_dir, "icons", "app", "icon_120.png")
__icons_app_icon_144_png_file = path.join(__base_frontend_dir, "icons", "app", "icon_144.png")
__icons_app_icon_152_png_file = path.join(__base_frontend_dir, "icons", "app", "icon_152.png")
__icons_app_icon_180_png_file = path.join(__base_frontend_dir, "icons", "app", "icon_180.png")
__icons_app_icon_192_png_file = path.join(__base_frontend_dir, "icons", "app", "icon_192.png")
__icons_app_icon_384_png_file = path.join(__base_frontend_dir, "icons", "app", "icon_384.png")
__icons_app_icon_512_png_file = path.join(__base_frontend_dir, "icons", "app", "icon_512.png")

__icons_ios_splash_1125x2436_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1125x2436.png") 
__icons_ios_splash_1170x2532_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1170x2532.png") 
__icons_ios_splash_1179x2556_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1179x2556.png") 
__icons_ios_splash_1242x2208_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1242x2208.png") 
__icons_ios_splash_1242x2688_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1242x2688.png") 
__icons_ios_splash_1284x2778_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1284x2778.png") 
__icons_ios_splash_1290x2796_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1290x2796.png") 
__icons_ios_splash_1488x2266_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1488x2266.png") 
__icons_ios_splash_1536x2048_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1536x2048.png") 
__icons_ios_splash_1620x2160_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1620x2160.png") 
__icons_ios_splash_1640x2360_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1640x2360.png") 
__icons_ios_splash_1668x2224_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1668x2224.png") 
__icons_ios_splash_1668x2388_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_1668x2388.png") 
__icons_ios_splash_2048x1536_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_2048x1536.png") 
__icons_ios_splash_2048x2732_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_2048x2732.png") 
__icons_ios_splash_2160x1620_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_2160x1620.png") 
__icons_ios_splash_2224x1668_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_2224x1668.png") 
__icons_ios_splash_2266x1488_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_2266x1488.png") 
__icons_ios_splash_2360x1640_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_2360x1640.png") 
__icons_ios_splash_2388x1668_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_2388x1668.png") 
__icons_ios_splash_2732x2048_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_2732x2048.png") 
__icons_ios_splash_640x1136_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_640x1136.png") 
__icons_ios_splash_750x1334_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_750x1334.png") 
__icons_ios_splash_828x1792_png_file = path.join(__base_frontend_dir, "icons", "ios", "splash_828x1792.png") 

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

__fonts_sharetechmono_css_file = path.join(__base_frontend_dir, "fonts", "sharetechmono.css")
__fonts_sharetechmono_J7aHnp1uDWRBEqV98dVQztYldFcLowEF_woff2_file = \
		path.join(__base_frontend_dir, "fonts", "sharetechmono", "J7aHnp1uDWRBEqV98dVQztYldFcLowEF.woff2")

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

def favicon_ico_supplier() -> bytes:
	with open(__favicon_ico_file, 'rb') as f:
		d = f.read()

	return d

def favicon_ico_supplier_time() -> int:
	return int(path.getmtime(__favicon_ico_file))

db_table['/favicon.ico'] = DB_Resource("/favicon.ico", "image/x-icon", Supplier(favicon_ico_supplier, favicon_ico_supplier_time))

def favicon_32_png_supplier() -> bytes:
	with open(__icons_favicon_32_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_32_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_32_png_file))

db_table['/icons/favicon_32.png'] = DB_Resource("/icons/favicon_32.png", "image/png", Supplier(favicon_32_png_supplier, favicon_32_png_supplier_time))

def favicon_64_png_supplier() -> bytes:
	with open(__icons_favicon_64_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_64_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_64_png_file))

db_table['/icons/favicon_64.png'] = DB_Resource("/icons/favicon_64.png", "image/png", Supplier(favicon_64_png_supplier, favicon_64_png_supplier_time))

def favicon_72_png_supplier() -> bytes:
	with open(__icons_favicon_72_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_72_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_72_png_file))

db_table['/icons/favicon_72.png'] = DB_Resource("/icons/favicon_72.png", "image/png", Supplier(favicon_72_png_supplier, favicon_72_png_supplier_time))

def favicon_96_png_supplier() -> bytes:
	with open(__icons_favicon_96_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_96_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_96_png_file))

db_table['/icons/favicon_96.png'] = DB_Resource("/icons/favicon_96.png", "image/png", Supplier(favicon_96_png_supplier, favicon_96_png_supplier_time))

def favicon_120_png_supplier() -> bytes:
	with open(__icons_favicon_120_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_120_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_120_png_file))

db_table['/icons/favicon_120.png'] = DB_Resource("/icons/favicon_120.png", "image/png", Supplier(favicon_120_png_supplier, favicon_120_png_supplier_time))

def favicon_128_png_supplier() -> bytes:
	with open(__icons_favicon_128_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_128_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_128_png_file))

db_table['/icons/favicon_128.png'] = DB_Resource("/icons/favicon_128.png", "image/png", Supplier(favicon_128_png_supplier, favicon_128_png_supplier_time))

def favicon_144_png_supplier() -> bytes:
	with open(__icons_favicon_144_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_144_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_144_png_file))

db_table['/icons/favicon_144.png'] = DB_Resource("/icons/favicon_144.png", "image/png", Supplier(favicon_144_png_supplier, favicon_144_png_supplier_time))

def favicon_152_png_supplier() -> bytes:
	with open(__icons_favicon_152_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_152_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_152_png_file))

db_table['/icons/favicon_152.png'] = DB_Resource("/icons/favicon_152.png", "image/png", Supplier(favicon_152_png_supplier, favicon_152_png_supplier_time))

def favicon_180_png_supplier() -> bytes:
	with open(__icons_favicon_180_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_180_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_180_png_file))

db_table['/icons/favicon_180.png'] = DB_Resource("/icons/favicon_180.png", "image/png", Supplier(favicon_180_png_supplier, favicon_180_png_supplier_time))

def favicon_192_png_supplier() -> bytes:
	with open(__icons_favicon_192_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_192_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_192_png_file))

db_table['/icons/favicon_192.png'] = DB_Resource("/icons/favicon_192.png", "image/png", Supplier(favicon_192_png_supplier, favicon_192_png_supplier_time))

def favicon_384_png_supplier() -> bytes:
	with open(__icons_favicon_384_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_384_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_384_png_file))

db_table['/icons/favicon_384.png'] = DB_Resource("/icons/favicon_384.png", "image/png", Supplier(favicon_384_png_supplier, favicon_384_png_supplier_time))

def favicon_512_png_supplier() -> bytes:
	with open(__icons_favicon_512_png_file, 'rb') as f:
		d = f.read()

	return d

def favicon_512_png_supplier_time() -> int:
	return int(path.getmtime(__icons_favicon_512_png_file))

db_table['/icons/favicon_512.png'] = DB_Resource("/icons/favicon_512.png", "image/png", Supplier(favicon_512_png_supplier, favicon_512_png_supplier_time))

def icons_app_icon_72_png_supplier() -> bytes:
	with open(__icons_app_icon_72_png_file, 'rb') as f:
		d = f.read()

	return d

def icons_app_icon_72_png_supplier_time() -> int:
	return int(path.getmtime(__icons_app_icon_72_png_file))

db_table['/icons/app/icon_72.png'] = DB_Resource("/icons/app/icon_72.png", "image/png", Supplier(icons_app_icon_72_png_supplier, icons_app_icon_72_png_supplier_time))

def icons_app_icon_96_png_supplier() -> bytes:
	with open(__icons_app_icon_96_png_file, 'rb') as f:
		d = f.read()

	return d

def icons_app_icon_96_png_supplier_time() -> int:
	return int(path.getmtime(__icons_app_icon_96_png_file))

db_table['/icons/app/icon_96.png'] = DB_Resource("/icons/app/icon_96.png", "image/png", Supplier(icons_app_icon_96_png_supplier, icons_app_icon_96_png_supplier_time))

def icons_app_icon_120_png_supplier() -> bytes:
	with open(__icons_app_icon_120_png_file, 'rb') as f:
		d = f.read()

	return d

def icons_app_icon_120_png_supplier_time() -> int:
	return int(path.getmtime(__icons_app_icon_120_png_file))

db_table['/icons/app/icon_120.png'] = DB_Resource("/icons/app/icon_120.png", "image/png", Supplier(icons_app_icon_120_png_supplier, icons_app_icon_120_png_supplier_time))

def icons_app_icon_144_png_supplier() -> bytes:
	with open(__icons_app_icon_144_png_file, 'rb') as f:
		d = f.read()

	return d

def icons_app_icon_144_png_supplier_time() -> int:
	return int(path.getmtime(__icons_app_icon_144_png_file))

db_table['/icons/app/icon_144.png'] = DB_Resource("/icons/app/icon_144.png", "image/png", Supplier(icons_app_icon_144_png_supplier, icons_app_icon_144_png_supplier_time))

def icons_app_icon_152_png_supplier() -> bytes:
	with open(__icons_app_icon_152_png_file, 'rb') as f:
		d = f.read()

	return d

def icons_app_icon_152_png_supplier_time() -> int:
	return int(path.getmtime(__icons_app_icon_152_png_file))

db_table['/icons/app/icon_152.png'] = DB_Resource("/icons/app/icon_152.png", "image/png", Supplier(icons_app_icon_152_png_supplier, icons_app_icon_152_png_supplier_time))

def icons_app_icon_180_png_supplier() -> bytes:
	with open(__icons_app_icon_180_png_file, 'rb') as f:
		d = f.read()

	return d

def icons_app_icon_180_png_supplier_time() -> int:
	return int(path.getmtime(__icons_app_icon_180_png_file))

db_table['/icons/app/icon_180.png'] = DB_Resource("/icons/app/icon_180.png", "image/png", Supplier(icons_app_icon_180_png_supplier, icons_app_icon_180_png_supplier_time))

def icons_app_icon_192_png_supplier() -> bytes:
	with open(__icons_app_icon_192_png_file, 'rb') as f:
		d = f.read()

	return d

def icons_app_icon_192_png_supplier_time() -> int:
	return int(path.getmtime(__icons_app_icon_192_png_file))

db_table['/icons/app/icon_192.png'] = DB_Resource("/icons/app/icon_192.png", "image/png", Supplier(icons_app_icon_192_png_supplier, icons_app_icon_192_png_supplier_time))

def icons_app_icon_384_png_supplier() -> bytes:
	with open(__icons_app_icon_384_png_file, 'rb') as f:
		d = f.read()

	return d

def icons_app_icon_384_png_supplier_time() -> int:
	return int(path.getmtime(__icons_app_icon_384_png_file))

db_table['/icons/app/icon_384.png'] = DB_Resource("/icons/app/icon_384.png", "image/png", Supplier(icons_app_icon_384_png_supplier, icons_app_icon_384_png_supplier_time))

def icons_app_icon_512_png_supplier() -> bytes:
	with open(__icons_app_icon_512_png_file, 'rb') as f:
		d = f.read()

	return d

def icons_app_icon_512_png_supplier_time() -> int:
	return int(path.getmtime(__icons_app_icon_512_png_file))

db_table['/icons/app/icon_512.png'] = DB_Resource("/icons/app/icon_512.png", "image/png", Supplier(icons_app_icon_512_png_supplier, icons_app_icon_512_png_supplier_time))

def icon_ios_splash_1125x2436_png_supplier() -> bytes:
	with open(__icons_ios_splash_1125x2436_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1125x2436_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1125x2436_png_file))

db_table['/icons/ios/splash_1125x2436.png'] = DB_Resource("/icons/ios/splash_1125x2436.png", "image/png", Supplier(icon_ios_splash_1125x2436_png_supplier, icon_ios_splash_1125x2436_png_supplier_time))

def icon_ios_splash_1170x2532_png_supplier() -> bytes:
	with open(__icons_ios_splash_1170x2532_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1170x2532_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1170x2532_png_file))

db_table['/icons/ios/splash_1170x2532.png'] = DB_Resource("/icons/ios/splash_1170x2532.png", "image/png", Supplier(icon_ios_splash_1170x2532_png_supplier, icon_ios_splash_1170x2532_png_supplier_time))

def icon_ios_splash_1179x2556_png_supplier() -> bytes:
	with open(__icons_ios_splash_1179x2556_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1179x2556_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1179x2556_png_file))

db_table['/icons/ios/splash_1179x2556.png'] = DB_Resource("/icons/ios/splash_1179x2556.png", "image/png", Supplier(icon_ios_splash_1179x2556_png_supplier, icon_ios_splash_1179x2556_png_supplier_time))

def icon_ios_splash_1242x2208_png_supplier() -> bytes:
	with open(__icons_ios_splash_1242x2208_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1242x2208_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1242x2208_png_file))

db_table['/icons/ios/splash_1242x2208.png'] = DB_Resource("/icons/ios/splash_1242x2208.png", "image/png", Supplier(icon_ios_splash_1242x2208_png_supplier, icon_ios_splash_1242x2208_png_supplier_time))

def icon_ios_splash_1242x2688_png_supplier() -> bytes:
	with open(__icons_ios_splash_1242x2688_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1242x2688_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1242x2688_png_file))

db_table['/icons/ios/splash_1242x2688.png'] = DB_Resource("/icons/ios/splash_1242x2688.png", "image/png", Supplier(icon_ios_splash_1242x2688_png_supplier, icon_ios_splash_1242x2688_png_supplier_time))

def icon_ios_splash_1284x2778_png_supplier() -> bytes:
	with open(__icons_ios_splash_1284x2778_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1284x2778_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1284x2778_png_file))

db_table['/icons/ios/splash_1284x2778.png'] = DB_Resource("/icons/ios/splash_1284x2778.png", "image/png", Supplier(icon_ios_splash_1284x2778_png_supplier, icon_ios_splash_1284x2778_png_supplier_time))

def icon_ios_splash_1290x2796_png_supplier() -> bytes:
	with open(__icons_ios_splash_1290x2796_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1290x2796_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1290x2796_png_file))

db_table['/icons/ios/splash_1290x2796.png'] = DB_Resource("/icons/ios/splash_1290x2796.png", "image/png", Supplier(icon_ios_splash_1290x2796_png_supplier, icon_ios_splash_1290x2796_png_supplier_time))

def icon_ios_splash_1488x2266_png_supplier() -> bytes:
	with open(__icons_ios_splash_1488x2266_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1488x2266_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1488x2266_png_file))

db_table['/icons/ios/splash_1488x2266.png'] = DB_Resource("/icons/ios/splash_1488x2266.png", "image/png", Supplier(icon_ios_splash_1488x2266_png_supplier, icon_ios_splash_1488x2266_png_supplier_time))

def icon_ios_splash_1536x2048_png_supplier() -> bytes:
	with open(__icons_ios_splash_1536x2048_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1536x2048_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1536x2048_png_file))

db_table['/icons/ios/splash_1536x2048.png'] = DB_Resource("/icons/ios/splash_1536x2048.png", "image/png", Supplier(icon_ios_splash_1536x2048_png_supplier, icon_ios_splash_1536x2048_png_supplier_time))

def icon_ios_splash_1620x2160_png_supplier() -> bytes:
	with open(__icons_ios_splash_1620x2160_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1620x2160_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1620x2160_png_file))

db_table['/icons/ios/splash_1620x2160.png'] = DB_Resource("/icons/ios/splash_1620x2160.png", "image/png", Supplier(icon_ios_splash_1620x2160_png_supplier, icon_ios_splash_1620x2160_png_supplier_time))

def icon_ios_splash_1640x2360_png_supplier() -> bytes:
	with open(__icons_ios_splash_1640x2360_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1640x2360_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1640x2360_png_file))

db_table['/icons/ios/splash_1640x2360.png'] = DB_Resource("/icons/ios/splash_1640x2360.png", "image/png", Supplier(icon_ios_splash_1640x2360_png_supplier, icon_ios_splash_1640x2360_png_supplier_time))

def icon_ios_splash_1668x2224_png_supplier() -> bytes:
	with open(__icons_ios_splash_1668x2224_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1668x2224_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1668x2224_png_file))

db_table['/icons/ios/splash_1668x2224.png'] = DB_Resource("/icons/ios/splash_1668x2224.png", "image/png", Supplier(icon_ios_splash_1668x2224_png_supplier, icon_ios_splash_1668x2224_png_supplier_time))

def icon_ios_splash_1668x2388_png_supplier() -> bytes:
	with open(__icons_ios_splash_1668x2388_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_1668x2388_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_1668x2388_png_file))

db_table['/icons/ios/splash_1668x2388.png'] = DB_Resource("/icons/ios/splash_1668x2388.png", "image/png", Supplier(icon_ios_splash_1668x2388_png_supplier, icon_ios_splash_1668x2388_png_supplier_time))

def icon_ios_splash_2048x1536_png_supplier() -> bytes:
	with open(__icons_ios_splash_2048x1536_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_2048x1536_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_2048x1536_png_file))

db_table['/icons/ios/splash_2048x1536.png'] = DB_Resource("/icons/ios/splash_2048x1536.png", "image/png", Supplier(icon_ios_splash_2048x1536_png_supplier, icon_ios_splash_2048x1536_png_supplier_time))

def icon_ios_splash_2048x2732_png_supplier() -> bytes:
	with open(__icons_ios_splash_2048x2732_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_2048x2732_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_2048x2732_png_file))

db_table['/icons/ios/splash_2048x2732.png'] = DB_Resource("/icons/ios/splash_2048x2732.png", "image/png", Supplier(icon_ios_splash_2048x2732_png_supplier, icon_ios_splash_2048x2732_png_supplier_time))

def icon_ios_splash_2160x1620_png_supplier() -> bytes:
	with open(__icons_ios_splash_2160x1620_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_2160x1620_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_2160x1620_png_file))

db_table['/icons/ios/splash_2160x1620.png'] = DB_Resource("/icons/ios/splash_2160x1620.png", "image/png", Supplier(icon_ios_splash_2160x1620_png_supplier, icon_ios_splash_2160x1620_png_supplier_time))

def icon_ios_splash_2224x1668_png_supplier() -> bytes:
	with open(__icons_ios_splash_2224x1668_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_2224x1668_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_2224x1668_png_file))

db_table['/icons/ios/splash_2224x1668.png'] = DB_Resource("/icons/ios/splash_2224x1668.png", "image/png", Supplier(icon_ios_splash_2224x1668_png_supplier, icon_ios_splash_2224x1668_png_supplier_time))

def icon_ios_splash_2266x1488_png_supplier() -> bytes:
	with open(__icons_ios_splash_2266x1488_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_2266x1488_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_2266x1488_png_file))

db_table['/icons/ios/splash_2266x1488.png'] = DB_Resource("/icons/ios/splash_2266x1488.png", "image/png", Supplier(icon_ios_splash_2266x1488_png_supplier, icon_ios_splash_2266x1488_png_supplier_time))

def icon_ios_splash_2360x1640_png_supplier() -> bytes:
	with open(__icons_ios_splash_2360x1640_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_2360x1640_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_2360x1640_png_file))

db_table['/icons/ios/splash_2360x1640.png'] = DB_Resource("/icons/ios/splash_2360x1640.png", "image/png", Supplier(icon_ios_splash_2360x1640_png_supplier, icon_ios_splash_2360x1640_png_supplier_time))

def icon_ios_splash_2388x1668_png_supplier() -> bytes:
	with open(__icons_ios_splash_2388x1668_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_2388x1668_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_2388x1668_png_file))

db_table['/icons/ios/splash_2388x1668.png'] = DB_Resource("/icons/ios/splash_2388x1668.png", "image/png", Supplier(icon_ios_splash_2388x1668_png_supplier, icon_ios_splash_2388x1668_png_supplier_time))

def icon_ios_splash_2732x2048_png_supplier() -> bytes:
	with open(__icons_ios_splash_2732x2048_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_2732x2048_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_2732x2048_png_file))

db_table['/icons/ios/splash_2732x2048.png'] = DB_Resource("/icons/ios/splash_2732x2048.png", "image/png", Supplier(icon_ios_splash_2732x2048_png_supplier, icon_ios_splash_2732x2048_png_supplier_time))

def icon_ios_splash_640x1136_png_supplier() -> bytes:
	with open(__icons_ios_splash_640x1136_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_640x1136_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_640x1136_png_file))

db_table['/icons/ios/splash_640x1136.png'] = DB_Resource("/icons/ios/splash_640x1136.png", "image/png", Supplier(icon_ios_splash_640x1136_png_supplier, icon_ios_splash_640x1136_png_supplier_time))

def icon_ios_splash_750x1334_png_supplier() -> bytes:
	with open(__icons_ios_splash_750x1334_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_750x1334_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_750x1334_png_file))

db_table['/icons/ios/splash_750x1334.png'] = DB_Resource("/icons/ios/splash_750x1334.png", "image/png", Supplier(icon_ios_splash_750x1334_png_supplier, icon_ios_splash_750x1334_png_supplier_time))

def icon_ios_splash_828x1792_png_supplier() -> bytes:
	with open(__icons_ios_splash_828x1792_png_file, 'rb') as f:
		d = f.read()

	return d

def icon_ios_splash_828x1792_png_supplier_time() -> int:
	return int(path.getmtime(__icons_ios_splash_828x1792_png_file))

db_table['/icons/ios/splash_828x1792.png'] = DB_Resource("/icons/ios/splash_828x1792.png", "image/png", Supplier(icon_ios_splash_828x1792_png_supplier, icon_ios_splash_828x1792_png_supplier_time))

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

def fonts_sharetechmono_css_supplier() -> bytes:
	with open(__fonts_sharetechmono_css_file, 'rb') as f:
		d = f.read()

	return d

def fonts_sharetechmono_css_supplier_time() -> int:
	return int(path.getmtime(__fonts_sharetechmono_css_file))

db_table['/fonts/sharetechmono.css'] = DB_Resource("/fonts/sharetechmono.css", "text/css", Supplier(fonts_sharetechmono_css_supplier, fonts_sharetechmono_css_supplier_time))

def fonts_sharetechmono_J7aHnp1uDWRBEqV98dVQztYldFcLowEF_woff2_supplier() -> bytes:
	with open(__fonts_sharetechmono_J7aHnp1uDWRBEqV98dVQztYldFcLowEF_woff2_file, 'rb') as f:
		d = f.read()

	return d

def fonts_sharetechmono_J7aHnp1uDWRBEqV98dVQztYldFcLowEF_woff2_supplier_time() -> int:
	return int(path.getmtime(__fonts_sharetechmono_J7aHnp1uDWRBEqV98dVQztYldFcLowEF_woff2_file))

db_table['/fonts/sharetechmono/J7aHnp1uDWRBEqV98dVQztYldFcLowEF.woff2'] = DB_Resource("/fonts/sharetechmono/J7aHnp1uDWRBEqV98dVQztYldFcLowEF.woff2", "application/font-woff2", Supplier(fonts_sharetechmono_css_supplier, fonts_sharetechmono_css_supplier_time))
