import configparser
import datetime
import os
import time

import requests
from lxml import etree

from phantomjs_helper import PhantomJsHelper

FILE_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')
DIRECTORY = FILE_PATH + "\\github"


def create_directory(name):
	if not os.path.exists(DIRECTORY):
		os.mkdir(DIRECTORY)
	print('创建目录:' + name)
	os.mkdir(name)


class Crawler(object):
	def __init__(self):
		self.phantomjs_helper = PhantomJsHelper()
		pass

	def crawl(self):
		page_source = self.get_page_source()
		git_list = self.get_git_href(page_source)
		for git in git_list:
			try:
				content, name = self.parse_git_href(git)
				self.save_article(content, name)
			except Exception as e:
				print(e)

	def get_page_source(self):
		config_parser = configparser.ConfigParser()
		config_parser.read(os.path.dirname(os.path.realpath(__file__)) + '\\config.txt')
		account = config_parser.get("Info", "account")
		password = config_parser.get("Info", "password")

		driver = self.phantomjs_helper.process_request('https://github.com/login')
		time.sleep(1)
		elem_login = driver.find_element_by_name("login")
		elem_login.send_keys(account)
		elem_password = driver.find_element_by_name("password")
		elem_password.send_keys(password)
		elem_commit = driver.find_element_by_name("commit")
		elem_commit.click()
		page_source = driver.page_source
		driver.quit()
		return page_source

	def get_git_href(self, page_source):
		xml = etree.HTML(page_source)
		content_list = xml.xpath('//div[@class="simple"]')
		yesterday = self.get_yesterday()
		git_list = []
		for content in content_list:
			time = str(content.xpath('div[@class="time"]/relative-time[@datetime]/@datetime'))
			if str(yesterday) == time[2:12]:
				href = 'http://github.com' + content.xpath('div[@class="title"]/a/@href')[1]
				git_list.append(href)
		return list(set(git_list))

	def parse_git_href(self, git: str):
		response = requests.get(git).text
		return response, git

	def save_article(self, content, git):
		name = git.split('/')[-1]
		file_path = DIRECTORY + '\\' + name
		create_directory(file_path)
		file = file_path + '\\README.html'
		with open(file, 'a', encoding='utf-8') as stream:
			stream.write(content + '\n\n')
			stream.close()
		file = file_path + '\\content.txt'
		with open(file, 'a', encoding='utf-8') as stream:
			stream.write(git)
			stream.close()
		xml = etree.HTML(content)
		img_url_list = xml.xpath('//article//img/@src')
		for index, img_url in enumerate(img_url_list):
			if 'camo.githubusercontent' in img_url:
				continue

			if not img_url.startswith("http"):
				img_url = "http://raw.githubusercontent.com" + img_url
			print(img_url)
			file = file_path + '\\image' + str(index) + '.jpg'
			try:
				response = requests.get(img_url, stream=True)
				if response.status_code == 200:
					with open(file, 'wb') as f:
						for chunk in response.iter_content(1024):
							f.write(chunk)
			except Exception as e:
				print(e)

	def get_yesterday(self):
		today = datetime.date.today()
		oneday = datetime.timedelta(days=1)
		yesterday = today - oneday
		return yesterday
