from typing import BinaryIO

Address = tuple[str, str]
Recipients = Address | str | list[Address | str]
Recipient = Address | str
Attachment = str | BinaryIO
