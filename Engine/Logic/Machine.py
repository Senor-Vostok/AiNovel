class Scene:
    def __init__(self, handler):
        self.handler = handler
        self.textures = handler.textures
        self.synchronous = 0
        self.rendering = False
