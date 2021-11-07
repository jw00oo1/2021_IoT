def test_f(i):
    if 'x' not in globals():
        global x
        x = []
        #print(globals())
    else:
        x = globals()['x']
        x.append(i)

threshold = 3
def init_var(var1, var2 = None):
    if abs(var1) < threshold:
        var1 = 0
    if var2 and abs(var2) < threshold:
        var2 = 0
    print("in function : {} {}".format(var1, var2))
    return (var1, var2) if var2 is not None else var1
if __name__=='__main__':
    for i in range(5):
        test_f(i)
        #print(x)
    a = 2.1
    b = 1
    c = 5.8
    a, b = init_var(a,b)
    c = init_var(c)
    print(a, b, c)