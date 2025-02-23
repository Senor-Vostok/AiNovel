class Scene:
    def __init__(self, handler):
        self.handler = handler
        self.textures = handler.textures
        self.synchronous = 1
        self.rendering = False
