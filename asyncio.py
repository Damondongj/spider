# import asyncio


# async def main():
#     print("主协程")
#     print("等待result1协程运行")
#     res1 = await result1()
#     print("等待result2协程运行")
#     res2 = await result2(res1)
#     return (res1,res2)


# async def result1():
#     print("这是result1协程")
#     return "result1"


# async def result2(arg):
#     print("这是result2协程")
#     return f"result2接收了一个参数,{arg}"


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         result = loop.run_until_complete(main())
#         print(f"获取返回值:{result}")
#     except:
#         print("exception happened")


import asyncio
import functools


def callback(args, *, kwargs="defalut"):
    print(f"普通函数做为回调函数，获取参数:{args}，{kwargs}")


async def main(loop):
    print("注册callback")
    loop.call_soon(callback, 1)
    wrapped = functools.partial(callback， kwargs="not defalut")
    loop.call_soon(wrapped, 2)
    await asyncio.sleep(0.2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(loop))
finally:
    loop.close()

    