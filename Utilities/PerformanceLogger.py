from time import time
import json
from datetime import datetime
from rich import print

import requests


class PerformanceLogger:

    def __init__(self, index_name):
        self.benchmark_total_time = {}  
        self.benchmark_total_time_list = []  
        self.benchmark_total_time_list_bulk_count = 1  

        self.elastic_url = "http://localhost:9200"
        self.index_name = index_name

    def _benchmark(self, func):
        def wrapper(*args, **kwargs):
            time_start = time()
            result = None

            try:
                result = func(*args, **kwargs)
            except Exception as ex:
                print(f'{func.__name__} Error -> {ex}')

            time_finish = time()

            time_delta = time_finish - time_start

            self.benchmark_total_time[func.__name__] = round(time_delta, 5)
            return result
        return wrapper

    def finishBenchmark(self):
        try:
            print(self.benchmark_total_time)
            self.benchmark_total_time["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03:00")
            self.benchmark_total_time_list.append(self.benchmark_total_time)
            if len(self.benchmark_total_time_list) >= self.benchmark_total_time_list_bulk_count:
                self.uploadBenchmarkToElastic()
                self.benchmark_total_time_list = []

            self.benchmark_total_time = {}
        except Exception as ex:
            print(f"PerformanceLogger.finishBenchmark() Error -> {ex}")

    def uploadBenchmarkToElastic(self):
        final_values = []
        for value in self.benchmark_total_time_list:
            destination_index = {"index": {}}
            final_values.append(destination_index)
            final_values.append(value)

        address = f"{self.elastic_url}/{self.index_name}/_bulk?pretty"

        serialized = '\n'.join([json.dumps(line) for line in final_values]) + '\n'

        response = requests.put(address, data=serialized, headers={"Content-Type": "application/x-ndjson"}, timeout=120)
        

        if response and response.status_code == 200:
            print(f"{len(self.benchmark_total_time_list)} işlemin benchmark süreleri ElasticSearch'e yüklendi.")
