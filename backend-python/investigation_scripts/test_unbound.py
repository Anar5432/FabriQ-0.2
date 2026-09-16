def func():
    for x in range(1):
        if True:
            pass
        else:
            if True:
                pass
            else:
                pass
        
        etap_step = 0
        if 'foo' in {}:
            try:
                etap_step = 1
            except ValueError:
                etap_step = 0
        
        print(etap_step)

func()
