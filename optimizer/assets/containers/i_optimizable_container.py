from typing import List
from abc import abstractmethod

class IOptimizableContainer():
	"""
	Represent an optimizable CoD4 asset container.
	"""

	@abstractmethod
	def add_items(self, items: List[str]):
		"""
		Add assets to the container to optimize.
		"""
		pass


	@abstractmethod
	def optimize(self):
		"""
		Optimize all assets.
		"""
		pass


	@abstractmethod
	def copy(self, to_path: str):
		"""
		Copy all assets to a specific path.
		"""
		pass
