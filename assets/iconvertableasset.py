from abc import abstractmethod
import os

class IConvertableAsset():

	@abstractmethod
	def loadAssets(self):
		pass

	@abstractmethod
	def move(self, path, type):
		pass

	@abstractmethod
	def convert(self):
		pass

	@abstractmethod
	def delete(self):
		pass
