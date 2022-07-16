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

