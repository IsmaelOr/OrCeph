def rellenarpixeles(x1,y1,x2,y2):
    for i in range(x1-4, x2+5):
        for j in range (y1-4, y2+5):
            if(j == 4):
                print(f'({i,j})')
            else:
                print(f'{i,j}', end="")

rellenarpixeles(1403,220,1403,302)