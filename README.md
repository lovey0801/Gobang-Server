#简介
使用了django框架实现了五子棋的服务端的逻辑

# 基本结构列表

## <a id="player">player [玩家结构]</a>
| 参数名 | 类型 | 内容 |
| ----  | ---- | ---- |
| name | string | 玩家名称 |
| role | string | 玩家角色 (X 或 O) |
| readyState | bool | 玩家是否准备 |

## <a id="table">table [游戏桌]</a>
| 参数名 | 类型 | 内容 |
| ----  | ---- | ---- |
| code | int | 游戏桌号 |
| playerX | [player](#player) | X玩家 |
| playerO | [player](#player) | O玩家 |
| rows | int | 棋盘的行数 |
| cols | int | 棋盘的列数 |
| squares | string array | 当前游戏内容 |

## <a id="game">game [游戏]</a>
| 参数名 | 类型 | 内容 |
| ----  | ---- | ---- |
| table | [table](#table) | 游戏桌 |
| state | int | 0: idle 表示玩家准备好，游戏未开始<br> 1: gaming 表示游戏中<br> 2: gameover 游戏结束 |
| winner | string | 胜出玩家角色 (X 或 O) |
| curPlayer | string | 当前回合的玩家角色 (X 或 O) |
| timestamp | string | 最后一次游戏内容改变的时间戳 |


# 接口列表 
```
response 基本结构如下：
{
    "code": 0, //返回码，0表示正常，其他的表示失败，详情看msg
    "msg": "请求成功", //返回文本提示信息
    "data": {} //数据部分
}
```

## enter [玩家加入游戏]
`request`

| 参数名 | 类型 | 内容 |
| ----  | ---- | ---- |
| name | string | 玩家名称 |

`response`

| 参数名 | 类型 | 内容 |
| ----  | ---- | ---- |
| game | [game](#game) | 游戏内容 |

## ready [玩家准备]
`request`

| 参数名 | 类型 | 内容 |
| ----  | ---- | ---- |
| tableCode | int | 游戏桌号 |
| role | string | 玩家角色 (X 或 O) |

`response`

| 参数名 | 类型 | 内容 |
| ----  | ---- | ---- |
| game | [game](#game) | 游戏内容 |

## play [玩家开始游戏、玩游戏、轮询状态协议]
`request`

| 参数名 | 类型 | 内容 |
| ----  | ---- | ---- |
| tableCode | int | 游戏桌号 |
| role | string | 玩家角色 (X 或 O) |
| position | int | 下棋的位置 (下棋时传具体位置，轮询传-1) |

`response`

| 参数名 | 类型 | 内容 |
| ----  | ---- | ---- |
| game | [game](#game) | 游戏内容 |
``` 
注: 最先由前端玩家加入游戏后自动触发1s后轮询该协议，直到结束 
```