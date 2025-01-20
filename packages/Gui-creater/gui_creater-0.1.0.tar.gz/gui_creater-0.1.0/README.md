This is a package about how to create a gui easily,
like this
```python
import Gui_creater as gc
root=gc.windows()
root.add("-Window",name=1)
a.add("-Text","2",father_name="1",placewhere=("place",{"x":0,"y":0}),args={"text":"HELLO_GUI(你好，GUI)","bg":"red"})
a.add("-Button","3",father_name="1",placewhere=("place",{"x":100,"y":0}),args={"text":"HELLO(你好)","bg":"blue","command":lambda:print("HELLO GUI!")})
root.start()
```
They can create a window,and there is a text ("HELLO_GUI("你好，GUI")"),a button (its text is "HELLO(你好)").If you click the button,then it can print("HELLO GUI!").You can run "test.py" to try it. 