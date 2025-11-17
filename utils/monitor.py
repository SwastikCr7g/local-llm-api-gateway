import psutil

def get_system_resource_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    return {"cpu_percent": cpu_percent, "memory_percent": mem_percent}
