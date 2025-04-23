from math import ceil, floor, trunc
from typing import Any, Callable, Generic, Optional, TypeVar, Union

from .monad import Monad

Maybe       = TypeVar('Maybe')
# MaybeBool   = TypeVar('MaybeBool')
# MaybeNumber = TypeVar('MaybeNumber')
# MaybeFloat  = TypeVar('MaybeFloat')
# MaybeInt    = TypeVar('MaybeInt')

T = TypeVar('T', bound = Any)
# N = TypeVar('N')

class Maybe(Generic[T]):
	pass

class Maybe(Monad[T]):
	def __init__(self, value:Optional[T]) -> None:
		self.__val = value

	@classmethod
	def wrap(cls, item:Optional[T]) -> Maybe[T]:
		return cls(item)

	def unwrap(self) -> Optional[T]:
		return self.__val

	def or_else(self, def_val:T) -> T:
		if self.unwrap() is None:
			return def_val
		
		return self.unwrap()

	def bind(self, fx:Callable[[T], Maybe]) -> Maybe:
		if self.unwrap() is None:
			return Maybe(None)

		return fx(self.unwrap())

	def map(self, fx:Callable[[T], T]) -> Maybe:
		return self.bind(lambda a: self.wrap(fx(a)))

	def wrap_nothing(self) -> Maybe:
		return self.wrap(None)

	def is_nothing(self) -> bool:
		return self.__val is None

	def __str__(self) -> str:
		if self.unwrap() is None:
			return "Nothing"

		return self.unwrap().__str__()

	def __repr__(self) -> str:
		if self.unwrap() is None:
			return "Nothing"

		return f"Just {self.unwrap().__repr__()}"

	def __bool__(self) -> bool:
		if self.unwrap() is None:
			return False

		return bool(self.unwrap())

	# Numeric Methods

	# Uniary Methods
	def __uniary_map(self, fx:Callable[[T], Any]) -> Maybe:
		return self.map(fx)

	def __trunc__(self) -> Maybe[int]:
		return self.__uniary_map(trunc)

	def __ceil__(self) -> Maybe[int]:
		return self.__uniary_map(ceil)

	def __floor__(self) -> Maybe[int]:
		return self.__uniary_map(floor)

	def __round__(self) -> Maybe[int]:
		return self.__uniary_map(round)

	def __invert__(self) -> Maybe[T]:
		return self.__uniary_map(lambda a: ~a)

	def __abs__(self) -> Maybe[T]:
		return self.__uniary_map(abs)

	def __neg__(self) -> Maybe[T]:
		return self.__uniary_map(lambda a: -a)

	def __pos__(self) -> Maybe[T]:
		return self.__uniary_map(lambda a: +a)

	# Binary Methods
	def __binary_map(self, other:Union[Any, Maybe[Any]], fx:Callable[[T, Any], Any]) -> Maybe[Any]:
		if isinstance(other, Maybe):
			return self.bind(lambda a: other.map(lambda b: fx(a, b)))

		return self.map(lambda a: fx(a, other))

	def __add__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a + b)

	def __radd__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a + b)

	def __sub__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a - b)

	def __rsub__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a - b)

	def __mul__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a * b)

	def __rmul__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a * b)

	def __floordiv__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a // b)

	def __rfloordiv__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a // b)

	def __truediv__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a / b)

	def __rtruediv__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a / b)

	def __mod__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a % b)

	def __rmod__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a % b)

	def __divmod__(self, other:Union[Any, Maybe[Any]]) -> tuple[Maybe[Any], Maybe[Any]]:
		return self.__binary_map(other, divmod)

	def __rdivmod__(self, other:Union[Any, Maybe[Any]]) -> tuple[Maybe[Any], Maybe[Any]]:
		return self.__binary_map(other, divmod)

	def __pow__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a ** b)

	def __rpow__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a ** b)

	def __lshift__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a << b)

	def __rlshift__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a << b)

	def __rshift__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a >> b)

	def __rrshift__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a >> b)

	def __and__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a & b)

	def __rand__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a & b)

	def __or__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a | b)

	def __ror__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a | b)

	def __xor__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a ^ b)

	def __rxor__(self, b:Union[Any, Maybe[Any]]) -> Maybe[Any]:
		return self.__binary_map(b, lambda a, b: a ^ b)

	def __eq__(self, other:Union[Any, Maybe[Any]]) -> Maybe[bool]:
		return self.__binary_map(other, lambda a, b: a == b)

	def __ne__(self, other:Union[Any, Maybe[Any]]) -> Maybe[bool]:
		return self.__binary_map(other, lambda a, b: a != b)

	def __lt__(self, other:Union[Any, Maybe[Any]]) -> Maybe[bool]:
		return self.__binary_map(other, lambda a, b: a < b)

	def __gt__(self, other:Union[Any, Maybe[Any]]) -> Maybe[bool]:
		return self.__binary_map(other, lambda a, b: a > b)

	def __le__(self, other:Union[Any, Maybe[Any]]) -> Maybe[bool]:
		return self.__binary_map(other, lambda a, b: a <= b)

	def __ge__(self, other:Union[Any, Maybe[Any]]) -> Maybe[bool]:
		return self.__binary_map(other, lambda a, b: a >= b)

# class MaybeBool(Maybe[bool]):
# 	def __init__(self, value):
# 		super().__init__(value)

# class MaybeNumber(Maybe):
# 	def __init__(self, value:Optional[N]) -> None:
# 		super().__init__(value)

# 	# Numeric uniary methods

# 	def __trunc__(self) -> MaybeInt:
# 		return self.bind(lambda a: MaybeInt(trunc(a)))

# 	def __ceil__(self) -> MaybeInt:
# 		return self.bind(lambda a: MaybeInt(ceil(a)))

# 	def __floor__(self) -> MaybeInt:
# 		return self.bind(lambda a: MaybeInt(floor(a)))

# 	def __round__(self) -> MaybeInt:
# 		return self.bind(lambda a: MaybeInt(round(a)))

# 	def __invert__(self) -> MaybeNumber:
# 		return self.bind(lambda a: self.wrap(~a))

# 	def __abs__(self) -> MaybeNumber:
# 		return self.bind(lambda a: self.wrap(abs(a)))

# 	def __neg__(self) -> MaybeNumber:
# 		return self.bind(lambda a: self.wrap(-a))

# 	def __pos__(self) -> MaybeNumber:
# 		return self.bind(lambda a: self.wrap(+a))

# 	# ALU binary operators

# 	def __add__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x + y))

# 		return self.bind(lambda a: self.wrap(a + b))

# 	def __radd__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x + y))

# 		return self.bind(lambda a: self.wrap(a + b))

# 	def __sub__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x - y))

# 		return self.bind(lambda a: self.wrap(a - b))

# 	def __rsub__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x - y))

# 		return self.bind(lambda a: self.wrap(a - b))

# 	def __mul__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x * y))

# 		return self.bind(lambda a: self.wrap(a * b))

# 	def __rmul__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x * y))

# 		return self.bind(lambda a: self.wrap(a * b))

# 	def __floordiv__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x // y))

# 		return self.bind(lambda a: self.wrap(a // b))

# 	def __rfloordiv__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x // y))

# 		return self.bind(lambda a: self.wrap(a // b))

# 	def __truediv__(self, b:Union[N, MaybeNumber]) -> MaybeFloat:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x / y))

# 		return self.bind(lambda a: MaybeFloat(a / b))

# 	def __rtruediv__(self, b:Union[N, MaybeNumber]) -> MaybeFloat:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x / y))

# 		return self.bind(lambda a: MaybeFloat(a / b))

# 	def __mod__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x % y))

# 		return self.bind(lambda a: self.wrap(a % b))

# 	def __rmod__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x % y))

# 		return self.bind(lambda a: self.wrap(a % b))

# 	def __divmod__(self, other:Union[N, MaybeNumber]) -> tuple[MaybeNumber, MaybeNumber]:
# 		if isinstance(other, MaybeNumber):
# 			return self.bind(lambda x: other.map(lambda y: divmod(x, y)))

# 		return self.bind(lambda a: self.wrap(divmod(a, other)))

# 	def __rdivmod__(self, other:Union[N, MaybeNumber]) -> tuple[MaybeNumber, MaybeNumber]:
# 		if isinstance(other, MaybeNumber):
# 			return self.bind(lambda x: other.map(lambda y: divmod(x, y)))

# 		return self.bind(lambda a: self.wrap(divmod(a, other)))

# 	def __pow__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x ** y))

# 		return self.bind(lambda a: self.wrap(a ** b))

# 	def __rpow__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x ** y))

# 		return self.bind(lambda a: self.wrap(a ** b))

# 	def __lshift__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x << y))

# 		return self.bind(lambda a: self.wrap(a << b))

# 	def __rlshift__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x << y))

# 		return self.bind(lambda a: self.wrap(a << b))

# 	def __rshift__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x << y))

# 		return self.bind(lambda a: self.wrap(a << b))

# 	def __rrshift__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x << y))

# 		return self.bind(lambda a: self.wrap(a << b))

# 	def __and__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x & y))

# 		return self.bind(lambda a: self.wrap(a & b))

# 	def __rand__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x & y))

# 		return self.bind(lambda a: self.wrap(a & b))

# 	def __or__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x | y))

# 		return self.bind(lambda a: self.wrap(a | b))

# 	def __ror__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x | y))

# 		return self.bind(lambda a: self.wrap(a | b))

# 	def __xor__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x ^ y))

# 		return self.bind(lambda a: self.wrap(a ^ b))

# 	def __rxor__(self, b:Union[N, MaybeNumber]) -> MaybeNumber:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x ^ y))

# 		return self.bind(lambda a: self.wrap(a ^ b))

# 	# Comparison Methods
# 	def __eq__(self, b:Union[N, MaybeNumber]) -> MaybeBool:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.bind(lambda y: MaybeBool(x == y)))

# 		return self.bind(lambda a: MaybeBool(a == b))

# 	def __ne__(self, b:Union[N, MaybeNumber]) -> MaybeBool:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x != y))

# 		return self.bind(lambda a: self.wrap(a != b))

# 	def __lt__(self, b:Union[N, MaybeNumber]) -> MaybeBool:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x < y))

# 		return self.bind(lambda a: self.wrap(a < b))

# 	def __gt__(self, b:Union[N, MaybeNumber]) -> MaybeBool:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x > y))

# 		return self.bind(lambda a: self.wrap(a > b))

# 	def __le__(self, b:Union[N, MaybeNumber]) -> MaybeBool:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x <= y))

# 		return self.bind(lambda a: self.wrap(a <= b))

# 	def __ge__(self, b:Union[N, MaybeNumber]) -> MaybeBool:
# 		if isinstance(b, MaybeNumber):
# 			return self.bind(lambda x: b.map(lambda y: x >= y))

# 		return self.bind(lambda a: self.wrap(a >= b))

# class MaybeFloat(MaybeNumber):
# 	def __init__(self, value):
# 		super().__init__(value)

# class MaybeInt(MaybeNumber):
# 	def __init__(self, value):
# 		super().__init__(value)
