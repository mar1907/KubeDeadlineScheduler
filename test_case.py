test_array = [(0,4,18), (2,12,27), (15,4,20), (1,12,18), (8,9,10), (12,4,4), (8,6,12), (18,8,18), (7,9,27), (18,4,9), (20,5,12), (20,11,19), (19,7,19),
              (2,10,12), (1,8,8), (16,4,24), (16,10,21), (1,5,22), (14,6,19), (4,3,10), (6,11,12), (3,8,24), (7,6,10), (16,9,15), (1,10,28), (15,2,5),
              (3,3,12), (15,4,15), (10,9,11), (5,11,19), (5,7,20), (6,4,15), (17,10,19), (17,6,13), (4,7,21), (12,7,19), (13,12,28), (9,12,24), (20,5,22),
              (8,11,17), (7,5,10), (18,7,23), (19,12,22), (18,10,28), (14,8,8), (5,10,10), (6,12,14), (13,11,21), (13,3,10), (17,5,21), (4,8,27), (18,3,14),
              (6,4,6), (1,3,12), (7,2,13), (7,10,14), (15,6,16), (20,7,13), (7,11,13), (5,8,17), (9,3,22), (4,4,4), (19,6,23), (17,8,24), (1,3,12), (13,10,10),
              (15,12,25), (19,8,23), (4,3,22), (4,3,13), (0,6,16), (7,12,31), (2,6,22), (19,10,25), (11,5,10), (13,12,31), (20,2,7), (10,9,21), (8,6,16),
              (15,5,5), (4,11,14), (7,5,18), (0,3,8), (16,11,27), (9,8,9), (20,10,11), (9,11,19), (14,4,8), (12,9,20), (11,11,20), (0,4,24), (6,9,28),
              (5,2,16), (9,2,9), (12,8,16), (2,6,24), (16,2,4), (10,9,18), (8,8,22), (10,5,7)]

def generate():
    import random
    for i in range(100):
        sleep = random.randint(0, 20)
        runtime = random.randint(2, 12)
        deadline = runtime + random.randint(0, 20)
        print("(%d,%d,%d)," % (sleep, runtime, deadline)),