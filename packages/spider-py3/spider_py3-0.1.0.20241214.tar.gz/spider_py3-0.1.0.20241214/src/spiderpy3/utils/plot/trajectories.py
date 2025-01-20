import matplotlib
from typing import Optional
import matplotlib.pyplot as plt


class PlotTrajectories(object):
    def __init__(
            self,
            trajectories,
            x_index: int = 0,
            y_index: int = 1,
            t_index: int = 2,
            x_offset: bool = False,
            y_offset: bool = False,
            t_offset: bool = True
    ):
        matplotlib.use("Qt5Agg")

        self.x = self._get_values(trajectories, x_index, x_offset)
        self.y = self._get_values(trajectories, y_index, y_offset)
        self.t = self._get_values(trajectories, t_index, t_offset)

    @staticmethod
    def _get_values(trajectories, index: int, offset: bool):
        values = []
        tmp = 0
        for i in list(map(lambda _: _[index], trajectories)):
            if offset is True:
                tmp += i
                values.append(tmp)
            else:
                values.append(i)
        return values

    def plot(self, show: bool = False, save: bool = False, save_file_path: Optional[str] = None) -> None:
        plt.figure(figsize=(10, 8))

        plt.subplot(2, 1, 1)
        plt.plot(self.x, self.y, color="red")
        plt.title("xy")
        plt.xlabel("x axis")
        plt.ylabel("y axis")

        plt.subplot(2, 2, 3)
        plt.plot(self.t, self.x, color="red")
        plt.title("tx")
        plt.xlabel("t axis")
        plt.ylabel("x axis")

        plt.subplot(2, 2, 4)
        plt.plot(self.t, self.y, color="red")
        plt.title("ty")
        plt.xlabel("t axis")
        plt.ylabel("y axis")

        if show is True:
            plt.show()

        if save is True and save_file_path is not None:
            plt.savefig(save_file_path)
