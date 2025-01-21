
from tkinter import N,W

def init(kws):
    cv = kws['canvas']
    w,h=kws['width'],kws['height']
    # 画X轴
    cv.create_line(0,h/2,w,h/2, width=10, fill='red')
    # 画Y轴
    cv.create_line(w/2,0,w/2,h, width=10, fill='blue')

    # 设置刻度间隔
    tick_interval = 200
    # X轴上的刻度
    for x in range(w//2,w,tick_interval):
        if int(x-w/2) == 0:
            continue
        cv.create_line(x,h/2-50,x,h/2+20, width=3, fill='red')  # 垂直线段
        cv.create_text(x,h/2-50, text=str(int(x-w/2)), font="Arial 8", anchor=N)  # 刻度值
    for x in range(w//2,0,-tick_interval):
        if int(x-w/2) == 0:
            continue
        cv.create_line(x,h/2-50,x,h/2+20, width=3, fill='red')  # 垂直线段
        cv.create_text(x,h/2-50, text=str(int(x-w/2)), font="Arial 8", anchor=N)  # 刻度值
    # Y轴上的刻度
    for y in range(h//2,h,tick_interval):
        cv.create_line(w/2-50,y,w/2+20,y, width=3, fill='blue')  # 垂直线段
        cv.create_text(w/2-50,y, text=str(-int(y-h/2)), font="Arial 8", anchor=N)  # 刻度值
    for y in range(h//2,0,-tick_interval):
        cv.create_line(w/2-50,y,w/2+20,y, width=3, fill='blue')  # 垂直线段
        cv.create_text(w/2-50,y, text=str(-int(y-h/2)), font="Arial 8", anchor=N)  # 刻度值


