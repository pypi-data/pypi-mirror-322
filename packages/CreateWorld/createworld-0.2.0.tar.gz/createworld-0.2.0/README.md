# CreateWorld - A Simple SDL2-based Python Module

CreateWorld 是一个基于 SDL2 的 Python 模块，旨在模拟 Pygame 的部分功能，提供窗口创建、屏幕绘制和事件处理等基本功能。
与0.1.0相比去除创建多个窗口的功能，但使用更加简便
使用说明1. 安装模块通过以下命令安装   CreateWorld   模块：bashpip install CreateWorld
2. 初始化模块在使用   CreateWorld   之前，需要初始化 SDL2 和相关资源：pythonfrom CreateWorld import CreateWorld

CreateWorld.init()  # 初始化 SDL2 和 SDL_image
3. 创建窗口使用   create   方法创建一个窗口，指定窗口标题、宽度和高度：pythonCreateWorld.create("My Window", width=800, height=600)
4. 加载背景图片使用   load_background   方法加载背景图片，并自动调整图片大小以适应窗口：pythonCreateWorld.load_background("path/to/background.png", width=800, height=600)
5. 绘制图形  CreateWorld   支持绘制矩形和圆形。以下是如何使用这些功能的示例：• 绘制矩形：pythonCreateWorld.draw_rect(x=100, y=100, width=200, height=100, r=255, g=0, b=0)  # 红色矩形
• 绘制圆形：pythonCreateWorld.draw_circle(x=400, y=300, radius=50, r=0, g=255, b=0)  # 绿色圆形
6. 清屏和更新屏幕每次绘制完成后，需要清屏并更新屏幕：pythonCreateWorld.clear()  # 清屏并绘制背景（如果已加载）
CreateWorld.update()  # 更新屏幕显示
7. 事件处理  CreateWorld   提供了简单的事件处理机制，可以检测窗口关闭、键盘事件和鼠标事件。以下是如何使用事件处理的示例：pythonrunning = True
while running:
    event = CreateWorld.poll_event()  # 检测事件
    if event == "quit":  # 窗口关闭事件
        running = False
    elif event == "keydown":  # 键盘按下事件
        print("Key pressed")
    elif event == "mousebuttondown":  # 鼠标按下事件
        print("Mouse button pressed")

    CreateWorld.clear()  # 清屏
    CreateWorld.draw_rect(100, 100, 200, 100, 255, 0, 0)  # 绘制矩形
    CreateWorld.update()  # 更新屏幕
8. 退出模块在程序结束时，调用   quit   方法释放资源并退出 SDL2：pythonCreateWorld.quit()
完整示例代码以下是一个完整的示例，展示如何使用   CreateWorld   模块创建一个窗口、加载背景图片、绘制图形并处理事件：pythonfrom CreateWorld import CreateWorld

# 初始化 SDL
CreateWorld.init()

# 创建窗口
CreateWorld.create("My Window", width=800, height=600)

# 加载背景图片
CreateWorld.load_background("background.png", width=800, height=600)

try:
    running = True
    while running:
        event = CreateWorld.poll_event()  # 检测事件
        if event == "quit":  # 窗口关闭事件
            running = False

        CreateWorld.clear()  # 清屏并绘制背景
        CreateWorld.draw_rect(100, 100, 200, 100, 255, 0, 0)  # 红色矩形
        CreateWorld.draw_circle(400, 300, 50, 0, 255, 0)  # 绿色圆形
        CreateWorld.update()  # 更新屏幕
except KeyboardInterrupt:
    pass

# 退出 SDL
CreateWorld.quit()
支持的事件类型  CreateWorld.poll_event()   方法返回以下事件类型：•   "quit"  ：窗口关闭事件•   "keydown"  ：键盘按下事件•   "keyup"  ：键盘释放事件•   "mousebuttondown"  ：鼠标按下事件•   "mousebuttonup"  ：鼠标释放事件•   "mousemotion"  ：鼠标移动事件•   "none"  ：无事件。
