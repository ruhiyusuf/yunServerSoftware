#Scale controller x,y values in range(-1,1) to motor value from (1000, 2000)
#Direction switch at 1500
#

def transformXY(x, y):
    return 0, 0


import time
t1 = time.time()
print(t1)
time.sleep(5)
t2 = time.time()
print(t2 - t1)