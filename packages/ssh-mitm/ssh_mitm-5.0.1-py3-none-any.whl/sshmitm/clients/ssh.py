"""
The module provides a set of classes for implementing SSH-MITM clients in Python.

The AuthenticationMethod class is a helper class that provides different methods
for authentication to a remote ssh server. It provides methods for authentication
using passwords, private key files, and key-pair certificates. This class makes
it easy to use different authentication methods in a consistent manner.

The BaseSSHClient class is an abstract class that provides the basic functionality
for an ssh client. This class provides methods to connect to a remote server, create
and use secure shell channels, and execute commands on the remote server.
It is designed to be extended and customized for specific use cases.

The SSHClient class is a concrete implementation of the BaseSSHClient class.
This class provides a high-level API for connecting to remote servers and
performing operations over ssh. It uses the Paramiko library under the hood
to handle the underlying ssh connectivity. This class makes it easy to connect
to remote servers, execute commands, and transfer files.
"""

import logging
from enum import Enum
from typing import TYPE_CHECKING, Optional

import paramiko
import paramiko.hostkeys
from paramiko.pkey import PKey
from sshpubkeys import SSHKey  # type: ignore[import-untyped]

from sshmitm.exceptions import InvalidHostKey, NoAgentKeys
from sshmitm.moduleparser import BaseModule

if TYPE_CHECKING:
    import sshmitm
    from sshmitm.forwarders.agent import AgentProxy
    from sshmitm.session import Session  # noqa: F401


class AuthenticationMethod(Enum):
    """
    An enumeration of possible authentication methods that can be
    used to connect to a remote host.
    """

    PASSWORD = "password"  # nosec # noqa: S105
    PUBLICKEY = "publickey"
    AGENT = "agent"


class BaseSSHClient(BaseModule):
    """ "
    The base class for an SSH client module.
    """


class SSHClient(BaseSSHClient):
    """
    The SSH client class, used to connect to a remote host.

    :param host: the hostname or IP address of the remote host
    :param port: the port number to connect to on the remote host
    :param method: the authentication method to use when connecting
    :param password: the password to use for authentication (if method is `password`)
    :param user: the username to use for authentication
    :param key: the public key to use for authentication (if method is `publickey`)
    :param session: the session instance
    """

    CIPHERS = None

    def __init__(  # pylint: disable=too-many-arguments
        self,
        host: str,
        port: int,
        method: AuthenticationMethod,
        password: Optional[str],
        user: str,
        key: Optional[PKey],
        session: "sshmitm.session.Session",
    ) -> None:
        super().__init__()
        self.session: "sshmitm.session.Session" = session
        self.session.register_session_thread()
        self.host: str = host
        self.port: int = port
        self.method: AuthenticationMethod = method
        self.user: str = user
        self.password: Optional[str] = password
        self.agent: Optional[AgentProxy] = self.session.agent
        self.key: Optional[PKey] = key
        self.transport: Optional[paramiko.Transport] = None
        self.connected: bool = False

    def connect(self) -> bool:  # noqa: C901
        """
        Connects to the remote host using the specified authentication method.

        :return: True if the connection was successful, False otherwise
        """
        message = None

        self.transport = paramiko.Transport((self.host, self.port))
        if self.CIPHERS:
            if not isinstance(self.CIPHERS, tuple):
                msg = "client ciphers must be a tuple"
                raise ValueError(msg)
            self.transport.get_security_options().ciphers = self.CIPHERS

        try:
            if self.method is AuthenticationMethod.PASSWORD:
                self.transport.connect(username=self.user, password=self.password)
            elif self.method is AuthenticationMethod.PUBLICKEY:
                self.transport.connect(
                    username=self.user, password=self.password, pkey=self.key
                )
            elif self.method is AuthenticationMethod.AGENT:
                if self.agent is not None:
                    keys = self.agent.get_keys()
                    if not keys:
                        raise NoAgentKeys
                    for k in keys:
                        try:
                            self.transport.connect(
                                username=self.user, password=self.password, pkey=k
                            )
                            ssh_pub_key = SSHKey(f"{k.get_name()} {k.get_base64()}")
                            ssh_pub_key.parse()
                            logging.debug(
                                "ssh-mitm connected to remote host with username=%s, key=%s %s %sbits",
                                self.user,
                                k.get_name(),
                                ssh_pub_key.hash_sha256(),
                                ssh_pub_key.bits,
                            )
                            break
                        except paramiko.AuthenticationException:
                            self.transport.close()
                            self.transport = paramiko.Transport((self.host, self.port))

            else:
                logging.error(
                    'authentication method "%s" not supported!', self.method.value
                )
                return False

            remotekey = self.transport.get_remote_server_key()
            if not self.check_host_key(
                f"{self.host}:{self.port}", remotekey.get_name(), remotekey
            ):
                raise InvalidHostKey
            self.connected = True
            # return True to force a login
            return True  # noqa: TRY300

        except paramiko.SSHException:
            message = "general ssh error"
        except NoAgentKeys:
            message = "no agent keys found"
        except InvalidHostKey:
            message = "Hostkey is invalid"

        userstring = f"{self.user}:{self.password}@{self.host}:{self.port}"
        logging.debug(
            "Authentication failed: %s, User: %s, Message: %s",
            self.method.value,
            userstring,
            message or "",
        )

        return False

    def check_host_key(self, hostname: str, keytype: str, key: PKey) -> bool:
        """
        Check the host key.

        :param hostname: Hostname of the remote server.
        :param keytype: Type of the key.
        :param key: Key of the remote server.
        :return: True if the host key is valid, False otherwise.
        """
        del hostname, keytype, key  # unused arguments
        return True
