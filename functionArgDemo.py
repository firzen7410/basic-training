def double(*args):
    return [x*2 for x in args ]
print(double(2,6,7,4,2))

def find(key,**kwarg):
    return kwarg[key] if key in kwarg else None

def connect(**kwargs):
    host = kwargs.get('host', 'localhost')
    port = kwargs.get('port', 3306)
    user = kwargs.get('user', 'root')
    print(f"連線到 {host}:{port} 使用者 {user}")

connect()
connect(host='192.168.1.1', user='admin')

params = {'x': 10, 'y': 20, 'z': 30}
print(find('y',**params))