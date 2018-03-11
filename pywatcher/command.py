# coding: utf-8
import argparse
import time
from watchdog.observers import Observer

from pywatcher import PyWatcher

from logging import getLogger, Formatter, StreamHandler, DEBUG
logger = getLogger(__name__)
formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.setLevel(DEBUG)
logger.addHandler(handler)


COMMAND_DESCRIPTION = """\
-----------------------------------------------------------------------
PyWatcher:

monitor file and reload process. like gulp watch

e.g:

pywatcher -t .  -c 'ping localhost'
-> if some file on current dir changed, restart process 'ping localhost'.

-----------------------------------------------------------------------
"""


def init():
    """
    arguments.
    """
    parser = argparse.ArgumentParser(description=COMMAND_DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-t',
        '--target-dir',
        type=str,
        required=True,
        dest='target_dir_path',
        help='target directory for watching.'
    )

    parser.add_argument(
        '-c',
        '--command',
        type=str,
        required=True,
        dest='target_command_str',
        help='target command. this command execute and restart when file changed.'
    )

    parser.add_argument(
        '-s',
        '--reload-interval-seconds',
        type=int,
        required=False,
        default=5,
        dest='reload_threshold_seconds',
        help='reload threshold seconds.'
    )

    parser.add_argument(
        '--disable-capture-stdout',
        required=False,
        action='store_true',
        default=False,
        dest='is_disable_capture_stdout',
        help='is_disable_capture_stdout'
    )

    return parser.parse_args()


def main_action(target_dir, command, reload_threshold_seconds, is_disable_capture_stdout):
    while True:
        event_handler = PyWatcher(
            process_command=command,
            reload_threshold_seconds=reload_threshold_seconds,
            is_capture_subprocess_output=not is_disable_capture_stdout,
            logger=logger
        )
        observer = Observer()
        observer.schedule(event_handler, target_dir, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(0.3)
        except KeyboardInterrupt:
            logger.info('stop watch request received.')
            observer.stop()
            logger.info('stop watch.')
            break
        observer.join()


def main():
    args = init()
    main_action(
        target_dir=args.target_dir_path,
        command=args.target_command_str,
        reload_threshold_seconds=args.reload_threshold_seconds,
        is_disable_capture_stdout=args.is_disable_capture_stdout
    )


if __name__ in '__main__':
    main()