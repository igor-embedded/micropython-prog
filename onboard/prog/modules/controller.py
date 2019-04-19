from prog.modules.displaycontroller import DisplayController
from prog.modules.motioncontroller import MotionController


class Controller():
    def __init__(self, board):
        self.board = board
        self.__displaycontroller = DisplayController(self)
        self.__motioncontroller = MotionController(self)

    def test(self):
        self.__motioncontroller.test()
