import copy


def dfs(features_group, cur_list):

    if len(cur_list) == len(features_group):
        print('-'.join(cur_list[::-1]))
        return

    for value in features_group[len(cur_list)]:
        tmp_list = copy.copy(cur_list)
        tmp_list.append(value)
        dfs(features_group, tmp_list)


if __name__ == '__main__':
    n = int(input())

    features_group = []
    for _ in range(n):
        features_group.append([s.strip() for s in input().split(' ')])
    dfs(features_group[::-1], [])

'''
3
man woman
coder gamer painter
phd
'''