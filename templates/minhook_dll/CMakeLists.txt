cmake_minimum_required(VERSION 3.20)
project(re_harness_patch_stub LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Placeholder only.
# Wire MinHook, include dirs, target exports and post-build copy steps later.

add_library(re_harness_patch_stub SHARED
  src/dllmain.cpp
  src/hook_entry.cpp
  src/logger.cpp
)

target_include_directories(re_harness_patch_stub PRIVATE include)
