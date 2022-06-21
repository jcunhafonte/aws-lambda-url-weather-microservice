class Router:
    def __init__(self):
        self.routes = {}

    def set(self, path, method, handler):
        self.routes[f"{path}-{method}"] = handler

    def get(self, path, method):
        try:
            route = self.routes[f"{path}-{method}"]
        except KeyError:
            raise RuntimeError(f"Cannot route request to the correct method. path={path}, method={method}")
        return route