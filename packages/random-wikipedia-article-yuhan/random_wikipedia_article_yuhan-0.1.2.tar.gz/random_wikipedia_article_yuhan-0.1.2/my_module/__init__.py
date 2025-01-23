# 定義此包可以導出的模組名稱
__all__ = ['my_email']

# 導入 my_email 模組
from . import my_email

# 如果您想直接從 my_module 中使用 my_email 的內容
# 可以使用 from .my_email import * 
# 或者指定要導入的具體內容