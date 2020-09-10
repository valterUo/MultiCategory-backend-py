def path_get(mydict, path):
    elem = mydict
    try:
        for x in path.strip("/").split("/"):
            print(x)
            try:
                x = int(x)
                elem = elem[x]
            except:
                elem = elem.get(x)
    except:
        pass
    return elem


def update(mydict, path, new_elem):
    key_path = path.strip("/").split("/")
    if len(key_path) > 1:
        main_key = key_path.pop(0)
        last_key = key_path[-1]
        new_dict = dict(mydict[main_key])
        elem = new_dict
        for key in key_path:
            if key == last_key:
                try:
                    elem[key] = new_elem
                except:
                    pass
            else:
                try:
                    elem = new_dict[key]
                except:
                    pass
        mydict[main_key] = new_dict


def remove(mydict, path):
    key_path = path.strip("/").split("/")
    if len(key_path) > 1:
        main_key = key_path.pop(0)
        last_key = key_path[-1]
        new_dict = dict(mydict[main_key])
        elem = new_dict
        for key in key_path:
            if key == last_key:
                try:
                    del elem[key]
                except:
                    pass
            else:
                try:
                    elem = new_dict[key]
                except:
                    pass
        mydict[main_key] = new_dict