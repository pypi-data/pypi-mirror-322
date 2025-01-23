import traceback

class TaskError(Exception):
    """
    自定义异常类

    用于处理任务相关的异常。

    :param message: 异常的消息字符串。
    :param data: 可选的附加数据字典。
    :param code: 错误码，默认为 500。
    :param original_exception: 可选的原始异常对象。
    """

    def __init__(
        self,
        message: str,
        data: dict | None = None,
        code: int = None,
        original_exception: Exception | None = None,
    ) -> None:
        """
        初始化 TaskError 异常。

        :param message: 异常的消息内容。
        :param data: 可选的附加数据，默认为 None。
        :param code: 错误码，默认为 500。
        :param original_exception: 可选的原始异常对象。
        """
        self.message: str = message
        self.data: dict | None = data or {}
        self.code: int = code or 500
        self.original_exception: Exception | None = original_exception
        self.stack_trace: str | None = (
            traceback.format_exc() if original_exception else None
        )
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        返回异常的字符串表示形式。

        :return: 异常消息字符串。
        """
        base_message = f"[{self.code}] {self.message}"
        context_message = f"Data: {self.data}" if self.data else "No additional data"
        if self.original_exception:
            original_message = f"Original Exception: {repr(self.original_exception)}"
            stack_message = f"Stack Trace:\n{self.stack_trace}"
            return f"{base_message}\n{context_message}\n{original_message}\n{stack_message}"
        return f"{base_message}\n{context_message}"
    
class TimeoutError(Exception):
    """自定义超时异常"""
    pass

class ElementNotInViewportError(Exception):
    """自定义元素不在视窗内，需要滚动窗口"""
    pass

class NotImplementError(Exception):
    """尚未实现"""
    pass

class NotSupportError(Exception):
    """不支持"""
    pass

class RequestParameterError(Exception):
    """请求参数错误"""
    pass

class CookieExpiredError(Exception):
    """Cookie过期"""
    pass

class InternalError(Exception):
    pass

class HTTPError(Exception):
    """HTTP请求错误"""

    def __init__(self, code: int, message: str) -> None:
        """
        初始化 HTTPError 异常。

        :param code: HTTP 状态码。
        :param message: 错误消息。
        """
        self.code: int = code
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        返回异常的字符串表示形式。

        :return: 格式化的 HTTP 错误信息字符串。
        """
        return f"HttpCode: {self.code}\nMessage: {self.message}"
    
