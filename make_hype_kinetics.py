import numpy as np
import scipy.interpolate as spi
import matplotlib

matplotlib.use('agg')

import matplotlib.pyplot as plt
from PIL import Image

hype_points = np.loadtxt('gartner_hype.csv', delimiter=',')

hype_curve = spi.interp1d(hype_points[:, 0], hype_points[:, 1], kind='cubic',
                     fill_value='extrapolate')


def time_delay(t):
    return max([t - 2, 0]) * 0.6


def plot_point(work_x):
    work_y = hype_curve(work_x)
    admin_x = time_delay(work_x)
    admin_y = hype_curve(admin_x)

    x = np.linspace(0, 40, 100)
    plt.plot(x, hype_curve(x), color='red')
    ax = plt.gca()
    ax.set(ylim=[0, 18])
    plt.text(1, 1, 'Technology trigger')
    plt.text(4.2, 12.2, 'Peak of inflated expectations (mount bullshit)')
    plt.text(9.5, 2.3, 'Trough of disillusionment')
    plt.text(11, 4.8, 'Slope of enlightenment')
    plt.text(18, 7, 'Plateau of productivity')
    plt.xlabel("Time")
    plt.ylabel("Visibility")
    plt.title("Following the Gartner Hype Cycle")

    plt.plot(work_x, work_y, 'bo')
    plt.plot(admin_x, admin_y, 'bo')
    plt.annotate('People actually doing the work',
                (work_x, work_y),
                (work_x + 3, 16),
                color='blue',
                arrowprops=dict(arrowstyle="->", relpos=(0, 0)))
    plt.annotate('Managers and consultants',
                (admin_x, admin_y),
                (admin_x + 3, 17),
                color='blue',
                arrowprops=dict(arrowstyle="->", relpos=(0, 0)))
    return plt.gcf()


out_x = np.linspace(0, 20, 3 * 25)

frames = []
for x in out_x:
    fig = plot_point(x)
    fig.tight_layout(pad=0)
    fig.canvas.draw()
    sz = fig.canvas.get_width_height()
    data = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    fig.clear()
    data = data.reshape(sz[::-1] + (4,))
    new_frame = Image.frombytes('RGBa', sz, data)
    frames.append(new_frame.convert('RGB'))

# Save into a GIF file that loops forever
frames[0].save('hype_kinetics.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=60, loop=0)
