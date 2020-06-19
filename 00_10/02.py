# coding: utf-8
target = 'Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics.'
result = []

words = target.split(' ')
for word in words:
    count = 0
    for char in word:
        if char.isalpha():
            count += 1
    result.append(count)

print(result)
