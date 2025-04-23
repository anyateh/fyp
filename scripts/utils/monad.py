from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar

Monad = TypeVar('Monad')
T     = TypeVar('T', Any)

class Monad(ABC, Generic[T]):
	@classmethod
	@abstractmethod
	def wrap(cls, item) -> Monad[T]:
		pass

	@abstractmethod
	def bind(self, fx:Callable[[Any], Monad[T]]) -> Monad[T]:
		pass
