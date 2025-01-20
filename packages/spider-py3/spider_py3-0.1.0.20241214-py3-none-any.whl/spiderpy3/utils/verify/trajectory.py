import random
from typing import Tuple, TypeVar, Union, List, Literal

from spiderpy3.utils.verify.point import X, Y, SlidePoints

T = TypeVar("T", bound=int)

Trajectory = Tuple[X, Y, T]
TimeInterval = Union[int, Tuple[int, int]]
TUnit = Literal["s", "ms"]
SlideTrajectory = Union[Tuple[int, int, int]]
SlideTrajectories = List[SlideTrajectory]


def get_offset_slide_trajectories(
        slide_trajectories: SlideTrajectories,
        x_offset: bool,
        y_offset: bool,
        t_offset: bool,
) -> SlideTrajectories:
    offset_slide_trajectories = []
    current_x, current_y, current_t = 0, 0, 0
    for slide_trajectory in slide_trajectories:
        x, y, t = slide_trajectory
        if x_offset is True:
            offset_x = x - current_x
            current_x = x
            x = offset_x
        if y_offset is True:
            offset_y = y - current_y
            current_y = y
            y = offset_y
        if t_offset is True:
            offset_t = t - current_t
            current_t = t
            t = offset_t
        offset_slide_trajectory = (x, y, t)
        offset_slide_trajectories.append(offset_slide_trajectory)
    return offset_slide_trajectories


def get_slide_trajectories(
        slide_points: SlidePoints,
        time_interval: TimeInterval,
        x_offset: bool,
        y_offset: bool,
        t_offset: bool,
        t_unit: TUnit
) -> SlideTrajectories:
    slide_trajectories = []

    t = 0
    for slide_point in slide_points:
        x, y = slide_point

        if isinstance(time_interval, int):
            t += time_interval
        else:
            if isinstance(time_interval, tuple) and len(time_interval) == 2:
                if all(map(lambda _: isinstance(_, int), time_interval)):
                    t += random.randint(*time_interval)
                else:
                    raise ValueError(f"不支持的 time_interval：{time_interval}！")
            else:
                raise ValueError(f"不支持的 time_interval：{time_interval}！")

        slide_trajectory = (x, y, t)
        slide_trajectories.append(slide_trajectory)

    offset_slide_trajectories = get_offset_slide_trajectories(slide_trajectories, x_offset, y_offset, t_offset)

    if t_unit == "s":
        pass
    elif t_unit == "ms":
        offset_slide_trajectories = list(
            map(lambda _: (_[0], _[1], float(f"{_[2] / 1e3:.2f}")), offset_slide_trajectories)
        )
    else:
        raise ValueError(f"不支持的 t_unit：{t_unit}！")

    return offset_slide_trajectories
