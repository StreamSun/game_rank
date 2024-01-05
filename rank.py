# _*_ coding:utf-8 _*_
"""
通用排行榜设计
"""
import time
import datetime
import redis
FMT = "%y%m%d%H%M"

rds = redis.StrictRedis(host='localhost', port=6379)


def get_self_rank(uid, rank_key, pipeline=None):
    """
    获取玩家自己的排名信息
    """
    pipeline = pipeline or rds.pipeline()
    pipeline.exists(rank_key)
    pipeline.zrevrank(rank_key, uid)
    pipeline.zscore(rank_key, uid)
    is_exist, self_rank, self_point = pipeline.execute()
    return is_exist, self_rank, self_point


def get_float_score(end, score):
    """
    获取玩家最终存入 redis 的分数
    整数位是玩家得分 小数位是到结束之间剩余的时间
    """
    end_float_str = "0." + str(max(0, end * 1000000 - int(time.time() * 1000000)))
    return float(score) + float(end_float_str)


def get_rank_key(prefix, end):
    """
    prefix: 排行榜键的前缀标记是哪个系统的排行榜
    end: 赛季结束时间;
    """
    # 将时间戳改成时间字符串 便于查询
    end = time.strftime(FMT, time.localtime(end))
    return f'{prefix}:{end}'


def update_game_rank(uid, rank_key, add_score, end_time):
    """
    更新分数排行榜
    """
    pipeline = rds.pipeline()
    is_exist, old_rank, old_point = get_self_rank(uid, rank_key, pipeline)
    if old_point is None:
        old_point = 0
    pipeline.zadd(rank_key, {str(uid): get_float_score(end_time, int(old_point) + add_score)})
    if old_rank is None and not is_exist:
        # 榜单新建 设置榜单过期时间
        pipeline.expire(rank_key, 30)
    pipeline.execute()

def get_rank_list_info(uid, rank_key):
    """
    玩家查询名次接口，能够查询自己名次前后10位玩家的分数和名次
    """
    pipeline = rds.pipeline()
    _, self_rank, _ = get_self_rank(uid, rank_key, pipeline)
    start, end = max(0, self_rank - 10), self_rank + 10
    pipeline.zrevrange(rank_key, start, end, withscores=True)
    pipeline.zcard(rank_key)
    uid_scores, rank_cnt = pipeline.execute()
    self_info = {}
    if not uid_scores:
        rank_info = []
    else:
        users_map = {}  # user map是
        for i, _ in uid_scores:
            users_map[i] = {"uid": int(i), "lev": int(i), "name": i.decode()}  # 获取真实等级和名字
        uid_scores.sort(key=lambda x: (float(x[1]), users_map[x[0]]['lev'], users_map[x[0]]['name'])) # 分数时间相同根据玩家等级/名字排序
        rank_info = []
        # 玩家排名、分数
        for i, j in enumerate(uid_scores):
            user_id = j[0]
            one = users_map.get(user_id)
            one['ranking'] = i + 1 + start
            one['point'] = int(float(j[1]))
            rank_info.append(one)
    ret = {'rank_info': rank_info, 'total_num': rank_cnt}
    return ret




if __name__ == "__main__":
    rank_prefix = "leaderboard"
    end_time = int(time.mktime(datetime.datetime(2024, 2, 4).timetuple()))
    uids = [i for i in range(100)]
    rank_key = get_rank_key(rank_prefix, end_time)
    for i in range(10000):
        update_game_rank(i, rank_key, i // 10, end_time)
    rank_list = get_rank_list_info(666, rank_key)
    for i in rank_list['rank_info']:
        print(i)
