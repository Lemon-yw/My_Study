def search(lines, pattern, history=5):
    previous_lines = []
    for line in lines:
        if len(previous_lines) < history and pattern in line:
            previous_lines.append(line)
    return previous_lines


if __name__ == '__main__':
    with open('log.txt', 'r') as f:
        # 去掉换行符
        f = f.read().splitlines()
        print(search(f, 'response'))
