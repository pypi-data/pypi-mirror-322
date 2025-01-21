from typing import TypedDict
import warnings

import curl_cffi.curl
from curl_cffi._wrapper import ffi, lib 
from curl_cffi.curl import CurlHttpVersion, CurlOpt
from curl_cffi.const import CurlSslVersion
from curl_cffi.requests.impersonate import (
	TLS_CIPHER_NAME_MAP,
	TLS_EC_CURVES_MAP,
	TLS_VERSION_MAP,
	ExtraFingerprints,
	normalize_browser_type,
	toggle_extension,
	BrowserTypeLiteral
)

from .base_adapter import BaseCurlAdapter

class CurlAdapterConfigurationOptions(TypedDict):
	ja3_str: str
	permute: bool
	akamai_str: str

class CurlCffiAdapter(BaseCurlAdapter):

	def __init__(self, 
			debug=False, 
			impersonate_browser_type: BrowserTypeLiteral="chrome", 
			use_curl_content_decoding=False, 
			use_thread_local_curl=True,
			tls_configuration_options: CurlAdapterConfigurationOptions=None
		):

		self.impersonate_browser_type = impersonate_browser_type
		
		self.configuration_options = tls_configuration_options

		super().__init__(curl_cffi.Curl, debug, use_curl_content_decoding, use_thread_local_curl)

	def enable_debug(self):
		if self.debug:
			self.curl.debug()

	def get_curl_info(self, curl: curl_cffi.Curl, option_code: int):
		if option_code >= 0x600000:
			"""
				Currently, curl_cfii doesn't work for retriving information like TOTAL_TIME_T, SPEED_DOWNLOAD_T,
				because they haven't mapped the all option codes. (These options start at 0x600000 int64_t, but curl_cfii maps only up to 0x400000...)
			"""
			c_value = ffi.new("int64_t*")
			value = lib.curl_easy_getinfo(curl._curl, option_code, c_value)
			curl._check_error(value, "getinfo", option_code)
			if c_value[0] == ffi.NULL:
				return None
			return int(c_value[0])
		
		return super().get_curl_info(curl, option_code)

	def set_ja3_options(self, curl: curl_cffi.Curl, ja3: str, permute: bool = False):
		"""
		Detailed explanation: https://engineering.salesforce.com/tls-fingerprinting-with-ja3-and-ja3s-247362855967/
		"""

		def toggle_extensions_by_ids(curl: curl_cffi.Curl, extension_ids):
			# TODO: find a better representation, rather than magic numbers
			default_enabled = {0, 51, 13, 43, 65281, 23, 10, 45, 35, 11, 16}

			to_enable_ids = extension_ids - default_enabled
			for ext_id in to_enable_ids:
				toggle_extension(curl, ext_id, enable=True)

			# print("to_enable: ", to_enable_ids)

			to_disable_ids = default_enabled - extension_ids
			for ext_id in to_disable_ids:
				toggle_extension(curl, ext_id, enable=False)

		tls_version, ciphers, extensions, curves, curve_formats = ja3.split(",")
	
		curl_tls_version = TLS_VERSION_MAP[int(tls_version)]
		curl.setopt(CurlOpt.SSLVERSION, curl_tls_version | CurlSslVersion.MAX_DEFAULT)
		assert curl_tls_version == CurlSslVersion.TLSv1_2, "Only TLS v1.2 works for now."
	
		cipher_names = []
		for cipher in ciphers.split("-"):
			cipher_id = int(cipher)
			cipher_name = TLS_CIPHER_NAME_MAP[cipher_id]
			cipher_names.append(cipher_name)
	
		curl.setopt(CurlOpt.SSL_CIPHER_LIST, ":".join(cipher_names))
	
		if extensions.endswith("-21"):
			extensions = extensions[:-3]
			warnings.warn(
				"Padding(21) extension found in ja3 string, whether to add it should "
				"be managed by the SSL engine. The TLS client hello packet may contain "
				"or not contain this extension, any of which should be correct.",
				stacklevel=1,
			)
		extension_ids = set(int(e) for e in extensions.split("-"))
		toggle_extensions_by_ids(curl, extension_ids)
	
		if not permute:
			curl.setopt(CurlOpt.TLS_EXTENSION_ORDER, extensions)

		TLS_EC_CURVES_MAP = {
			19: "P-192",
			21: "P-224",
			23: "P-256",
			24: "P-384",
			25: "P-521",
			29: "X25519",
			4588: "X25519MLKEM768", #https://www.ietf.org/archive/id/draft-kwiatkowski-tls-ecdhe-mlkem-02.html
			25497: "X25519Kyber768Draft00",
		
		}

		curve_names = []
		for curve in curves.split("-"):
			curve_id = int(curve)
			curve_name = TLS_EC_CURVES_MAP[curve_id]
			curve_names.append(curve_name)
	
		curl.setopt(CurlOpt.SSL_EC_CURVES, ":".join(curve_names))
	
		assert int(curve_formats) == 0, "Only curve_formats == 0 is supported."

	def set_akamai_options(self, curl: curl_cffi.Curl, akamai: str):
		"""
		Detailed explanation: https://www.blackhat.com/docs/eu-17/materials/eu-17-Shuster-Passive-Fingerprinting-Of-HTTP2-Clients-wp.pdf
		"""
		settings, window_update, streams, header_order = akamai.split("|")
		
		# For compatiblity with tls.peet.ws
		settings = settings.replace(",", ";")
		
		curl.setopt(CurlOpt.HTTP_VERSION, CurlHttpVersion.V2_0)
		
		curl.setopt(CurlOpt.HTTP2_SETTINGS, settings)
		curl.setopt(CurlOpt.HTTP2_WINDOW_UPDATE, int(window_update))
		
		if streams != "0":
			curl.setopt(CurlOpt.HTTP2_STREAMS, streams)
		
		# m,a,s,p -> masp
		# curl-impersonate only accepts masp format, without commas.
		curl.setopt(CurlOpt.HTTP2_PSEUDO_HEADERS_ORDER, header_order.replace(",", ""))
	
	def set_curl_options(self, curl, request, url, timeout, proxies):
		
		super().set_curl_options(curl, request, url, timeout, proxies)

		# impersonate
		curl.impersonate(
			normalize_browser_type(self.impersonate_browser_type), 
			default_headers=False
		)

		# additional TLS fingerprint configuration options
		if self.configuration_options:
			if self.configuration_options.get("ja3_str"):
				self.set_ja3_options(
					curl, 
					self.configuration_options.get("ja3_str"), 
					self.configuration_options.get("permute", False)
				)
			if self.configuration_options.get("akamai_str"):
				self.set_akamai_options(
					curl,
					self.configuration_options.get("akamai_str")
				)
	