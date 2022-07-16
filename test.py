import random

def generate_random_rgb():
   rgb = set()
   r = random.randint(0, 255)
   g = random.randint(0, 255)
   b = random.randint(0, 255)
   rgb_e = r, g, b
 
   print('A Random color is :', rgb_e)
   rgb.add(rgb_e)
   print(rgb)
   if rgb_e in rgb:
     print("It is in set")


generate_random_rgb()


my_list = []

my_list.append(1)

print(my_list)

dictionary = dict()

dictionary[1] = False
dictionary[2] = True
dictionary[3] = True
dictionary[4] = False
dictionary[5] = True

print(dictionary)

