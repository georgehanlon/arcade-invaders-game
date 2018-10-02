import pickle
lst = []
t1 = (20, 'George')
t2 = (50, 'Fred')
t3 = (35, 'Lexa')
t4 = (10, 'James')
t5 = (9, 'Amy')
t6 = (2, 'Greg')
lst.append(t1)
lst.append(t2)
lst.append(t3)
lst.append(t4)
lst.append(t5)
lst.append(t6)

#"""
f = open("highscore.dat", "rb")
v = pickle.load(f)
print(v)
f.close()
#"""


"""
f = open("highscore.dat", "wb")
pickle.dump(lst, f)
f.close()

"""
