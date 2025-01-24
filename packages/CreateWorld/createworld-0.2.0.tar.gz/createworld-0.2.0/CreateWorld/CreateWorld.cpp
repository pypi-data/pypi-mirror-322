// CreateWorld/CreateWorld.cpp
#include <Python.h>
#include <SDL.h>
#include <SDL_image.h>  // 需要 SDL_image 库来加载图片
#include <iostream>
#include <string>

// 定义全局变量
SDL_Window* window = nullptr;
SDL_Renderer* renderer = nullptr;
SDL_Texture* background_texture = nullptr;

// 初始化 SDL
static PyObject* init_sdl(PyObject* self, PyObject* args) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        PyErr_SetString(PyExc_RuntimeError, SDL_GetError());
        return NULL;
    }
    if (IMG_Init(IMG_INIT_PNG) != IMG_INIT_PNG) {
        PyErr_SetString(PyExc_RuntimeError, IMG_GetError());
        return NULL;
    }
    Py_RETURN_NONE;
}

// 创建窗口
static PyObject* create_window(PyObject* self, PyObject* args) {
    const char* title;
    int width, height;
    if (!PyArg_ParseTuple(args, "sii", &title, &width, &height)) {
        return NULL;
    }

    window = SDL_CreateWindow(title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, SDL_WINDOW_SHOWN);
    if (!window) {
        PyErr_SetString(PyExc_RuntimeError, SDL_GetError());
        return NULL;
    }

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        PyErr_SetString(PyExc_RuntimeError, SDL_GetError());
        return NULL;
    }

    Py_RETURN_NONE;
}

// 加载背景图片
static PyObject* load_background(PyObject* self, PyObject* args) {
    const char* path;
    int width, height;
    if (!PyArg_ParseTuple(args, "sii", &path, &width, &height)) {
        return NULL;
    }

    SDL_Surface* surface = IMG_Load(path);
    if (!surface) {
        PyErr_SetString(PyExc_RuntimeError, IMG_GetError());
        return NULL;
    }

    // 调整图片大小
    SDL_Surface* resized_surface = SDL_CreateRGBSurface(0, width, height, surface->format->BitsPerPixel, surface->format->Rmask, surface->format->Gmask, surface->format->Bmask, surface->format->Amask);
    SDL_BlitScaled(surface, NULL, resized_surface, NULL);

    SDL_FreeSurface(surface);

    background_texture = SDL_CreateTextureFromSurface(renderer, resized_surface);
    SDL_FreeSurface(resized_surface);

    if (!background_texture) {
        PyErr_SetString(PyExc_RuntimeError, SDL_GetError());
        return NULL;
    }

    Py_RETURN_NONE;
}

// 清屏并绘制背景
static PyObject* clear_screen(PyObject* self, PyObject* args) {
    if (!renderer) {
        PyErr_SetString(PyExc_RuntimeError, "Renderer not initialized");
        return NULL;
    }

    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);

    if (background_texture) {
        SDL_RenderCopy(renderer, background_texture, NULL, NULL);
    }

    Py_RETURN_NONE;
}

// 更新屏幕
static PyObject* update_screen(PyObject* self, PyObject* args) {
    if (!renderer) {
        PyErr_SetString(PyExc_RuntimeError, "Renderer not initialized");
        return NULL;
    }
    SDL_RenderPresent(renderer);
    Py_RETURN_NONE;
}

// 退出 SDL
static PyObject* quit_sdl(PyObject* self, PyObject* args) {
    if (background_texture) {
        SDL_DestroyTexture(background_texture);
        background_texture = nullptr;
    }
    if (window) {
        SDL_DestroyWindow(window);
        window = nullptr;
    }
    if (renderer) {
        SDL_DestroyRenderer(renderer);
        renderer = nullptr;
    }
    SDL_Quit();
    IMG_Quit();
    Py_RETURN_NONE;
}

// 绘制矩形
static PyObject* draw_rect(PyObject* self, PyObject* args) {
    int x, y, w, h, r, g, b;
    if (!PyArg_ParseTuple(args, "iiiiiii", &x, &y, &w, &h, &r, &g, &b)) {
        return NULL;
    }
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_Rect rect = {x, y, w, h};
    SDL_RenderFillRect(renderer, &rect);
    Py_RETURN_NONE;
}

// 绘制圆形
static PyObject* draw_circle(PyObject* self, PyObject* args) {
    int x, y, radius, r, g, b;
    if (!PyArg_ParseTuple(args, "iiiiii", &x, &y, &radius, &r, &g, &b)) {
        return NULL;
    }
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    for (int i = 0; i < 360; i++) {
        int dx = radius * cos(i * M_PI / 180);
        int dy = radius * sin(i * M_PI / 180);
        SDL_RenderDrawPoint(renderer, x + dx, y + dy);
    }
    Py_RETURN_NONE;
}

// 处理事件
static PyObject* poll_event(PyObject* self, PyObject* args) {
    SDL_Event event;
    if (SDL_PollEvent(&event)) {
        switch (event.type) {
            case SDL_QUIT:
                return Py_BuildValue("s", "quit");
            case SDL_KEYDOWN:
                return Py_BuildValue("s", "keydown");
            case SDL_KEYUP:
                return Py_BuildValue("s", "keyup");
            case SDL_MOUSEBUTTONDOWN:
                return Py_BuildValue("s", "mousebuttondown");
            case SDL_MOUSEBUTTONUP:
                return Py_BuildValue("s", "mousebuttonup");
            case SDL_MOUSEMOTION:
                return Py_BuildValue("s", "mousemotion");
            default:
                return Py_BuildValue("s", "none");
        }
    }
    return Py_BuildValue("s", "none");
}

// 定义模块方法
static PyMethodDef CreateWorldMethods[] = {
    {"init_sdl", init_sdl, METH_VARARGS, "Initialize SDL2"},
    {"create_window", create_window, METH_VARARGS, "Create a window"},
    {"load_background", load_background, METH_VARARGS, "Load a background image"},
    {"clear_screen", clear_screen, METH_VARARGS, "Clear the screen"},
    {"update_screen", update_screen, METH_VARARGS, "Update the screen"},
    {"quit_sdl", quit_sdl, METH_VARARGS, "Quit SDL2"},
    {"draw_rect", draw_rect, METH_VARARGS, "Draw a rectangle"},
    {"draw_circle", draw_circle, METH_VARARGS, "Draw a circle"},
    {"poll_event", poll_event, METH_VARARGS, "Poll for events"},
    {NULL, NULL, 0, NULL}
};

// 定义模块结构
static struct PyModuleDef CreateWorldModule = {
    PyModuleDef_HEAD_INIT,
    "CreateWorld",
    "A simple SDL2-based module",
    -1,
    CreateWorldMethods
};

// 初始化模块
PyMODINIT_FUNC PyInit_CreateWorld(void) {
    PyObject* m = PyModule_Create(&CreateWorldModule);
    if (m == NULL) {
        return NULL;
    }
    return m;
}

