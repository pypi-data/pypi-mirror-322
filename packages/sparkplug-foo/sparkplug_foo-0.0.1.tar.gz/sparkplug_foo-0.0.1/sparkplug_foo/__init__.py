# python
import logging


log = logging.getLogger(__name__)


def hello_foo():
    msg = "Hello Foo!"
    print(msg)
    log.debug(msg)

