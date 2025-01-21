#pylint:disable=E0401

#pyrole源代码

'''
这个模块可以让你的代码更简单
'''
import tkinter as _tk
import PIL.Image as _image
import PIL.ImageTk as _ImageTk
import math as _math
import random as _random
import time as _time
import sys as _sys
def _gcg():
    """
    获取调用者的全局变量。
    """
    # 获取当前调用栈的信息
    sys=_sys
    frame = sys._getframe(1)
    # 获取调用者的全局变量
    caller_globals = frame.f_globals
    return caller_globals

_w=_tk.Tk(className='''python Role code''')
_w.withdraw()#默认是隐藏，只有在程序运行时才显示。

_sw,_sh=_w.winfo_screenwidth(),_w.winfo_screenheight()
_cv=_tk.Canvas(_w,width=_sw,height=_sh,bd=0,highlightthickness=0)

_rolelist=[]
_globals={}
_i=1j
NoFrame=_w.overrideredirect
set_the_title=_w.title
isinit=True
class PyroleError(Exception):
    """
    异常类，用于处理与 Pyrole 相关的错误。

    参数:
        message (str): 错误消息，描述发生了什么问题。
        detailed (str): 详细描述，如为何引发这个错误。
        code (int, optional): 错误代码，默认为 None。
    """

    def __init__(self, message, detailed='', code=None):
        """
        初始化 PyroleError 实例。

        参数:
            message (str): 错误消息。
            detailed (str): 可选的详细描述。
            code (int, optional): 可选的错误代码。
        """
        super().__init__(message+'\n'+detailed)
        self.code = code
        self.detailed = detailed
        self.message = message

    def __str__(self):
        """
        返回错误的字符串表示形式。

        如果指定了错误代码，则将其包含在错误消息中。
        """
        error_message = self.message+'\n'+self.detailed
        if self.code is not None:
            error_message = f'[{self.code}] {error_message}'
        return error_message

class Background:
	_o=None
	def __new__(cls,*args,**kws):
		if cls._o is None:
			cls._o=super().__new__(cls)
		return cls._o
	def __init__(self,path=__file__.replace('__init__.py','')+f'images{__file__[-12]}bg.png'):
		self._path=path
		self._image=_ImageTk.PhotoImage(_im(path).resize((_sw,_sh)))
		self._bgid=_cv.create_image(_sw/2,_sh/2,image=self._image)
	def toggle(self,path):
		_cv.delete(self._bgid)
		self._path=path
		self._image=_ImageTk.PhotoImage(_im(self._path).resize((_sw,_sh)))
		self._bgid=_cv.create_image(_sw/2,_sh/2,image=self._image)
		

_isMouseDown=False
def _ismd(event):
    global _isMouseDown
    _isMouseDown=True
_cv.bind('<Button-1>',_ismd)
def _nomd(event):
    global _isMouseDown
    _isMouseDown=False
_cv.bind('<ButtonRelease-1>',_nomd)
_mx=0
_my=0
def _mpos(event):
    global _mx,_my
    _mx=int(event.x-_sw/2)
    _my=int(_sh/2-event.y)
_cv.bind('<Motion>',_mpos)
_PressKey=''
def _psk(event):
    global _PressKey
    _PressKey=event.char
    
_cv.bind('<Key>',_psk)

class _PyroleCode:
	_objs=[]
	def __new__(cls,a):
		for obj in cls._objs:
			if obj._a is a:
				return obj
		cls._tf=True
		cls._objs.append(super().__new__(cls))
		return cls._objs[-1]
	def __init__(self,a):
		self._a=a
		

class Event():
    def __init__(self,event):
        self._event=event
    def bool(self):
        v={
                        'mousepos':(_mx,_my),
                        #'鼠标位置':(_mx,_my),
                        'mousedown':_isMouseDown,
                        #'鼠标按下':_isMouseDown
                }
        b=eval(self._event,v)
        return b
    

def _get_kws():
    return {
        'roles':_rolelist.copy(),
        'width':_sw,
        'height':_sh,
        'canvas':_cv,
        'glo':globals()
    }

def play():
    for i in _rolelist:
        i._Libs()
    while True :
    	try:
    		refresh()
    	except _tk.TclError:
    		return 'hello'
    	except PyroleError as e:
    		print(repr(type(e))[8:-2],':',e)

def refresh(code=_PyroleCode(_PyroleCode)):
        if code is _PyroleCode(_PyroleCode):
        	_w.deiconify()
        for module in _modules:
            if 'update' in dir(module):
                module.update(_get_kws())
        _w.update()
        for i in _rolelist:
            for j in range(0,len(i._codeEvent)):
                Bool=i._codeEvent[j]
                if type(Bool)==Event:
                    Bool=Bool.bool()
                if Bool:
                    i._code[j]()
        isinit=False
        _time.sleep(0.02)

_cv.pack()


class Role:
    _roles=[]
    @classmethod
    def getrole(cls,ID):
    	'''
    	通过id调用角色
    	参数：
    		id(int)：角色id，通过getid函数返回.
    	返回：
    		Role：你的id所对应的角色
    	事例：
    		>>>Role()#没有声明变量
    		>>>role=Role.getrole(1):
    		>>>role
    		未命名
    	'''
    	try:
    		return cls._roles[ID-1]
    	except IndexError :
    		raise PyroleError(
    			'错误：未找到角色',
    			f'你的角色id输入为{ID}，但是角色只有{" ".join(cls._roles)}这些，总共{len(cls._roles)}个,找不到id为{ID}的',
    			'空盒'
    		)
    def getid(self):
    	'''
    	通过角色获取id
    	参数：
    		仅self
    	返回：
    		int：你的角色的id
    	事例：
    		>>>role=Role()#没有声明变量
    		>>>id=Role.getid(role):
    		>>>id
    		role
    	'''
    	return type(self)._roles.index(self)+1
    def __new__(cls,*args,**kw):
    	self=super().__new__(cls)
    	cls._roles.append(self)
    	return self
    def _draw(self):
    	# 调整图像大小和旋转
        self._im[self._imid] = _im(self._imstring[self._imid]).resize((self._width, self._height))
        self._im[self._imid] = self._im[self._imid].rotate(self._angle, expand=True)
        self._im[self._imid] = _ImageTk.PhotoImage(self._im[self._imid])
   	 # 如果_id存在并且是有效的Canvas ID，则先删除旧的图像
        if self._id is not None:
        	_cv.delete(self._id)
    	# 创建新的图像
        self._id = _cv.create_image(self._x, self._y, image=self._im[self._imid])
	#绑定相应的事件
    def bind_event(self,function,event):
           if type(event)!=Event:
               event=Event(event)
           self._code.append(function)
           self._codeEvent.append(event)
    def xymove(self,x,y):
        oldx=self._x
        oldy=self._y
        _cv.move(self._id,x,-y)
        newx=oldx+x
        newy=oldy-y
        if self._pen['isdown']:
            _cv.create_line(oldx,oldy,newx,newy,fill=self._pen['color'])
        self._tx += x
        self._x += x
        self._ty += y
        self._y -= y
    #移动num步
    def move(self, num):
        oldx = self._x
        oldy = self._y
        x = ((_i ** (self._angle / 90)).real) * num
        y = ((_i ** (self._angle / 90)).imag) * num
        self._x += x
        self._y -= y
        
        if self._pen['isdown']:
            _r = self._pen['size']
            color=self._pen['color']
            _cv.create_line(oldx, oldy, self._x, _sh - self._y, width=_r,fill=color)
        
        _cv.move(self._id, x, y)
    def rotate(self,angle):
        if angle%360==0:
        	return 
        self._draw()
        self._angle+=angle
        if self._angle==360:
            self._angle=0
    #碰到边缘就反弹
    def boenedg(self):
        pos=_cv.coords(self._id)
        x=pos[0]
        y=pos[1]
        if x+self._width/2>=_sw:
            ang=self._angle
            ang=90-ang
            self._angle=90+ang
        if y+self._height/2>=_sh:
            ang=self._angle
            ang=ang-90
            self._angle=ang
        if x-self._width/2<=0:
            ang=self._angle
            ang=90-ang
            self._angle=90+ang
        if y-self._height/2<=0:
            ang=self._angle
            ang=ang-90
            self._angle=ang
        self._draw()
    #面向angle度
    def face(self,angle):
        self._angle=angle
        self._draw()
        
    #移到x,y
    def goto(self,x,y):
        xxx=x
        yyy=y
        self._tx=x
        self._ty=y
        x1=self._x
        y1=self._y
        x=_sw/2+x
        y=_sh/2-y
        pos=_cv.coords(self._id)
        x2=pos[0]
        y2=pos[1]
        _cv.move(self._id,-pos[0],-pos[1])
        self._x,self._y=x,y
        _cv.move(self._id,self._x,self._y)
        if self._pen['isdown']:
         self._pen['draws'].append(
        _cv.create_line(
        x1,
        y1,
        x2,
        y2,
        width=self._pen['size']
        ))
        if hasattr(self,'physical_attributes'):
            if self.physical_attributes['Inertia']:
                e=self.physical_attributes['exercise']
                e[0]=xxx/2
                e[1]=yyy/2
        else:
            pass
        
    #设置X坐标为x
    def setX(self,x):
        self._x=_sw/2+x
        self._tx=x
        self.goto(self._tx,self._ty)
    #设置Y坐标为y
    def setY(self,y):
        self._y=_sh/2-y
        self._ty=y
        self.goto(self._tx,self._ty)
    #X坐标增加XADD
    def xadd(self,XADD):
        self._x+=XADD
        self._tx+=XADD
        self.goto(self._tx,self._ty)
    #Y坐标增加YADD
    def yadd(self,YADD):
        self._y-=YADD
        self._ty+=YADD
        self.goto(self._tx,self._ty)
    #def inTimeGoto(x,y,t):
#        
    #下一个造型
    def next_look(self):
        self._imid+=1
        len_imstring=len(self._imstring)
        if self._imid >= len_imstring:
            self._imid-=len_imstring
        self._draw()
    #上一个造型
    def previous_look(self):
        self._imid-=1
        if self._imid < 0:
            self._imid+=len(self._imstring)
        self._draw()
    def to_look(self,number):
        len_imstring=len(self._imstring)
        if number>len_imstring:
            raise PyroleError('没有这么多造型！',
                code='国王的新衣',
                detailed=f'造型总共有{len_imstring}个,不存在第{number}个')
        self._imid=number-1
        self._draw()
    #落笔
    def pen_down(self):
        self._pen['isdown']=True
    #抬笔
    def pen_up(self):
        self._pen['isdown']=False
    #清除画笔
    def pen_delete(self):
        for i in self._pen['draws']:
            _cv.delete(i)
        self._pen['draws']=[]
    #设置画笔粗细为a
    def pen_size(self,a):
        self._pen['size']=a
    #设置画笔的颜色为color
    def pen_color(self,color):
        self._pen['color']=color
    #
    def press(self):
        return _ismd
    def quit_edge(self,qe='nswe'):
        x=self._x
        y=self._y
        if x-self._width/2>_sw and 'e' in qe:
            return True
        if y-self._height/2>_sh and 'n' in qe:
            return True
        if x+self._width/2<0 and 'w' in qe:
            return True
        if y+self._height/2<0 and 's' in qe:
            return True
        return False
    def meet_edge(self,qe='nswe'):
        x=self._x
        y=self._y
        if 'e' in qe and x+self._width/2>=_sw:
            return True
        if 'n' in qe and y+self._height/2>=_sh:
            return True
        if 'w' in qe and x-self._width/2<=0:
            return True
        if 's' in qe and y-self._height/2<=0:
            return True
        return False
    def attribute(self,attrname):
        attrname=attrname.lower()
        if attrname=='x' or attrname=='X坐标':
            return self._x
        if attrname=='y' or attrname=='Y坐标':
            return self._y
        if attrname == 'modeling' or attrname=='造型编号':
            return self._imid+1
        if attrname=='angle' or attrname=='角度':
            return self._angle
        if attrname== 'size' or attrname=='大小':
            return self._size
        if attrname== 'width' or attrname=='宽度':
            return self._width
        if attrname== 'height' or attrname=='高度':
            return self._height
    def distanc(self,Object):
        Object=Object.lower()
        if Object=='鼠标' or Object=='mouse':
            a=abs(_mx-self._tx)
            b=abs(_my-self._ty)
        else :
            a=abs(Object._tx-self._tx)
            b=abs(Object._ty-self._ty)
        c=(a**2+b**2)**0.5
        return c
            
    def mousepos(self,attr):
        if attr.upper()=='X':
            return _mx
        elif attr.upper()=='Y':
            return _my
        
    def screenWH(self,attr):
        if attr.upper()=='WIDTH' or attr=='宽度':
            return _sw
        elif attr.upper()=='HEIGHT' or attr=='高度':
            return _sh
    def time(self,arg):
        time=_time.localtime()
        if arg=='year' or arg=='年':
            return time[0]
        elif arg=='month' or arg=='月':
            return time[1]
        elif arg=='day' or arg=='日':
           return time[2]
        elif arg=='hour' or arg=='时':
            return time[3]
        elif arg=='minute' or arg=='分':
            return time[4]
        elif arg=='second' or arg=='秒':
            return time[5]
        elif arg=='week' or arg=='星期':
            return time[6]+1
    def get_bounding_box(self):
        position = _cv.coords(self._id)
        return (position[0] - self._width/2, 
                    position[1] - self._height/2,
                    position[0] + self._width/2, 
                    position[1] + self._height/2)

    def check_collision_with_mouse(self, mouse_position):
        bbox = self.get_bounding_box()
        return bbox[0] <= mouse_position[0] <= bbox[2] and bbox[1] <= mouse_position[1] <= bbox[3]

    def check_collision_with_role(self, other_role):
        this_bbox = self.get_bounding_box()
        other_bbox = other_role.get_bounding_box()
        return not (this_bbox[2] <= other_bbox[0] or this_bbox[0] >= other_bbox[2] or
                        this_bbox[3] <= other_bbox[1] or this_bbox[1] >= other_bbox[3])
    def __repr__(self):
    	glo=_gcg()
    	for var in glo:
    		if glo[var] is self:
    			return var
    	return '未命名'
    def __init__(self,x=0,y=0,angle=0,size=100,im=[],width=None,height=None,rolevars=None):
        self._tx=x
        self._ty=y
        x=_sw/2+x
        y=_sh/2-y
        self._x=x
        self._y=y
        self._size=size
        self._angle=angle
        self._pen={
        'isdown':False,
        'draws':[],
        'size':1,
        'color':'#000000'
        }
        self._im=im.copy()
        self._imstring=im.copy()
        if width is None:
            width=_im(self._im[0]).width
        if height is None:
            height=_im(self._im[0]).height
        wh=width+height
        wh//=2
        width = width*size//wh
        height = height*size//wh
        if im == []:
            raise SyntaxError('你给加个造型不好吗')
        for i in range(len(self._im)):
            self._im[i]=_im(self._im[i])
            self._im[i]=self._im[i].resize((width,height))
            self._im[i]=_ImageTk.PhotoImage(self._im[i])
            _images.append(self._im[0])
        self._id=_cv.create_image(x,y,image=self._im[0])#不是角色id，是在屏幕上的图形id.
        self._imid=0
        self._code=[]
        self._codeEvent=[]
        self._width=width
        self._height=height
        _rolelist.append(self)
        if rolevars is None:
            rolevars={}
        self._rolevars=rolevars
        self._name=repr(self)
        self._init=False
        self._Libs()
        self._init=True
    def _Libs(self):
            for module in _modules:
                if not self._init:
                    if 'init_role' in dir(module):
                        module.init_role(self)

def Random_int(a, b):
    return _random.randint(a, b)

def is_even(num):
    num1 = num % 2
    return bool(num1) and int(num) == num

def is_odd(num):
    return (not is_even(num)) and int(num) == num

def is_prime(num):
    if int(num) != num:
        return False
    if num <= 1:  # 确保大于 1 的整数才可能是质数
        return False
    if num == 2:  # 特殊处理偶数，2 是唯一的偶数质数
        return True
    if num % 2 == 0:  # 排除所有偶数（除了2）
        return False

    # 只需检查到 sqrt(num)
    for i in range(3, int(num**0.5) + 1, 2):  # 从 3 开始，并步长为 2（排除偶数）
        if num % i == 0:
            return False
    return True

def is_int(num):
    return int(num) == num

def is_positive(num):
    return num > 0

def is_negative(num):
    return num < 0

def Divisible(Divisor, divisor):
    return Divisor % divisor == 0

def cos(angle):
    return _math.cos(angle)

def sin(angle):
    return _math.sin(angle)

def tan(angle):
    return _math.tan(angle)

def acos(num):
    return _math.acos(num)

def asin(num):
    return _math.asin(num)

def atan(num):
    return _math.atan(num)

_images=[]

def add_module(module):
    global _modules
    _modules.append(module)
    if 'init' in dir(module):
        module.init(_get_kws())

_modules=[]
def _im(file):
    a=_image.open(file)
    return a

Background()

_file=__file__.replace('__init__.py','')
s=_file[-1]#获取不同系统的路径分割字符，如Android是/,Windows是\\
ostar=_file+f'images{s}ostar.gif'
bstar=_file+f'images{s}bstar.gif'
astar=_file+f'images{s}astar.gif'
fstar=_file+f'images{s}fstar.gif'
gstar=_file+f'images{s}gstar.gif'
kstar=_file+f'images{s}kstar.gif'
mstar=_file+f'images{s}mstar.gif'

mercury = _file + f"images{s}mercury.png"
venus = _file + f"images{s}venus.png"
earth = _file + f"images{s}earth.png"
mars = _file + f"images{s}mars.png"
jupiter = _file + f"images{s}jupiter.png"
saturn = _file + f"images{s}sautrn.png"
uranus = _file + f"images{s}uranus.png"
neptune = _file + f"images{s}neptune.png"

b1 = _file + f'images{s}b1.png'
b2 = _file + f'images{s}b2.png'
b3 = _file + f'images{s}b3.png'
b4 = _file + f'images{s}b4.png'
b5 = _file + f'images{s}b5.png'
b6 = _file + f'images{s}b6.png'
b7 = _file + f'images{s}b7.png'

Icon=_file+f'images{s}icon.jpg'

_icon=_im(Icon)
_icon=_icon.resize((32,32))
_icon=_ImageTk.PhotoImage(_icon)

#_tk.Label(_w,image=_icon).pack()
_w.iconphoto(True,_icon)

del s

if __name__=='__main__':
	#NoFrame(True)
	Role(0,0,0,500,im=[earth])
	def _f():
		role=Role.getrole(1)
		role.rotate(1)
		role.move(1)
	role=Role.getrole(1)
	role.bind_event(_f,'True')
	play()
