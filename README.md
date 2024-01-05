# game_rank
游戏排行榜，使用 redis 的有序集合实现
额外需求：如果玩家分数，触发时间均相同，则根据玩家等级，名字依次排序，此情景如何设计?
提供两种方案 1.玩家查询排行帮的时候再根据玩家的分数/时间/等级/姓名做排序，因为就 20 条信息，不存在性能问题，缺点：发排行榜奖励时 可能会有误差
           2.将玩家的等级/名字等信息转化成数字 拼接到 redis 分数的小数部分的高位，剩余时间使用固定的位数，后边添加等级/名字信息
本例使用的是第一种方案
# 运行结果展示
{'uid': 656, 'lev': 656, 'name': '656', 'ranking': 9327, 'point': 65}
{'uid': 655, 'lev': 655, 'name': '655', 'ranking': 9328, 'point': 65}
{'uid': 654, 'lev': 654, 'name': '654', 'ranking': 9329, 'point': 65}
{'uid': 653, 'lev': 653, 'name': '653', 'ranking': 9330, 'point': 65}
{'uid': 652, 'lev': 652, 'name': '652', 'ranking': 9331, 'point': 65}
{'uid': 651, 'lev': 651, 'name': '651', 'ranking': 9332, 'point': 65}
{'uid': 650, 'lev': 650, 'name': '650', 'ranking': 9333, 'point': 65}
{'uid': 669, 'lev': 669, 'name': '669', 'ranking': 9334, 'point': 66}
{'uid': 668, 'lev': 668, 'name': '668', 'ranking': 9335, 'point': 66}
{'uid': 667, 'lev': 667, 'name': '667', 'ranking': 9336, 'point': 66}
{'uid': 666, 'lev': 666, 'name': '666', 'ranking': 9337, 'point': 66}
{'uid': 665, 'lev': 665, 'name': '665', 'ranking': 9338, 'point': 66}
{'uid': 664, 'lev': 664, 'name': '664', 'ranking': 9339, 'point': 66}
{'uid': 663, 'lev': 663, 'name': '663', 'ranking': 9340, 'point': 66}
{'uid': 662, 'lev': 662, 'name': '662', 'ranking': 9341, 'point': 66}
{'uid': 661, 'lev': 661, 'name': '661', 'ranking': 9342, 'point': 66}
{'uid': 660, 'lev': 660, 'name': '660', 'ranking': 9343, 'point': 66}
{'uid': 679, 'lev': 679, 'name': '679', 'ranking': 9344, 'point': 67}
{'uid': 678, 'lev': 678, 'name': '678', 'ranking': 9345, 'point': 67}
{'uid': 677, 'lev': 677, 'name': '677', 'ranking': 9346, 'point': 67}
{'uid': 676, 'lev': 676, 'name': '676', 'ranking': 9347, 'point': 67}
