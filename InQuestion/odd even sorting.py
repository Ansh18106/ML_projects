n = int (input())
li = []
for i in range(n):
    t = int(input())
    li.append(t)


odd = []
even = []
for i in range(n):
    if (li[i]%2):
        odd.append(li[i])
    else:
        even.append(li[i])

odd.sort()
even.sort()
print (odd)
print (even)