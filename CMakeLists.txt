# SPDX-License-Identifier: MIT
cmake_minimum_required(VERSION 3.14)

#-------------------------------------------------------------------------------
# PROJECT configuration
#-------------------------------------------------------------------------------
set(Library_NAME Efika CACHE STRING "The name of the main library.")

string(TOLOWER ${Library_NAME} library_NAME)
string(TOUPPER ${Library_NAME} LIBRARY_NAME)

project(${library_NAME}
  VERSION      0.0.1
  DESCRIPTION  "High performance sparse fixed-radius library"
  HOMEPAGE_URL "https://github.com/jiverson002/projects/1"
  LANGUAGES    C)

#-------------------------------------------------------------------------------
# LIBRARY configuration
#-------------------------------------------------------------------------------
add_library(${PROJECT_NAME})
add_library(${Library_NAME}::${library_NAME} ALIAS ${PROJECT_NAME})

set_target_properties(${PROJECT_NAME}
  PROPERTIES SOVERSION ${PROJECT_VERSION_MAJOR}
             VERSION   ${PROJECT_VERSION})

#-------------------------------------------------------------------------------
# INTERNAL DEPENDENCY configuration
#-------------------------------------------------------------------------------
include(FetchContent)

set(EFIKA_CORE_COMPONENTS "apss;core;io" CACHE STRING "The core components to be included when
building the library")

foreach(dep ${EFIKA_CORE_COMPONENTS})
  if (dep STREQUAL "apss")
    FetchContent_Declare(${library_NAME}-${dep}
      GIT_REPOSITORY https://github.com/jiverson002/${library_NAME}-${dep}.git
      GIT_TAG        nova)
  else()
    FetchContent_Declare(${library_NAME}-${dep}
      GIT_REPOSITORY https://github.com/jiverson002/${library_NAME}-${dep}.git)
  endif()

  FetchContent_MakeAvailable(${library_NAME}-${dep})

  # This should be BUILD_INTERFACE only so that these deps aren't required by
  # project linking against. A project that links against, can require that
  # certain components were installed, but shouldn't need to require them all.
  target_link_libraries(${PROJECT_NAME}
    PUBLIC $<BUILD_INTERFACE:${Library_NAME}::${dep}>)
endforeach()

#-------------------------------------------------------------------------------
# PACKAGE configuration
#-------------------------------------------------------------------------------
include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

configure_package_config_file(${Library_NAME}Config.cmake.in
                      cmake/${Library_NAME}Config.cmake
  INSTALL_DESTINATION lib/cmake/${library_NAME})

write_basic_package_version_file(cmake/${Library_NAME}ConfigVersion.cmake
  VERSION       ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion)

install(TARGETS ${PROJECT_NAME} EXPORT ${PROJECT_NAME}Targets
  RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR}
           COMPONENT   ${Library_NAME}_Runtime
  LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
           COMPONENT          ${Library_NAME}_Runtime
           NAMELINK_COMPONENT ${Library_NAME}_Development
  ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
           COMPONENT   ${Library_NAME}_Development
  INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT ${PROJECT_NAME}Targets
  FILE        ${Library_NAME}Targets.cmake
  NAMESPACE   ${Library_NAME}::
  DESTINATION lib/cmake/${library_NAME}
  COMPONENT   ${Library_NAME}_Development)

install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/cmake/
  DESTINATION lib/cmake/${library_NAME}
  COMPONENT   ${Library_NAME}_Development)
