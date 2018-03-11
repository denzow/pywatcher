# -*- coding: utf-8 -*-
import argparse
import threading
import datetime
import time
import subprocess

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

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


class PyWatcher(FileSystemEventHandler):

    def __init__(self, process_command, reload_threshold_seconds, is_capture_subprocess_output):
        """
        :param str process_command: process command string
        :param int reload_threshold_seconds: reload min threshold seconds.
        :param bool is_capture_subprocess_output: capture subprocess output flag.
        """
        super().__init__()
        self.process_command = process_command
        self.reload_threshold_seconds = reload_threshold_seconds
        self.is_capture_subprocess_output = is_capture_subprocess_output

        self.process = self._run_sub_process()
        self.reload_time = datetime.datetime.now()

    def _run_sub_process(self):
        """
        execute child process
        :return:
        """
        logger.info('[start process]: {}'.format(self.process_command))
        process = subprocess.Popen(
            self.process_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
            close_fds=True
        )
        # run subprocess stream watcher thread.
        if self.is_capture_subprocess_output:
            read_thread = threading.Thread(target=self._capture_subprocess_stdout, args=(process,), daemon=True)
            read_thread.start()
        return process

    def _reload_sub_process(self):
        """
        if last reload time is too old(over reload_threshold_seconds)
        reload subprocess. terminate and restart.
        :return:
        """
        if (datetime.datetime.now() - self.reload_time).seconds > self.reload_threshold_seconds:
            logger.info('[reload process]: {}'.format(self.process_command))
            self.process.stdout.close()
            self.process.terminate()
            self.process = self._run_sub_process()
            self.reload_time = datetime.datetime.now()

    @staticmethod
    def _capture_subprocess_stdout(process):
        """
        capture subprocess stdout function. this function execute via thread.
        :param subprocess.Popen process: target process.
        :return:
        """
        try:
            for line in iter(process.stdout.readline, ''):
                if line and hasattr(line, 'decode'):
                    output = line.decode('utf-8').rstrip()
                else:
                    output = line
                logger.debug('[subprocess_output]: {}'.format(output))

        except ValueError:
            pass

    def on_created(self, event):
        self._reload_sub_process()

    def on_modified(self, event):
        self._reload_sub_process()

    def on_deleted(self, event):
        self._reload_sub_process()


def init():
    """
    引数処理
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
        '-i',
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


def main(target_dir, command, reload_threshold_seconds, is_disable_capture_stdout):
    while True:
        event_handler = PyWatcher(
            process_command=command,
            reload_threshold_seconds=reload_threshold_seconds,
            is_capture_subprocess_output=not is_disable_capture_stdout
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


if __name__ in '__main__':
    args = init()
    main(
        target_dir=args.target_dir_path,
        command=args.target_command_str,
        reload_threshold_seconds=args.reload_threshold_seconds,
        is_disable_capture_stdout=args.is_disable_capture_stdout
    )
