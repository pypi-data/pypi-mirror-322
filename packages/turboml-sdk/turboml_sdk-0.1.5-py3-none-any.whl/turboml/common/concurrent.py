from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

_tb_use_multiprocessing = True


def use_multiprocessing(enable: bool):
    global _tb_use_multiprocessing
    _tb_use_multiprocessing = enable


def multiprocessing_enabled() -> bool:
    global _tb_use_multiprocessing
    return _tb_use_multiprocessing


def get_executor_pool_class() -> type[ProcessPoolExecutor | ThreadPoolExecutor]:
    return ProcessPoolExecutor if multiprocessing_enabled() else ThreadPoolExecutor
