from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional
from enum import Enum
from threading import Thread
import time
import copy

class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass

    @abstractmethod
    def update_status(self, Status):
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _status = None
    _handlers_list = None
    _name = None
    _request = None

    def handle(self):
        self.update_status(HandlerStatus.NOT_AVAILABLE)
        print('>>> ' + self._name + ' is handling ' + self._request.get_request_id() + ' which is a '+ str(self._request.get_request_duration())  + ' seconds meeting... \n')
        time.sleep(self._request.get_request_duration())
        self._request._queue.remove_request(self._request)
        self.update_status(HandlerStatus.AVAILABLE)
        print('*** ' + self._name + ' is available again \n')

    def update_status(self, status):
        # in order to avoid the error "same Thread cannot be started twice"
        # We need to make a copy of the handler, then remove the initial handler from the _handlers_list and then append the copied handler.
        if status == HandlerStatus.AVAILABLE:
            new_handler = None
            if type(self) is SE:
                new_handler = SE(HandlerStatus.AVAILABLE, self._name)
            if isinstance(self, type(Lead_SE)):
                Lead_SE.reset_instance()
                new_handler = Lead_SE.get_instance(HandlerStatus.AVAILABLE, self._name)
            if isinstance(self, type(SE_Manager)):
                SE_Manager.reset_instance()
                new_handler = SE_Manager.get_instance(HandlerStatus.AVAILABLE, self._name)

            #copied_handler._status = Status.AVAILABLE
            handler_name = self._name
            for i, o in enumerate(self._handlers_list):
                if o._name == handler_name:
                    del self._handlers_list[i]
                    if new_handler:
                        self._handlers_list.append(new_handler)
                    break
            return

        self._status = status
        
    @classmethod
    def set_handlers_list(cls, handlers_list):
        cls._handlers_list = handlers_list

    def set_request(self, request: Request):
        if request.get_status() == RequestStatus.AVAILABLE_TO_BE_PICKED:
            self._request = request
            self._request.set_status(RequestStatus.BEING_PROCESSED)


"""
All Concrete Handlers either handle a request or pass it to the next handler in
the chain.
"""
class HandlerStatus(Enum):
    AVAILABLE = "AVAILABLE"
    NOT_AVAILABLE = "NOT AVAILABLE"

class RequestStatus(Enum):
    BEING_PROCESSED = "BEING_PROCESSED"
    AVAILABLE_TO_BE_PICKED = "AVAILABLE_TO_BE_PICKED"

class Lead_SE(AbstractHandler, Thread):
    _instance = None

    def __init__(self) -> Logger:
        raise RuntimeError('Call get_instance() instead')

    @classmethod
    def get_instance(cls, status: HandlerStatus = None, name = None):
        if cls._instance is None:
            Thread.__init__(cls)
            cls._status = status
            cls._name = name
            cls._instance = cls.__new__(cls)
            #print ('Lead_SE ' + cls._name + ' created')
        return cls._instance

    @classmethod
    def reset_instance(cls):
        cls._instance = None
        #print('resetting instance')

    def run(self):
        self.handle()   

class SE_Manager(AbstractHandler, Thread):
    _instance = None

    def __init__(self) -> Logger:
        raise RuntimeError('Call get_instance() instead')   

    @classmethod
    def get_instance(cls, status: HandlerStatus = None, name = None):
        if cls._instance is None:
            Thread.__init__(cls)
            cls._status = status
            cls._name = name
            cls._request = None
            cls._instance = cls.__new__(cls)
            #print ('SE_Manager ' + cls._name + ' created')
            # Put any initialization here.
        return cls._instance

    @classmethod
    def reset_instance(cls):
        cls._instance = None
        #print('resetting instance')
        
    def run(self):
        self.handle()

class SE(AbstractHandler, Thread):

    def __init__(self, status: HandlerStatus = None, name = None):
        Thread.__init__(self)
        self._status = status
        self._name = name
        #print ('SE ' + self.name + ' created')

    def get_status():
        return self._status

    def get_name():
        return self._name

    def run(self):
        self.handle()

class Request():
    _queue = None
    _status = RequestStatus.AVAILABLE_TO_BE_PICKED
    def __init__(self, request_id: str, request_duration: int, status: RequestStatus):
        self._request_id = request_id
        self._request_duration = request_duration
        self._status = status
        
    def get_request_id(self):
        return self._request_id

    def get_request_duration(self):
        return self._request_duration
    @classmethod
    def set_queue(cls, queue: RequestsQueue):
        cls._queue = queue

    def set_status(self, status: RequestStatus):
        self._status = status

    def get_status(self):
        return self._status

class RequestsQueue():
    _requests_queue = []
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def get_instance(cls, requests_queue):
        if cls._instance is None:
            cls._requests_queue = requests_queue
            cls._instance = cls.__new__(cls, cls._requests_queue)
        return cls._instance
    
    def add_request(self, request: Request):
        self._requests_queue.append(request)

    @classmethod
    def remove_request(cls, request: Request):
        request_id = request.get_request_id()
        for i, o in enumerate(cls._requests_queue):
            if o.get_request_id() == request_id:
                del cls._requests_queue[i]
                print('--- ' + request.get_request_id() + ' finished and got removed from queue \n')
                break

    def print_requests(self):
        if (len(self._requests_queue)==0):
            print('All requests got processed. Queue is empty!!')
        else:
            print('\n------------------------------------------')
            print('THE INITIAL LIST OF REQUESTS IN THE QUEUE:')
            print('------------------------------------------')
            for req in self._requests_queue:
                print(req.get_request_id() + ' --> ' + str(req.get_request_duration()) + ' seconds of processing')

    def print_sum_requests_duration(self):
        print('\n--------------------------------------')
        print('SUM DURATION OF ALL REQUESTS MEETINGS:')
        print('--------------------------------------')
        sum_duration = 0
        for req in self._requests_queue:
            sum_duration = sum_duration + req.get_request_duration()
        print('TOTAL_DURATION = ' + str(sum_duration) + '\n')

if __name__ == "__main__":

    def print_handlers(handlers):
        print('-----------------------')
        print('THE LIST OF PROCESSORS:')
        print('-----------------------')
        for handler in handlers:
            print(handler._name)

    def get_available_handler(handlers_list):
        # first check for SE availibility
        for handler in handlers_list:
            if handler._name.startswith('SE'):
                if handler._status == HandlerStatus.AVAILABLE:
                    return handler
        # then check for lead
        for handler in handlers_list:
            if handler._name.startswith('The_Only_Lead_SE'):
                if handler._status == HandlerStatus.AVAILABLE:
                    return handler
        # then check for lead
        for handler in handlers_list:
            if handler._name.startswith('The_Only_SE_Manager'):
                if handler._status == HandlerStatus.AVAILABLE:
                    return handler
        return None

    def process_queue(requestsQueue):
        global handlers_list
        global SE_Manager
        global Lead_SE
        global threads
        waiting = False 
        for req in requestsQueue._requests_queue:
            if req.get_status() == RequestStatus.AVAILABLE_TO_BE_PICKED:
                #print('\nIncoming request ' +  req.get_request_id() +'. Determining processor...\n')
                selected_handler = get_available_handler(handlers_list)
                if selected_handler:
                    selected_handler.set_request(req)
                    threads.append(selected_handler)
                    selected_handler.start()
                else:
                    if not waiting:
                        print('!!! No available handlers at the moment. Waiting for the next availibility...')
                        waiting = True


    ###### INITIALIZE HANDLERS STATUS ######
    SE1 = SE(HandlerStatus.AVAILABLE, 'SE1')
    SE2 = SE(HandlerStatus.AVAILABLE, 'SE2')
    SE3 = SE(HandlerStatus.AVAILABLE, 'SE3')
    Lead_SE = Lead_SE.get_instance(HandlerStatus.AVAILABLE, 'The_Only_Lead_SE')
    SE_Manager = SE_Manager.get_instance(HandlerStatus.AVAILABLE, 'The_Only_SE_Manager')
    handlers_list = [SE1, SE2, SE3, Lead_SE, SE_Manager]
    AbstractHandler.set_handlers_list(handlers_list)
    print_handlers(handlers_list)
    threads = []

    ###### INITIALIZE REQUESTS ######
    request1 = Request('REQ1', 10, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request2 = Request('REQ2', 10, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request3 = Request('REQ3', 10, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request4 = Request('REQ4', 2, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request5 = Request('REQ5', 2, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request6 = Request('REQ6', 2, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request7 = Request('REQ7', 5, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request8 = Request('REQ8', 5, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request9 = Request('REQ9', 5, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request10 = Request('REQ10', 1, RequestStatus.AVAILABLE_TO_BE_PICKED)
    request11 = Request('REQ11', 1, RequestStatus.AVAILABLE_TO_BE_PICKED)

    ###### ASSIGN REQUESTS TO QUEUE ######
    requests_list = [request1, request2, request3, request4, request5, request6, request7, request8, request9, request10, request11]
    requestsQueue = RequestsQueue.get_instance(requests_list)
    request1.set_queue(requestsQueue)
    requestsQueue.print_requests()
    requestsQueue.print_sum_requests_duration()

    ###### START PROCESSING QUEUE #####
    print('\n------------------------------')
    print('PROCESSING OF REQUESTS STARTED')
    print('------------------------------')
    while len(requestsQueue._requests_queue) > 0:
        # check first if there are requests in queue with status AVAILABLE
        available_request = False
        available_handler = False
        for request in requestsQueue._requests_queue:
            if request.get_status() == RequestStatus.AVAILABLE_TO_BE_PICKED:
                available_request = True
                break
        if available_request:
            for handler in AbstractHandler._handlers_list:
                if handler._status == HandlerStatus.AVAILABLE:
                    available_handler = True
                    break
        if available_request and available_handler:
            process_queue(requestsQueue)
    ####let the main thread wait for all threads####
    try:
        for x in threads:
            x.join()
    except:
        pass
    
    print('\nremaining requests to process:')
    requestsQueue.print_requests()
    print('\n----------------------')
    print('TOTAL PROCESSING TIME:')
    print('----------------------')
