from environment.models.fruit import Fruit


class FaulFruit(Fruit):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)