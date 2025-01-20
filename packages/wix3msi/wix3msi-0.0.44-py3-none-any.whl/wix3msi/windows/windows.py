#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import os
import shutil
import ctypes
import sys



#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
SPACE: str = " "


#--------------------------------------------------------------------------------
# 윈도우 유틸리티.
#--------------------------------------------------------------------------------
class Windows:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 관리자모드가 아닐 경우 관리자모드로 재실행.
	#--------------------------------------------------------------------------------
	@staticmethod	
	def ExecuteWithAdministrator(callback: Callable[[], None]) -> None:
		isAdministrator = Windows.IsAdministrator()
		if isAdministrator:
			callback()
		else:
			argumentListString = SPACE.join(sys.argv)
			ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, argumentListString, None, 1)
			sys.exit(0)

		
	#--------------------------------------------------------------------------------
	# 관리자모드 실행인지 여부.
	#--------------------------------------------------------------------------------
	@staticmethod
	def IsAdministrator() -> bool:
		try:
			if not ctypes.windll.shell32.IsUserAnAdmin():
				return False
			return True
		except Exception as exception:
			return False