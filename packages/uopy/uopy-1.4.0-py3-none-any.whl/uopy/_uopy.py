# Copyright 2020 - 2024 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#
import threading
from ._config import config, POOLING_ON, IDLE_REMOVE_INTERVAL
from ._logger import get_logger
from ._pool import Pool
from ._session import Session
from ._utils import build_connect_config, build_pooling_config, make_pool_key
from importlib.metadata import version

_logger = get_logger(__name__)

_logger.info(config.connection)
_logger.info(config.pooling)
_logger.info(config.ssl_auth)
_logger.info(config.logging)

_pools: dict[str, Pool] = {}
_pooling_on = config.pooling[POOLING_ON]
_lock = threading.RLock()

""" Use uopy.__version__ to get the uopy version """
__version__ = version("uopy")


def _remove_idle_connections():
    _logger.debug("Enter")
    global _pooling_on
    with _lock:
        try:
            for p in _pools.values():
                p.remove_idle_connections()
        finally:
            if _pooling_on:
                timer = threading.Timer(
                    config.pooling[IDLE_REMOVE_INTERVAL], _remove_idle_connections
                )
                timer.daemon = True
                timer.start()
                _logger.debug("Start timer")
            else:
                _logger.debug("Cancel timer")
    _logger.debug("Exit")


def close_all_cp_sessions():
    _logger.debug("Enter: close_all_cp_sessions")
    if not _pools:
        _logger.debug("Exit: _pools empty")
        return
    with _lock:
        if _pooling_on:
            for pool in _pools.values():
                pool.close_all_connections()
                _logger.debug(
                    "Disconnect Pool: Server = {}, User Id = {}, Account = {}".format(
                        pool.get_server(), pool.get_userid(), pool.get_account()
                    )
                )
    _logger.debug("Exit: close_all_cp_sessions")


def create_timer(f):
    def wrapper():
        with _lock:
            if not wrapper.hasrun:
                wrapper.hasrun = True
                return f()

    wrapper.hasrun = False
    return wrapper


wrapper = create_timer(_remove_idle_connections)
if _pooling_on:
    wrapper()


def connect(**kwargs):
    """Open a connection to an MV Database.

    Args:
        kwargs: connection configuration keyword parameters:  host, port, user, password, account, service, timeout,
                encoding, ssl, min_pool_size, max_pool_size.

                1. only user and password are required, the rest have default values in uopy.config.connection.

                2. if connection pooling is turned on and connect() is called for the first time to open a connection
                to the database server, a connection pool will be created for the same host, account, user and password
                that are passed in. If min_pool_size and/or max_pool_size are passed in as well, they will be used
                instead of the default values in the uopy.config.pooling section to set the minimum and maximum pool
                sizes. Note that once a connection pool is created, its min_pool_size and max_pool_size cannot be
                changed. This means that the min_pool_size and max_pool_size parameters are ignored on subsequent calls
                to connect() for the same pool.

    Returns:
        A Session object: either newly established or straight from a connection pool.

    Raises:
        UOError, ValueError

    Examples:
        >>> session = uopy.connect(user = 'test', password ='test')

        >>> session = uopy.connect(host ='localhost', user = 'test', password ='test', account = 'HS.SALES',
                    service=uopy.UV_SERVICE, port=31438)

        >>> config = {
                'user': 'test',
                'password': 'test',
                'service': 'udcs',
                'account': 'demo',
                'encoding': 'GB18030',
                'ssl': True
            }
        >>> session = uopy.connect(**config)

    """
    global _pooling_on
    config.update(kwargs)
    connect_config = build_connect_config(kwargs)
    pooling_config = build_pooling_config(kwargs)

    _pooling_on = pooling_config.get("pooling_on")
    if _pooling_on:
        pool_key = make_pool_key(connect_config)
        if not wrapper.hasrun:
            wrapper()
        with _lock:
            pool = _pools.get(pool_key)
            if not pool:
                pool = Pool(connect_config, pooling_config)
                _pools[pool_key] = pool

        return pool.get()
    else:
        session = Session(connect_config)
        session.connect()
        return session
