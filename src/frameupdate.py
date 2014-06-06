from threading import Thread

"""
updates each frame, so it can notify you etc..
"""
class updatethread(Thread):

  def __init__(self, parent):
    Thread.__init__(self)
    self.parent = parent