import logging
from typing import TYPE_CHECKING, Optional, Type, Union, cast

import paramiko

from sshmitm.interfaces.sftp import BaseSFTPServerInterface
from sshmitm.moduleparser import BaseModule

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer

    import sshmitm


class SFTPHandlerBasePlugin(BaseModule):
    def __init__(self, sftp: "SFTPBaseHandle", filename: str) -> None:
        super().__init__()
        self.filename: str = filename
        self.sftp: "SFTPBaseHandle" = sftp

    @classmethod
    def get_interface(cls) -> Optional[Type[BaseSFTPServerInterface]]:
        return None

    @classmethod
    def get_file_handle(cls) -> Type["SFTPBaseHandle"]:
        return cast(Type[SFTPBaseHandle], SFTPBaseHandle)

    def close(self) -> None:
        pass

    def handle_data(
        self, data: bytes, *, offset: Optional[int] = None, length: Optional[int] = None
    ) -> bytes:
        del offset, length  # unused arguments
        return data


class SFTPHandlerPlugin(SFTPHandlerBasePlugin):
    """transfer files from/to remote sftp server"""


class SFTPBaseHandle(paramiko.SFTPHandle):
    def __init__(
        self,
        session: "sshmitm.session.Session",
        plugin: Type[SFTPHandlerBasePlugin],
        filename: str,
        flags: int = 0,
    ) -> None:
        super().__init__(flags)
        self.session = session
        self.session.register_session_thread()
        self.plugin = plugin(self, filename)
        self.writefile: Optional[paramiko.sftp_file.SFTPFile] = None
        self.readfile: Optional[paramiko.sftp_file.SFTPFile] = None

    def close(self) -> None:
        super().close()
        self.plugin.close()

    def read(self, offset: int, length: int) -> Union[bytes, int]:
        logging.debug("R_OFFSET: %s", offset)
        if self.readfile is None:
            return paramiko.sftp.SFTP_FAILURE
        data = self.readfile.read(length)
        return self.plugin.handle_data(data, length=length)

    def write(self, offset: int, data: "ReadableBuffer") -> int:
        logging.debug("W_OFFSET: %s", offset)
        if not isinstance(data, bytes):
            logging.error("SFTPBaseHandle.write got invalid argument!")
            return paramiko.sftp.SFTP_FAILURE
        data = self.plugin.handle_data(data, offset=offset)
        if self.writefile is None:
            return paramiko.sftp.SFTP_FAILURE
        self.writefile.write(data)
        return paramiko.sftp.SFTP_OK
