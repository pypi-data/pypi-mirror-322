"""Module that defines a ConfigSection for uvicorn"""

from __future__ import annotations

import ssl
from dataclasses import asdict, field
from typing import Any

from application_settings import ConfigSectionBase, attributes_doc, dataclass


@attributes_doc
@dataclass(frozen=True)
class UvicornApplicationConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to the application to serve."""

    app: str = ""
    """The ASGI application to run, in the format `'<module>:<attribute>'`. Set to '' if you supply the app instance.
    Default: ''."""

    factory: bool = False
    """Whether or not to treat app as an application factory, i.e. a () -> <ASGI app> callable; default: False."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornApplicationConfigSection to a dictionary suitable for Uvicorn configuration."""
        uvicorn_config_dict = asdict(self)
        if not self.app:
            uvicorn_config_dict.pop("app")
        return uvicorn_config_dict


@attributes_doc
@dataclass(frozen=True)
class UvicornSocketBindingConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to socket binding."""

    host: str = "127.0.0.1"
    """Bind socket to this host. Use '0.0.0.0' to make the application available on your local network.
    IPv6 addresses are supported, for example: '::'. Default: '127.0.0.1'."""

    port: int = 8000
    """Bind to a socket with this port. Default: 8000"""

    uds: str = ""
    """Bind to a UNIX domain socket, for example '/tmp/uvicorn.sock'. Useful if you want to run Uvicorn behind a
    reverse proxy. Set to '' if you don't want to use this. Default: ''."""

    fd: int = -1
    """Bind to socket from this file descriptor. Useful if you want to run Uvicorn within a process manager.
    Set to a negative number if you don't want to use this. Default: -1."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornSocketBindingConfigSection to a dictionary suitable for Uvicorn configuration."""
        uvicorn_config_dict = asdict(self)
        if not self.uds:
            uvicorn_config_dict.pop("uds")
        if self.fd < 0:
            uvicorn_config_dict.pop("fd")
        return uvicorn_config_dict


@attributes_doc
@dataclass(frozen=True)
class UvicornDevelopmentConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to development."""

    reload: bool = False
    """Whether or not to enable auto-reload. uvicorn_configurable currently only supports reload for reload_dirs.
    Default: False."""

    reload_dirs: list[str] = field(default_factory=lambda: [])
    """Specify which directories to watch for python file changes. If an empty list, then by default the whole current
    directory will be watched. Default: []."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornDevelopmentConfigSection to a dictionary suitable for Uvicorn configuration."""
        uvicorn_config_dict = asdict(self)
        if not self.reload_dirs:
            uvicorn_config_dict.pop("reload_dirs")
        return uvicorn_config_dict


@attributes_doc
@dataclass(frozen=True)
class UvicornProductionConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to production."""

    workers: int = 0
    """Use multiple worker processes. Set to 0 to obtain the uvicorn default, which is setting it to the
    $WEB_CONCURRENCY environment variable if available, or 1. Default: 0."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornProductionConfigSection to a dictionary suitable for Uvicorn configuration."""
        if self.workers:
            return asdict(self)
        return {}


@attributes_doc
@dataclass(frozen=True)
class UvicornLoggingConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to logging."""

    set_default_log_config: bool = True
    """If True, the default LOG_CONFIG of uvicorn is set; if False, then self.log_config is set. Default: True"""

    log_config: str = ""
    """Logging configuration file. Options: dictConfig() formats: .json, .yaml. Any other format will be processed with
    fileConfig(). Set the formatters.default.use_colors and formatters.access.use_colors values to override the
    auto-detected behavior. If you wish to use a YAML file for your logging config, you will need to include PyYAML as
    a dependency for your project or install uvicorn with the [standard] optional extras. Set to '' in order to set the
    log_config to None. Default: ''."""

    log_level: str = "info"
    """Sets the log level. Options: 'critical', 'error', 'warning', 'info', 'debug', 'trace'. Default: 'info'."""

    access_log: bool = True
    """Whether or not to have an access log, without changing log level. Default: True."""

    use_colors: int = -1
    """Enable / disable colorized formatting of the log records. Valid values: -1, 0, 1. A value of -1 means do not
    set, in case this is not set it will be auto-detected. A value of 0 means disable and 1 is enable. This option is
    ignored if the --log-config CLI option is used. Default: -1 (do not set). """

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornLoggingConfigSection to a dictionary suitable for Uvicorn configuration."""
        uvicorn_config_dict = asdict(self)
        uvicorn_config_dict.pop("set_default_log_config")
        if self.set_default_log_config:
            uvicorn_config_dict.pop("log_config")
        else:
            if not self.log_config:
                uvicorn_config_dict["log_config"] = None
        if self.use_colors < 0:
            uvicorn_config_dict.pop("use_colors")
        else:
            uvicorn_config_dict["use_colors"] = self.use_colors != 0
        return uvicorn_config_dict


@attributes_doc
@dataclass(frozen=True)
class UvicornImplementationConfigSection(ConfigSectionBase):  # pylint: disable=too-many-instance-attributes
    """ConfigSection for uvicorn, settings related to implementation."""

    loop: str = "auto"
    """Set the event loop implementation. The uvloop implementation provides greater performance, but is not compatible
    with Windows or PyPy. Options: 'auto', 'asyncio', 'uvloop'. Default: 'auto'."""

    http: str = "auto"
    """Set the HTTP protocol implementation. The httptools implementation provides greater performance, but is not
    compatible with PyPy. Options: 'auto', 'h11', 'httptools'. Default: 'auto'."""

    ws: str = "auto"
    """Sets the WebSockets protocol implementation. Either of the websockets and wsproto packages are supported. Use
    'none' to ignore all websocket requests. Options: 'auto', 'none', 'websockets', 'wsproto'. Default: 'auto'."""

    ws_max_size: int = 16777216
    """Sets the WebSockets max message size, in bytes. Please note that this can be used only with the default
    websockets protocol. Default: 16777216."""

    ws_max_queue: int = 32
    """Sets the maximum length of the WebSocket incoming message queue. Please note that this can be used only with the
    default websockets protocol. Default: 32."""

    ws_ping_interval: float = 20.0
    """Sets the WebSockets ping interval, in seconds. Please note that this can be used only with the default
    websockets protocol. Default: 20.0."""

    ws_ping_timeout: float = 20.0
    """Sets the WebSockets ping timeout, in seconds. Please note that this can be used only with the default websockets
    protocol. Default: 20.0."""

    lifespan: str = "auto"
    """Sets the Lifespan protocol implementation. Options: 'auto', 'on', 'off'. Default: 'auto'."""

    h11_max_incomplete_event_size: int = 16384
    """Sets the maximum number of bytes to buffer of an incomplete event. Only available for h11 HTTP protocol
    implementation. Default: '16384' (16 KB)."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornImplementationConfigSection to a dictionary suitable for Uvicorn configuration."""
        return asdict(self)


@attributes_doc
@dataclass(frozen=True)
class UvicornApplicationInterfaceConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to application interface."""

    interface: str = "auto"
    """Select ASGI3, ASGI2, or WSGI as the application interface. Note that WSGI mode always disables WebSocket
    support, as it is not supported by the WSGI interface. Options: 'auto', 'asgi3', 'asgi2', 'wsgi'. Warning: 
    Uvicorn's native WSGI implementation is deprecated, you should switch to a2wsgi (pip install a2wsgi).
    Default: 'auto'."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornApplicationInterfaceConfigSection to a dictionary suitable for Uvicorn configuration."""
        return asdict(self)


@attributes_doc
@dataclass(frozen=True)
class UvicornHTTPConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to HTTP."""

    root_path: str = ""
    """Set the ASGI root_path for applications submounted below a given URL path; default: ''."""

    proxy_headers: bool = True
    """Whether or not to enable X-Forwarded-Proto, X-Forwarded-For to populate remote address info. Default: True,
    but is restricted to only trusting connecting IPs in the forwarded-allow-ips configuration."""

    set_default_forwarded_allow_ips: bool = True
    """Whether or not to appy the uvicorn default for 'forwarded_allow_ips', which equals the $FORWARDED_ALLOW_IPS
    environment variable if available, or '127.0.0.1'. Default: True. The field 'forwarded_allow_ips' is used only
    if this field is set to False."""

    forwarded_allow_ips: list[str] = field(default_factory=lambda: [])
    """Comma separated list of IP Addresses, IP Networks, or literals (e.g. UNIX Socket path) to trust with proxy
    headers. The literal '*' means trust everything. This setting is applied only if 'set_default_forwarded_allow_ips'
    is False."""

    server_header: bool = True
    """Whether or not to enable default Server header; default: True."""

    date_header: bool = True
    """Whether or not to enable default Date header; default: True. Note: This flag doesn't have effect on the
    websockets implementation."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornHTTPConfigSection to a dictionary suitable for Uvicorn configuration."""
        uvicorn_config_dict = asdict(self)
        uvicorn_config_dict.pop("set_default_forwarded_allow_ips")
        if self.set_default_forwarded_allow_ips:
            uvicorn_config_dict.pop("forwarded_allow_ips")
        return uvicorn_config_dict


@attributes_doc
@dataclass(frozen=True)
class UvicornHTTPSConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to HTTPS.
    To understand more about the SSL context options, please refer to the Python documentation."""

    ssl_keyfile: str = ""
    """Pathlike string that specifies where to find the SSL key file; default: '', which implies not set."""

    ssl_keyfile_password: str = ""
    """The password to decrypt the ssl key; default: '', which implies not set."""

    ssl_certfile: str = ""
    """The SSL certificate file."""

    ssl_version: int = ssl.PROTOCOL_TLS_SERVER
    """The SSL version to use; default: ssl.PROTOCOL_TLS_SERVER."""

    ssl_cert_reqs: int = ssl.CERT_NONE
    """Whether client certificate is required; default: ssl.CERT_NONE."""

    ssl_ca_certs: str = ""
    """The CA certificates file; default: '', which implies not set."""

    ssl_ciphers: str = "TLSv1"
    """The ciphers to use; default: 'TLSv1'."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornHTTPSConfigSection to a dictionary suitable for Uvicorn configuration."""
        uvicorn_config_dict = asdict(self)
        if not self.ssl_keyfile:
            uvicorn_config_dict.pop("ssl_keyfile")
        if not self.ssl_keyfile_password:
            uvicorn_config_dict.pop("ssl_keyfile_password")
        if not self.ssl_certfile:
            uvicorn_config_dict.pop("ssl_certfile")
        if not self.ssl_ca_certs:
            uvicorn_config_dict.pop("ssl_ca_certs")
        return uvicorn_config_dict


@attributes_doc
@dataclass(frozen=True)
class UvicornResourceLimitsConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to resource limits."""

    limit_concurrency: int = -1
    """Maximum number of concurrent connections or tasks to allow, before issuing HTTP 503 responses. Useful for
    ensuring known memory usage patterns even under over-resourced loads. Default: -1, which implies not set."""

    limit_max_requests: int = -1
    """Maximum number of requests to service before terminating the process. Useful when running together with a
    process manager, for preventing memory leaks from impacting long-running processes. Default: -1, which implies
    not set."""

    backlog: int = 2048
    """Maximum number of connections to hold in backlog. Relevant for heavy incoming traffic. Default: 2048."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornResourceLimitsConfigSection to a dictionary suitable for Uvicorn configuration."""
        uvicorn_config_dict = asdict(self)
        if self.limit_concurrency == -1:
            uvicorn_config_dict.pop("limit_concurrency")
        if self.limit_max_requests == -1:
            uvicorn_config_dict.pop("limit_max_requests")
        return uvicorn_config_dict


@attributes_doc
@dataclass(frozen=True)
class UvicornTimeoutsConfigSection(ConfigSectionBase):
    """ConfigSection for uvicorn, settings related to timeouts."""

    timeout_keep_alive: int = 5
    """Close Keep-Alive connections if no new data is received within this timeout. Default: 5."""

    timeout_graceful_shutdown: int = -1
    """Maximum number of seconds to wait for graceful shutdown. After this timeout, the server will start terminating
    requests. Default: -1, which implies not set."""

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornTimeoutsConfigSection to a dictionary suitable for Uvicorn configuration."""
        uvicorn_config_dict = asdict(self)
        if self.timeout_graceful_shutdown == -1:
            uvicorn_config_dict.pop("timeout_graceful_shutdown")
        return uvicorn_config_dict


@attributes_doc
@dataclass(frozen=True)
class UvicornConfigSection(ConfigSectionBase):  # pylint: disable=too-many-instance-attributes
    """ConfigSection for uvicorn."""

    application: UvicornApplicationConfigSection = UvicornApplicationConfigSection()
    socket_binding: UvicornSocketBindingConfigSection = UvicornSocketBindingConfigSection()
    development: UvicornDevelopmentConfigSection = UvicornDevelopmentConfigSection()
    production: UvicornProductionConfigSection = UvicornProductionConfigSection()
    logging: UvicornLoggingConfigSection = UvicornLoggingConfigSection()
    implementation: UvicornImplementationConfigSection = UvicornImplementationConfigSection()
    application_interface: UvicornApplicationInterfaceConfigSection = UvicornApplicationInterfaceConfigSection()
    http: UvicornHTTPConfigSection = UvicornHTTPConfigSection()
    https: UvicornHTTPSConfigSection = UvicornHTTPSConfigSection()
    resource_limits: UvicornResourceLimitsConfigSection = UvicornResourceLimitsConfigSection()
    timeouts: UvicornTimeoutsConfigSection = UvicornTimeoutsConfigSection()

    def as_uvicorn_config_dict(self) -> dict[str, Any]:
        """Converts UvicornConfigSection to a dictionary suitable for Uvicorn configuration."""

        uvicorn_config_dict = (
            self.application.as_uvicorn_config_dict()
            | self.socket_binding.as_uvicorn_config_dict()
            | self.development.as_uvicorn_config_dict()
            | self.production.as_uvicorn_config_dict()
            | self.logging.as_uvicorn_config_dict()
            | self.implementation.as_uvicorn_config_dict()
            | self.application_interface.as_uvicorn_config_dict()
            | self.http.as_uvicorn_config_dict()
            | self.https.as_uvicorn_config_dict()
            | self.resource_limits.as_uvicorn_config_dict()
            | self.timeouts.as_uvicorn_config_dict()
        )
        return uvicorn_config_dict
