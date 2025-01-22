import mimetypes
import os
import re
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from os.path import basename
from smtplib import SMTPException

from dvrd_smtp.types import Recipients, Address, Recipient


class SMTPMessage:
    def __init__(self, *, to_addr: Recipients = None, from_addr: Recipient = None, cc: Recipients | None = None,
                 bcc: Recipients | None = None, reply_to: Recipient = None, subject: str = None, plain_body: str = None,
                 html_body: str = None, attachments: list[str] = None, return_path: Recipient = None,
                 dkim_cert_path: str = None, dkim_selector: str = None):
        self._to_addr = to_addr
        self._from_addr = from_addr
        self._cc = cc
        self._bcc = bcc
        self._reply_to = reply_to
        self._return_path = return_path
        self._subject = subject
        self._plain_body = plain_body
        self._html_body = html_body
        self._attachments = attachments
        self._dkim_cert_path = dkim_cert_path
        self._dkim_selector = dkim_selector

    @property
    def to_addr(self) -> Recipients | None:
        return self._to_addr

    @to_addr.setter
    def to_addr(self, value: Recipients):
        self._to_addr = value

    @property
    def from_addr(self) -> Recipient | None:
        return self._from_addr

    @from_addr.setter
    def from_addr(self, value: Recipient):
        self._from_addr = value

    @property
    def parsed_from_addr(self) -> str:
        if not self._from_addr:
            raise SMTPException('Missing from address or return path')
        return _format_address(address=self._from_addr)

    @property
    def envelope(self) -> str:
        if not self._return_path and not self._from_addr:
            raise SMTPException('Missing return path or from address')
        from_addr = self._return_path or self._from_addr
        return _format_address(address=from_addr)

    @property
    def cc(self) -> Recipients | None:
        return self._cc

    @cc.setter
    def cc(self, value: Recipients | None):
        self._cc = value

    @property
    def bcc(self) -> Recipients | None:
        return self._bcc

    @bcc.setter
    def bcc(self, value: Recipients | None):
        self._bcc = value

    @property
    def reply_to(self) -> Recipient | None:
        return self._reply_to

    @reply_to.setter
    def reply_to(self, value: Recipient | None):
        self._reply_to = value

    @property
    def all_recipients(self) -> list[str]:
        if isinstance(self.to_addr, list):
            recipients: list[str] = [_format_address(address=addr) for addr in self.to_addr]
        else:
            recipients: list[str] = [_format_address(address=self.to_addr)]
        if cc := self.cc:
            if isinstance(cc, list):
                recipients.extend(cc)
            elif isinstance(cc, str):
                recipients.append(cc)
            else:
                recipients.append(_format_address(address=cc, allow_none=True))
        if bcc := self.bcc:
            if isinstance(bcc, list):
                recipients.extend(bcc)
            elif isinstance(bcc, str):
                recipients.append(bcc)
            else:
                recipients.append(_format_address(address=bcc, allow_none=True))
        return recipients

    @property
    def subject(self) -> str | None:
        return self._subject

    @subject.setter
    def subject(self, value: str):
        self._subject = value

    @property
    def plain_body(self) -> str | None:
        return self._plain_body

    @plain_body.setter
    def plain_body(self, value: str):
        self._plain_body = value

    @property
    def html_body(self) -> str | None:
        return self._html_body

    @html_body.setter
    def html_body(self, value: str):
        self._html_body = value

    @property
    def attachments(self) -> list[str] | None:
        return self._attachments

    @attachments.setter
    def attachments(self, value: list[str]):
        self._attachments = value

    def add_attachment(self, *, attachment: str):
        attachments: list[str] = self._attachments or list()
        attachments.append(attachment)
        self._attachments = attachments

    def remove_attachment(self, *, attachment: str):
        if not (attachments := self._attachments):
            raise SMTPException('Attachment cannot be found')
        try:
            attachments.remove(attachment)
        except ValueError:
            raise SMTPException('Attachment cannot be found')

    def build(self) -> EmailMessage:
        message = EmailMessage()
        message['Subject'] = self._subject
        message['From'] = _format_address(address=self._from_addr)
        message['To'] = _format_address_list(addresses=self._to_addr, allow_none=False)
        if cc := _format_address_list(addresses=self._cc):
            message['CC'] = cc
        if reply_to := _format_address(address=self._reply_to, allow_none=True):
            message['Reply-To'] = reply_to
        message['Message-ID'] = make_msgid(domain=self._get_from_domain())
        if plain_body := self._plain_body:
            message.set_content(plain_body)
        if html_body := self._html_body:
            message.add_alternative(html_body, subtype='html')
        message = self._build_attachments(message=message)
        return self._dkim_sign_message(message=message)

    def _dkim_sign_message(self, *, message: EmailMessage) -> EmailMessage:
        if not (dkim_selector := self._dkim_selector) or not self._dkim_cert_path:
            return message
        try:
            import dkim
        except ImportError:
            # DKIM not installed
            return message
        with open(self._dkim_cert_path) as dkim_file:
            private_key = dkim_file.read()
        headers = [b'To', b'From', b'Subject', b'Message-ID']
        sig = dkim.sign(
            message=message.as_bytes(),
            selector=dkim_selector.encode(),
            domain=self._get_from_domain().encode(),
            privkey=private_key.encode(),
            include_headers=headers,
            linesep=b''
        )
        message['DKIM-Signature'] = sig[len('DKIM-Signature: '):].decode()
        return message

    def _get_from_domain(self) -> str | None:
        from_addr = _format_address(address=self._from_addr, allow_none=True)
        if not from_addr:
            return None
        email_reg = r'<[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.[a-zA-Z]{2,})>'
        if match := re.search(email_reg, from_addr):
            return match.group(1)
        else:
            return from_addr[from_addr.index('@') + 1:]

    def _build_attachments(self, message: EmailMessage):
        if not (attachments := self._attachments):
            return message
        for file_path in attachments:
            if not os.path.isfile(file_path):
                raise SMTPException(f'File {file_path} does not exist')
            ctype, _ = mimetypes.guess_type(file_path)
            if not ctype:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(file_path, 'rb') as fp:
                message.add_attachment(fp.read(),
                                       maintype=maintype,
                                       subtype=subtype,
                                       filename=basename(file_path))
        return message


def _format_address(*, address: str | Address | None, allow_none: bool = False) -> str | None:
    if address is None:
        if not allow_none:
            raise SMTPException('Address is not allowed to be None')
        return None
    if isinstance(address, str):
        return address
    return formataddr(address)


def _format_address_list(*, addresses: Recipients | None, allow_none: bool = True) -> str | None:
    if addresses is None:
        if not allow_none:
            raise SMTPException('Addresses is not allowed to be None')
        return None
    if isinstance(addresses, str):
        return addresses
    parsed_addresses = (_format_address(address=address, allow_none=allow_none) for address in addresses)
    return ', '.join(parsed_addresses)
