x=int(input('Hints: '))
z=input('Code: ')
q=str('abcdefghijklmnopqrstuvwxyz')
p=str('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
r=''
for i in z:
    if i.isalpha():
        if i.islower():
            j=q.index(i)
            if x>=0:
                if j+x>25:
                    j=j+x-26
                else:
                    j+=x
                r+=q[j]
            else:
                if j+x<0:
                    j=j+x+26
                else:
                    j+=x
                r+=q[j]
        if i.isupper():
            r+=i
    else:
        r+=i
print(r)

