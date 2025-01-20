import random
from typing import Tuple, TypeVar, List, Any, Literal

from spiderpy3.utils.verify.sdk.cBezier import bezierTrajectory
from spiderpy3.utils.execute.js import execute_js_code_by_execjs

X = TypeVar("X", bound=int)
Y = TypeVar("Y", bound=int)

Point = Tuple[X, Y]

SlidePoint = Point
SlidePoints = List[SlidePoint]
SlideMode = Literal["bezier_curve", "ghost_cursor"]


def get_slide_points_by_bessel_function(slide_distance: int, **kwargs: Any) -> SlidePoints:
    bt = bezierTrajectory()
    kw = {
        "numberList": random.randint(25, 45),
        "le": 4,
        "deviation": 10,
        "bias": 0.5,
        "type": 2,
        "cbb": 1,
        "yhh": 5
    }
    """
    numberList: 返回的数组的轨迹点的数量 numberList = 150
    le: 几阶贝塞尔曲线，越大越复杂 如 le = 4
    deviation: 轨迹上下波动的范围 如 deviation = 10
    bias: 波动范围的分布位置 如 bias = 0.5
    type: 0表示均速滑动，1表示先慢后快，2表示先快后慢，3表示先慢中间快后慢 如 type = 1
    cbb: 在终点来回摆动的次数
    yhh: 在终点来回摆动的范围
    """
    kw.update(kwargs)
    result = bt.trackArray([0, 0], [slide_distance, 0], **kw)
    result = result["trackArray"].tolist()
    slide_points = [(round(i[0]), round(i[1])) for i in result]
    return slide_points


def get_slide_points_by_ghost_cursor(slide_distance: int, **_kwargs: Any) -> SlidePoints:
    js_code = '''function sdk(from,to){const{path}=require("ghost-cursor");return path(from,to,{useTimestamps:false})}'''  # noqa
    result = execute_js_code_by_execjs(
        js_code=js_code, func_name="sdk",
        func_args=({"x": 0, "y": 0}, {"x": slide_distance, "y": 0})
    )
    slide_points = [(round(i["x"]), round(i["y"])) for i in result]
    return slide_points


def get_slide_points(slide_distance: int, slide_mode: SlideMode = "bezier_curve", **kwargs: Any) -> List[SlidePoint]:
    if slide_mode == "bezier_curve":
        slide_points = get_slide_points_by_bessel_function(slide_distance, **kwargs)
    elif slide_mode == "ghost_cursor":
        slide_points = get_slide_points_by_ghost_cursor(slide_distance, **kwargs)
    else:
        raise ValueError(f"不支持的 slide_mode：{slide_mode}！")
    return slide_points
