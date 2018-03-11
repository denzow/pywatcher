# coding: utf-8
import threading
import datetime
import subprocess

from watchdog.events import FileSystemEventHandler
from logging import getLogger
default_logger = getLogger(__name__)


class PyWatcher(FileSystemEventHandler):

    def __init__(self, process_command, reload_threshold_seconds, is_capture_subprocess_output, logger=None):
        """
        :param str process_command: process command string
        :param int reload_threshold_seconds: reload min threshold seconds.
        :param bool is_capture_subprocess_output: capture subprocess output flag.
        """
        super().__init__()
        self.process_command = process_command
        self.reload_threshold_seconds = reload_threshold_seconds
        self.is_capture_subprocess_output = is_capture_subprocess_output
        self.logger = logger or default_logger
        self.process = self._run_sub_process()
        self.reload_time = datetime.datetime.now()

    def _run_sub_process(self):
        """
        execute child process
        :return:
        """
        self.logger.info('[start process]: {}'.format(self.process_command))
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
            self.logger.info('[reload process]: {}'.format(self.process_command))
            self.process.stdout.close()
            self.process.terminate()
            self.process = self._run_sub_process()
            self.reload_time = datetime.datetime.now()

    def _capture_subprocess_stdout(self, process):
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
                self.logger.debug('[subprocess_output]: {}'.format(output))

        except ValueError:
            pass

    def on_created(self, event):
        self._reload_sub_process()

    def on_modified(self, event):
        self._reload_sub_process()

    def on_deleted(self, event):
        self._reload_sub_process()

