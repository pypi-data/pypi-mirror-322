import time

def count_time():
    start = time.perf_counter()
    end = time.perf_counter()
    
    
    execution_time = end - start
    
    hours = execution_time // 3600
    minutes = (execution_time % 3600) // 60
    seconds = execution_time % 60
    
    formatted_time = f"{hours:02}: {minutes:02}: {seconds:02}"
    print(f"Execution time: {formatted_time}")