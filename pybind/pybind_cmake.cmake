# Note: this file is *included* (not add_subidrectory) via the main CMakeList (parent folder)
# CMAKE_CURRENT_LIST_DIR is thus ".." i.e the main repo dir
set(THIS_DIR ${PROJECT_SOURCE_DIR}/pybind)

#
# Find pydinb11 location via python (probably in a virtual env)
#
if (NOT DEFINED PYTHON_EXECUTABLE)
  set(PYTHON_EXECUTABLE "python")
endif()
execute_process(
  COMMAND "${PYTHON_EXECUTABLE}" -c "import pybind11; print(pybind11.get_cmake_dir())"
  OUTPUT_VARIABLE pybind11_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
list(APPEND CMAKE_PREFIX_PATH "${pybind11_dir}")
find_package(pybind11 CONFIG REQUIRED)

#
# Main target: cpp_imvision python module
#
set(IMMVISION_PYBIND_BIN_MODULE_NAME cpp_immvision)
file(GLOB_RECURSE sources_immvision_pybind ${THIS_DIR}/pybind_src/*.cpp ${THIS_DIR}/pybind_src/*.h)
file(GLOB_RECURSE sources_immvision ${PROJECT_SOURCE_DIR}/src/immvision/*.h ${PROJECT_SOURCE_DIR}/src/immvision/*.cpp)
pybind11_add_module(${IMMVISION_PYBIND_BIN_MODULE_NAME} MODULE ${sources_immvision_pybind} ${sources_immvision})
target_include_directories(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE ${PROJECT_SOURCE_DIR}/src)

#
# Compile definitions and install
target_compile_definitions(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE
    VERSION_INFO=${PROJECT_VERSION}
    IMMVISION_PYBIND_BIN_MODULE_NAME=${IMMVISION_PYBIND_BIN_MODULE_NAME}
    IMMVISION_BUILDING_PYBIND
    )
install(TARGETS ${IMMVISION_PYBIND_BIN_MODULE_NAME} DESTINATION .)


#
# Link with OpenCV
#
find_package(OpenCV)
if (NOT OpenCV_FOUND)
  set(default_opencv_include_dir ${CMAKE_CURRENT_LIST_DIR}/../external/vcpkg/installed/x64-osx/include)
  message(WARN "find_package(OpenCV) failed, using default (and probably bad) location:
          set(OpenCV_INCLUDE_DIRS ${default_include_dir}) ")
  set(OpenCV_INCLUDE_DIRS ${default_include_dir})
else()
  # Hack for broken vcpkg naming
  set(OpenCV_INCLUDE_DIRS ${OpenCV_INCLUDE_DIRS} ${opencv_INCLUDE_DIRS})
endif()
target_include_directories(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE ${OpenCV_INCLUDE_DIRS})
# Link
target_link_libraries(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE opencv_core opencv_imgproc opencv_highgui opencv_imgcodecs)


#
# Link with imgui
#
set(imgui_source_dir ${PROJECT_SOURCE_DIR}/external/imgui)
file(GLOB imgui_sources ${imgui_source_dir}/*.h ${imgui_source_dir}/*.cpp)
target_include_directories(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE ${imgui_source_dir})


# Methode sans rien linker
#  ==> undefined symbol: _ZN5ImGui11PopStyleVarEi

# Methode avec link statique:
# => les import semblent fonctionner, mais c'est inquietant ?
add_library(imgui_shared_pybind STATIC ${imgui_sources})
target_compile_options(imgui_shared_pybind PRIVATE -fPIC)
target_include_directories(imgui_shared_pybind PUBLIC ${imgui_source_dir})
target_link_libraries(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE imgui_shared_pybind)
install(TARGETS imgui_shared_pybind DESTINATION .)


# Methode avec lib shared classique:
#add_library(imgui_shared_pybind SHARED ${imgui_sources})
#target_include_directories(imgui_shared_pybind PUBLIC ${imgui_source_dir})
#target_link_libraries(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE imgui_shared_pybind)
#install(TARGETS imgui_shared_pybind DESTINATION .)




# Methode avec lib shared pybind:
#  ==> undefined symbol: _ZN5ImGui11PopStyleVarEi
#pybind11_add_module(imgui_shared_pybind SHARED ${imgui_sources})
#target_include_directories(imgui_shared_pybind PUBLIC ${imgui_source_dir})
#target_link_libraries(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE imgui_shared_pybind)
#install(TARGETS imgui_shared_pybind DESTINATION .)


# Methode / Hack link pip imgui on docker
# ==> Semi-ok, avec LD_LIBRARY_PATH avant appel python
# LD_LIBRARY_PATH=/dvp/sources/immvision_pybind/venv_docker/lib/python3.10/site-packages/imgui
#set(imgui_docker_lib_dir "/dvp/sources/immvision_pybind/venv_docker/lib/python3.10/site-packages/imgui/")
#target_link_directories(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE ${imgui_docker_lib_dir})
#target_link_libraries(${IMMVISION_PYBIND_BIN_MODULE_NAME} PRIVATE core internal)
#install(TARGETS imgui_shared_pybind DESTINATION .)



#
# Post build: deploy library to ${CMAKE_BINARY_DIR}/_pybind/,
# so that we can use it as a python package name immvision
# add_custom_command(
#     TARGET ${IMMVISION_PYBIND_BIN_MODULE_NAME}
#     POST_BUILD
#     COMMAND
#     ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/CMakeUtilities.py
#       ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_BINARY_DIR} "post_build_deploy"
#     )

#
# immvision_debug_pybind
#
find_package(pybind11 CONFIG REQUIRED)
add_executable(pybind_debug_helper ${THIS_DIR}/pybind_debug_helper/pybind_debug_helper.cpp)
target_link_libraries(pybind_debug_helper PRIVATE pybind11::embed)
target_include_directories(pybind_debug_helper PRIVATE ${pybind11_INCLUDE_DIRS})
