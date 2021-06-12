from src.utility import file_management


data = file_management.read_summary("ProjectMetrics")

print(type(data))