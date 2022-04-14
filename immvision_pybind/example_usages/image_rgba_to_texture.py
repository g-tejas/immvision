#!/usr/bin/env python3
import OpenGL.GL as gl
import cv2
import numpy as np

def hello():
    print("hello")


def image_rgba_to_texture(img_rgba):
    """
    Performs the actual transfer to the gpu and returns a texture_id
    """
    # inspired from https://www.programcreek.com/python/example/95539/OpenGL.GL.glPixelStorei (example 3)
    print(f"Python, entering image_rgba_to_texture, shape={img_rgba.shape}")

    width = img_rgba.shape[1]
    height = img_rgba.shape[0]
    texture_id = gl.glGenTextures(1)
    print(f"Python, image_rgba_to_texture, texture_id={texture_id}")
    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(
        gl.GL_TEXTURE_2D,
        0,
        gl.GL_RGBA,
        width,
        height,
        0,
        gl.GL_RGBA,
        gl.GL_UNSIGNED_BYTE,
        img_rgba,
    )
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    print(f"Python, exiting image_rgba_to_texture texture_id={texture_id}")
    return texture_id


def delete_texture(texture_id):
    print(f"Python, entering delete_texture texture_id={texture_id}")
    gl.glDeleteTextures([texture_id])
    print(f"Python, exiting delete_texture texture_id={texture_id}")


##############################

from sdl2 import *

def sdl_gl_init():
    if SDL_Init(SDL_INIT_EVERYTHING) < 0:
        print("Error: SDL could not initialize! SDL Error: " + SDL_GetError().decode("utf-8"))
        exit(1)

    # out = SDL_GL_LoadLibrary([])
    # print(f"SDL_GL_LoadLibrary returned {out}")

    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_ACCELERATED_VISUAL, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 16)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)

    SDL_SetHint(SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK, b"1")
    SDL_SetHint(SDL_HINT_VIDEO_HIGHDPI_DISABLED, b"1")

    window = SDL_CreateWindow("hello".encode('utf-8'),
                              SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              300, 200,
                              SDL_WINDOW_OPENGL|SDL_WINDOW_RESIZABLE)

    if window is None:
        print("Error: Window could not be created! SDL Error: " + SDL_GetError().decode("utf-8"))
        exit(1)

    gl_context = SDL_GL_CreateContext(window)
    if gl_context is None:
        print("Error: Cannot create OpenGL Context! SDL Error: " + SDL_GetError().decode("utf-8"))
        exit(1)

    SDL_GL_MakeCurrent(window, gl_context)
    if SDL_GL_SetSwapInterval(1) < 0:
        print("Warning: Unable to set VSync! SDL Error: " + SDL_GetError().decode("utf-8"))
        exit(1)

    return window, gl_context



def test_main():
    window, gl_context = sdl_gl_init()
    m = cv2.imread("Smiley.png")
    m2 = cv2.cvtColor(m, cv2.COLOR_BGR2BGRA)
    print(m2.shape)
    texture_id = image_rgba_to_texture(m2)
    print(f"texture_id={texture_id}")
    delete_texture(texture_id)


if __name__ == "__main__":
    test_main()