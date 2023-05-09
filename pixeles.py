def rellenarpixeles(x,y):
    for i in range(x-4, y+5):
        for j in range (-4, 5):
            if(j == 4):
                print(f'({i,j})')
            else:
                print(f'{i,j}', end="")

rellenarpixeles(0,0)