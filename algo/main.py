from thisnonsense import *
import numpy as np
from  draw import draw_polygon

example = np.array([[0.46169355, 0.87175325],
                    [0.38508065, 0.61201299],
                    [0.13306452, 0.51461039],
                    [0.38709677, 0.45508658],
                    [0.47580645, 0.1547619 ],
                    [0.5483871 , 0.4469697 ],
                    [0.80040323, 0.57142857],
                    [0.54435484, 0.63906926]])

points = example
hierarchy(points)