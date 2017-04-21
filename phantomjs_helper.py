from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class PhantomJsHelper(object):
	def process_request(self, url):
		driver = self.phantomjs_opened()
		driver.get(url)
		return driver

	def phantomjs_opened(self):
		capabilities = DesiredCapabilities.PHANTOMJS.copy()
		# proxy = proxy_pool.random_choice_proxy()
		# capabilities['proxy'] = {
		# 	'proxyType': 'MANUAL',
		# 	'ftpProxy': proxy,
		# 	'sslProxy': proxy,
		# 	'httpProxy': proxy,
		# 	'noProxy': None
		# }
		# capabilities['phantomjs.cli.args'] = [
		# 	'--proxy-auth=' + evar.get('WONDERPROXY_USER') + ':' + evar.get('WONDERPROXY_PASS')
		# ]
		# driver = webdriver.PhantomJS(desired_capabilities=capabilities)
		driver = webdriver.Ie()
		# driver.set_page_load_timeout(60)
		return driver

	def phantomjs_closed(self, driver):
		driver.quit()
