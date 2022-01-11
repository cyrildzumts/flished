import logging
import logging.handlers
from copy import copy
from core.logger_tasks import async_logger_task



class AsyncLoggingHandler(logging.Handler):

    def __init__(self, level=logging.NOTSET, formatter=None, queue=None, exchange='log', routing_key='logger'):
        self.level = level
        self.formatter = formatter
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key
        super(AsyncLoggingHandler, self).__init__(level=level)
    
    def emit(self, record: logging.LogRecord) -> None:
        try:
            """if hasattr(record, 'request'):
                no_exc_record = copy(record)
                #del no_exc_record.exc_info
                #del no_exc_record.exc_text
                #del no_exc_record.request

                
                formatted = self.format(no_exc_record)
            else:"""
            formatted = self.format(record)
            
            # send formatted record to celery
            async_logger_task.apply_async(
                args=[formatted, self.level],
                queue=self.queue,
                routing_key=self.routing_key
            )
        except Exception as e:
            message = f"Exception while emit record {record} - Exception : {e}"
            async_logger_task.apply_async(
                args=[message, logging.WARNING],
                queue=self.queue,
                routing_key=self.routing_key
            )