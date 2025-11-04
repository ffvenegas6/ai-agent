# from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

# response = get_files_info("calculator", ".")
# print(response)
# response = get_files_info("calculator", "pkg")
# print(response)
# response = get_files_info("calculator", "/bin")
# print(response)
# response = get_files_info("calculator", "../")
# print(response)

# response = get_file_content("calculator", "lorem.txt")
# print(response)

# response = get_file_content("calculator", "main.py")
# print(response)
# response = get_file_content("calculator", "pkg/calculator.py")
# print(response)
# response = get_file_content("calculator", "/bin/cat")
# print(response)
# response = get_file_content("calculator", "pkg/does_not_exist.py")
# print(response)

response = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(response)
response = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(response)
response = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(response)
