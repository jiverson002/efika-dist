# SPDX-License-Identifier: MIT
cmake_minimum_required(VERSION 3.14)

# ...
project(efika
  VERSION 0.0.1
  DESCRIPTION ""
  HOMEPAGE_URL ""
  LANGUAGES C)

# Include build configurations (compiler standards, options, etc.)
if (CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME AND EFIKA_BUILDCONFIG_FILE)
  include(${EFIKA_BUILDCONFIG_FILE})
endif()

# Include required CMake modules
include(CMakePackageConfigHelpers)
include(GNUInstallDirs)
include(FetchContent)

#-------------------------------------------------------------------------------
# LIBRARY configuration
#-------------------------------------------------------------------------------
add_library(${PROJECT_NAME})

add_library(Efika::efika ALIAS ${PROJECT_NAME})

set_target_properties(${PROJECT_NAME} PROPERTIES
  SOVERSION     ${PROJECT_VERSION_MAJOR}
  VERSION       ${PROJECT_VERSION})

#-------------------------------------------------------------------------------
# COMPONENT configuration (must be included in this order, so as to correctly
# build the public header)
#-------------------------------------------------------------------------------
foreach(component core impl io)
  FetchContent_Declare(Efika-${component}
    GIT_REPOSITORY git@github.com:jiverson002/efika-${component}.git)

  FetchContent_MakeAvailable(efika-${component})

  target_sources(${PROJECT_NAME}
    PRIVATE $<TARGET_OBJECTS:Efika::${component}>)

  list(APPEND PROJECT_INCLUDE_DIRECTORIES
    $<TARGET_PROPERTY:Efika::${component},INTERFACE_INCLUDE_DIRECTORIES>)
endforeach()

# Add trailing '/' to each directory in the list to prevent CMake from appending
# the directory name to eh CMAKE_INSTALL_INCLUDEDIR.
list(TRANSFORM PROJECT_INCLUDE_DIRECTORIES APPEND "/")

#-------------------------------------------------------------------------------
# PACKAGE configuration
#-------------------------------------------------------------------------------
write_basic_package_version_file(EfikaConfigVersion.cmake
  VERSION       ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion)

install(TARGETS ${PROJECT_NAME} EXPORT EfikaTargets
  RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR}
           COMPONENT   Efika_Runtime
  LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
           COMPONENT          Efika_Runtime
           NAMELINK_COMPONENT Efika_Development
  ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
           COMPONENT   Efika_Development
  INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT EfikaTargets
  FILE        EfikaTargets.cmake
  NAMESPACE   Efika::
  DESTINATION lib/cmake/Efika)

install(DIRECTORY ${PROJECT_INCLUDE_DIRECTORIES}
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  COMPONENT   Efika_Development)

install(
  FILES       EfikaConfig.cmake
              ${CMAKE_CURRENT_BINARY_DIR}/EfikaConfigVersion.cmake
  DESTINATION lib/cmake/Efika
  COMPONENT   Efika_Development)
