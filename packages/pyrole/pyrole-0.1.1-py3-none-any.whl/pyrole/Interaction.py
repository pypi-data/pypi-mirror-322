import tkinter as tk

_w, _h = 0, 0

class Control:
    _conts = []
    def __init__(self, x, y, cont=tk.Label, **kw):
        self._frm = tk.Frame()
        Control._conts.append(self)
        self._x = x
        self._y = y
        kws = {'master': self._frm}
        kws.update(kw)
        self._cont = cont(**kws)
        self._cont.pack()
        self._id = None

class Label(Control):
    def __init__(self, x, y, text='', textvariable=None):
        cont = tk.Label
        if textvariable is None:
            super().__init__(x, y, cont=cont, text=text)
        else:
            super().__init__(x, y, cont=cont, textvariable=textvariable)

class Button(Control):
    def __init__(self, x, y, text='', textvariable=None, command=print):
        cont = tk.Button
        if textvariable is None:
            super().__init__(x, y, cont=cont, text=text, command=command)
        else:
            super().__init__(x, y, cont=cont, textvariable=textvariable, command=command)

class Entry(Control):
    def __init__(self, x, y, textvariable=tk.StringVar):
        cont = tk.Entry
        super().__init__(x, y, cont=cont, textvariable=textvariable)
        self._textvariable = textvariable

    def get(self):
        return self._textvariable.get()

StringVar = tk.StringVar

def update(kws):
    global _w, _h
    cv = kws['canvas']
    _w, _h = kws['width'], kws['height']
    for cont in Control._conts:
        if cont._id is not None:
            cv.delete(cont._id)
        cont._id = cv.create_window(cont._x + _w // 2, _h // 2 - cont._y, window=cont._frm)
        cont._frm.update()
