import tkinter
from typing import List,Tuple
global LEFT,RIGHT,UP,DOWN
LEFT=tkinter.LEFT
RIGHT=tkinter.RIGHT
UP=tkinter.TOP
DOWN=tkinter.BOTTOM
class Radiobox():
    def __init__(self,father:tkinter.Tk,args:dict={}):
        text=[]
        value=[]
        if "text"in list(args.keys()):
            text=args["text"]
            del args["text"]
        if "value"in list(args.keys()):
            value=args["value"]
            del args["value"]
        initvalue=value[0]
        if "initvalue"in list(args.keys()):
            initvalue=args["initvalue"]
            del args["initvalue"]
        self.valuevar=tkinter.StringVar()
        self.valuevar.set(initvalue)
        self.buttons=[]
        for i in range(min(len(text),len(value))):
            self.buttons.append(tkinter.Radiobutton(father,text=text[i],\
                                                    variable=self.valuevar,value=value[i],
                                                    **args))
        self.tv=dict(zip(value,text))
    def show_get(self):
        print(self.tv[self.valuevar.get()])
        return self.tv[self.valuevar.get()]
    
    def pack(self,args:List[dict]):
        for i in range(len(self.buttons)):
            self.buttons[i].pack(**(args[i]))
    def grid(self,args:List[dict]):
        for i in range(len(self.buttons)):
            self.buttons[i].grid(**(args[i]))
    def place(self,args:List[dict]):
        for i in range(len(self.buttons)):
            print(args[i])
            self.buttons[i].place(**(args[i]))

class Checkbox():
    def __init__(self,father:tkinter.Tk,args={}):
        value=[]
        if "value" in args:
            
    

def print_selection(listbox:tkinter.Listbox):
    # 获取被选中的项的索引
    selected_indices = listbox.curselection()
    # 遍历所有被选中的项
    for index in selected_indices:
        # 打印被选中的项
        print(listbox.get(index))
class p_where():
    def __init__(self,p,where):
        self.p = p
        self.where = where
    def __call__(self):
        try:
            self.p(**self.where)
        except:
            self.p(self.where)

def place_user(widget,place):
    if place=="pack":
        return widget.pack
    elif place=="grid":
        return widget.grid
    elif place=="place":
        return widget.place

class Windows():
    def __init__(self):
        import tkinter
        self.tk=tkinter
        self.widget={}
        self.root_name=''
    def add(self,widget:str,name:str,father_name=None,placewhere=("pack",{"side":UP}),args:dict={}):
        if widget=="-Window":
            self.widget[name]=self.tk.Tk()
            self.root_name=name
        if widget=="-Text":
            d=self.tk.Label(self.widget[father_name],**args)
            p_where(place_user(d,placewhere[0]),placewhere[1])()
            self.widget[name]=d
        if widget=="-Button":
            d=self.tk.Button(self.widget[father_name],**args)
            p_where(place_user(d,placewhere[0]),placewhere[1])()
            self.widget[name]=d
        if widget=="-Canvas":
            d=self.tk.Canvas(self.widget[father_name],**args)
            p_where(place_user(d,placewhere[0]),placewhere[1])()
            self.widget[name]=d
        if widget=="-Input":
            d=self.tk.Text(self.widget[father_name],**args)
            p_where(place_user(d,placewhere[0]),placewhere[1])()
            self.widget[name]=d
        if widget=="-Listbox":
            data=[]
            if "data"in list(args.keys()):
                data=args["data"]
                del args["data"]
            if "command" in list(args.keys()):
                command=args["command"]
                del args["command"]
            d=self.tk.Listbox(self.widget[father_name],**args)
            p_where(place_user(d,placewhere[0]),placewhere[1])()
            self.widget[name]=d
            for i in data:
                d.insert("end",i)
            try:
                self.widget[name].bind(command[0],lambda x:command[1](self.widget[name]))
            except:
                pass
        if widget=="-Radiobutton":
            d=Radiobox(self.widget[father_name],args)
            p_where(place_user(d,placewhere[0]),placewhere[1])()
            self.widget[name]=d
        '''
        if widget=="-Checkbutton":
            d=Checkbox(self.widget[father_name],args)
            p_where(place_user(d,placewhere[0]),placewhere[1])()
            self.widget[name]=d
        '''
    def run(self,name,attr,*args,**argp):
        attr=attr[1:]
        if len(argp)!=0:
            return getattr(self.widget[name],attr)(**argp)
        else:
            return getattr(self.widget[name],attr)(*args)
    def get(self,name):
        return self.widget[name]
    def start(self):
        self.widget[self.root_name].mainloop()