# pyutility
My py utility tools


## ResPool 

The Common pool design for resource

### how to use

```python
class A:
    def run(self,*argv, **kwargs):
        print( *argv, **kwargs)
    
def createA():
    return A()

# ----
a = MDResPool(2,-1,2)
a.set_generate_func(createA, argv=(), kwargs={}) # set connection power
a.connect()
a.run()  # you can put argv, kwargs
a.close()
```

