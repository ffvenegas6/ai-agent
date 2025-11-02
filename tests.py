from functions.get_files_info import get_files_info


response = get_files_info("calculator", ".")
print(response)
response = get_files_info("calculator", "pkg")
print(response)
response = get_files_info("calculator", "/bin")
print(response)
response = get_files_info("calculator", "../")
print(response)
