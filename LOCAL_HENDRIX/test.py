import numpy as np

def rollavg_direct(a,n=3): 
    assert n%2==1
    b = a*0.0
    for i in range(len(a)) :
        b[i]=a[max(i-n//2,0):min(i+n//2+1,len(a))].mean()
    return b

arr = np.array([0,1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1,0])

print(arr)

print(rollavg_direct(arr))