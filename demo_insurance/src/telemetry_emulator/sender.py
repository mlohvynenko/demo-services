#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

import logging
import os
import signal
import socket
import sys
import time
from threading import Thread

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telemetry_emulator.config import (
    CONNECTION_RETRY_DELAY, EMULATOR_UPDATE_TIME, SENDING_INTERVAL, SEND_TO_ADDRESS, CONTROL_API_ADDRESS
)
from telemetry_emulator.control_api import ControlApiSever
from telemetry_emulator.emulator import VertexPool, Emulator
from telemetry.converter import Converter

logger = logging.getLogger(__name__)


def signal_handler(signum, frame):
    if signum == 15:
        control_server.shutdown()
        print('got SIGTERM')
        sys.exit(0)


def sending_loop(emulator):
    while True:
        sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            _sending_loop(sc, emulator)
        except ConnectionError as ex:
            logger.error(f"Exception: {ex}")
        except socket.gaierror as ex:
            logger.error(f"can't resolve address '{SEND_TO_ADDRESS}'")
        except Exception as ex:
            logger.exception("Unexpected exception during sending loop", exc_info=ex)
        finally:
            sc.close()
        time.sleep(CONNECTION_RETRY_DELAY)


def _sending_loop(sc, emulator):
    while True:
        emulator.update(EMULATOR_UPDATE_TIME)
        data = emulator.get_data()
        logger.debug(data)
        converted_data = Converter(data).to_bytes()
        logger.debug(converted_data)
        sc.sendto(converted_data, SEND_TO_ADDRESS)
        time.sleep(SENDING_INTERVAL)


if __name__ == '__main__':
    # logging setup
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    tl = logging.getLogger('control_api')
    tl.addHandler(logging.StreamHandler())
    tl.setLevel(logging.DEBUG)

    base_dir = os.path.dirname(__file__)
    vp = VertexPool(os.path.join(base_dir, 'map.json'))
    emulator = Emulator(vp)
    control_server = ControlApiSever(CONTROL_API_ADDRESS, emulator)

    signal.signal(signal.SIGTERM, signal_handler)

    server_thread = Thread(target=control_server.serve_forever, daemon=False)
    server_thread.start()
    try:
        sending_loop(emulator)
    except KeyboardInterrupt:
        logger.info("received Keyboard interrupt. shutting down")
