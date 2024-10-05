def parse_cookies_from_file(file_path):
    cookies = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if '=' in line: 
                name, value = line.split('=', 1)
                cookies[name.strip()] = value.strip()
            else:
                print(f"Skipping malformed line: {line}")
    return cookies

def get_cookies_content_with_semicolon(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    content_with_semicolon = ''.join([line.strip() + ';' for line in content])
    return content_with_semicolon

