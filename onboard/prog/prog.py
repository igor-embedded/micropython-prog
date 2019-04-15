from prog.drivers.board import Board
from prog.modules.controller import Controller


class Program():
    def __init__(self):
        self.__board = Board()
        self.__controller = Controller(self.__board)

    def test(self):
        self.__controller.test()

    def run(self):
        self.test()
