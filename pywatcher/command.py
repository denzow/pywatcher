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
        '--reload-wait-seconds',
        type=int,
        required=False,
        default=0,
        dest='reload_wait_seconds',
        help='reload wait seconds.'
    )

    parser.add_argument(
        '--disable-capture-stdout',
        required=False,
        action='store_true',
        default=False,
        dest='is_disable_capture_stdout',
        help='is_disable_capture_stdout'
    )

    parser.add_argument(
        '-p',
        '--pattern',
        type=str,
        nargs='*',
        required=False,
        dest='target_pattern_list',
        help='target pattern for monitoring. default, all file match.',
        metavar='TARGET_PATTERN',
    )

    parser.add_argument(
        '--signal',
        required=False,
        type=str,
        default='TERM',
        choices=('TERM', 'KILL'),
        dest='reload_signal',
        help='reload_signal'
    )

    parser.add_argument(
        '--is-use-shell',
        required=False,
        action='store_true',
        default=False,
        dest='is_use_shell',
        help='use shell=True ?'
    )

    return parser.parse_args()


def main_action(target_dir, command, reload_threshold_seconds, watch_pattern_list,
                reload_wait_seconds, is_use_shell, reload_signal, is_disable_capture_stdout):
    while True:
        event_handler = PyWatcher(
            process_command=command,
            reload_threshold_seconds=reload_threshold_seconds,
            is_capture_subprocess_output=not is_disable_capture_stdout,
            pattern_list=watch_pattern_list,
            is_use_shell=is_use_shell,
            reload_signal=reload_signal,
            reload_wait_seconds=reload_wait_seconds,
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
        is_use_shell=args.is_use_shell,
        watch_pattern_list=args.target_pattern_list,
        reload_signal=args.reload_signal,
        reload_wait_seconds=args.reload_wait_seconds,
        is_disable_capture_stdout=args.is_disable_capture_stdout,
    )


if __name__ in '__main__':
    main()
