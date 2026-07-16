import stdio
import is_empty
total ,count = 0 ,0
while not is_empty:
    total += stdio.readfloat()
    count += 1
print("Average : %f" %(total/count))