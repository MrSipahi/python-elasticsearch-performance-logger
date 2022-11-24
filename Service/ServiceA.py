
from random import randint
from time import sleep

from Utilities.PerformanceLogger import PerformanceLogger

class ServiceA:

    PerformanceLogger = PerformanceLogger("performance_service_a")

    def __init__(self) -> None:
        pass

    def start(self):
        print("Service A started")
        while True:
            self.function1()
            self.function2()
            self.function3()

            self.PerformanceLogger.finishBenchmark()

    @PerformanceLogger._benchmark
    def function1(self):
        sleep((randint(1, 10) / 10) * 2)
        return True    

    @PerformanceLogger._benchmark
    def function2(self):
        sleep(randint(0, 1) / 10)
        return True

    @PerformanceLogger._benchmark
    def function3(self):
        sleep(randint(0, 1) / 10)
        return True  
    