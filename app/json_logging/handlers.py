import json
import gzip
import time

from logging import StreamHandler, DEBUG
from logging.handlers import RotatingFileHandler
from . import settings
from .constants import LogTypes
from .log_object import ErrorLogObject, SqlLogObject


def message_from_record(record):
    if isinstance(record.msg, dict) or isinstance(record.msg, str):
        if settings.DEBUG:
            message = record.msg
        else:
            message = dict(raw=record.msg)
    elif isinstance(record.msg, Exception):
        message = ErrorLogObject.format_exception(record.msg)
    else:
        try:
            message = record.msg.to_dict
        except AttributeError:
            return dict(raw='Unable to parse LogObject.')
    return message


class DefaultFileHandler(RotatingFileHandler):
    def emit(self, record):
        if isinstance(record.msg, SqlLogObject):
            return
        super(DefaultFileHandler, self).emit(record)

    def format(self, record):
        created = int(record.created)
        message = message_from_record(record)
        return json.dumps({record.levelname: {created: message}}, sort_keys=True)

    def rotation_filename(self, default_name):
        return f'{default_name}-{time.strftime("%Y%m%d")}.gz'

    def rotate(self, source, dest):
        with open(source, 'rb+') as fh_in:
            with gzip.open(dest, 'wb') as fh_out:
                fh_out.writelines(fh_in)
            fh_in.seek(0)
            fh_in.truncate()


class DebugFileHandler(DefaultFileHandler):
    def emit(self, record):
        if record.levelno != DEBUG:
            return
        return super(DebugFileHandler, self).emit(record)


# class ConsoleHandler(StreamHandler):
#     def emit(self, record):
#         return super(ConsoleHandler, self).emit(record)
#
#     def format(self, record):
#         if isinstance(record.msg, LogObject) or isinstance(record.msg, SqlLogObject):
#             created = int(record.created)
#             message = {record.levelname: {datetime.datetime.fromtimestamp(created).isoformat(): record.msg.to_dict}}
#             return json.dumps(message, sort_keys=True, indent=settings.INDENT_CONSOLE_LOG)
#         elif isinstance(record.msg, ErrorLogObject):
#             return str(record.msg)
#         elif isinstance(record.msg, dict):
#             created = int(record.created)
#             message = {record.levelname: {created: record.msg}}
#             return json.dumps(message, sort_keys=True, indent=settings.INDENT_CONSOLE_LOG)
#         else:
#             return super(ConsoleHandler, self).format(record)
class ConsoleHandler(StreamHandler):
    @staticmethod
    def format_message(record):
        msg = {
            'datetime': int(time.time()),
            'source': record.name,
            'level': record.levelname,
        }
        if type(record.msg) == str:
            msg['type'] = LogTypes.TYPE_MESSAGE
            msg['message'] = record.msg
        else:
            msg['context'] = record.msg
            if type(record.args) == dict:
                msg['name'] = record.args.get('event_name', None)
                msg['chain'] = record.args.get('chain', None)

        return json.dumps(msg, sort_keys=True, separators=(',', ':', ))

    def emit(self, record):
        try:
            record.msg = self.format_message(record)
        finally:
            pass
        super(ConsoleHandler, self).emit(record)


class SQLFileHandler(RotatingFileHandler):
    def emit(self, record):
        if not isinstance(record.msg, SqlLogObject):
            return
        super(SQLFileHandler, self).emit(record)

    def format(self, record):
        created = int(record.created)
        message = {record.levelname: {created: record.msg.to_dict}}
        return json.dumps(message, sort_keys=True)

    def rotation_filename(self, default_name):
        return f'{default_name}-{time.strftime("%Y%m%d")}.gz'

    def rotate(self, source, dest):
        with open(source, 'rb+') as fh_in:
            with gzip.open(dest, 'wb') as fh_out:
                fh_out.writelines(fh_in)
            fh_in.seek(0)
            fh_in.truncate()
