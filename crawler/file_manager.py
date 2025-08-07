import os


def create_project_dir(directory: str):
    if not os.path.exists(directory):
        print(f'Creating directory: {directory}')
        os.makedirs(directory)


def create_data_files(project_name: str, base_url: str):
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, 'crawled.txt')
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


def write_file(path: str, data: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def append_to_file(path: str, data: str):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(data + '\n')


def delete_file_contents(path: str):
    open(path, 'w', encoding='utf-8').close()


def file_to_set(file_name: str) -> set:
    with open(file_name, 'r', encoding='utf-8') as f:
        return {line.strip() for line in f if line.strip()}


def set_to_file(links: set, file_name: str):
    with open(file_name, 'w', encoding='utf-8') as f:
        for link in sorted(links):
            f.write(link + '\n')
