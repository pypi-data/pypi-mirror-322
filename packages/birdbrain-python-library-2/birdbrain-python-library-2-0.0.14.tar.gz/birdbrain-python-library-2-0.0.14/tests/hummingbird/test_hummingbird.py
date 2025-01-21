import time

from BirdBrain import Hummingbird

def test_blink():
    bird = Hummingbird('A')

    for i in range(0, 10):
        bird.setLED(1, 100)
        time.sleep(0.1)
        bird.setLED(1, 0)
        time.sleep(0.1)

    bird.stopAll()
