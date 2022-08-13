from abc import abstractmethod

class IOptimizableContainer():
	"""
	Represent an optimizable CoD4 asset container.
	"""

	@abstractmethod
	def load_assets(self):
		"""
		Load all assets from the CSV hint file.
		"""
		pass

	@abstractmethod
	def move(self, path, type):
		"""
		Move all assets to a specified path.
		"""
		pass

	@abstractmethod
	def optimize(self):
		"""
		Optimize all assets.
		"""
		pass

	@abstractmethod
	def delete(self):
		"""
		Delete all assets.
		"""
		pass
