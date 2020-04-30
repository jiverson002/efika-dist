# SPDX-License-Identifier: MIT
cmake_minimum_required(VERSION 3.14)

# ...
project(Efika
  VERSION      0.0.1
  DESCRIPTION  "High performance sparse fixed-radius library"
  HOMEPAGE_URL "https://github.com/jiverson002/projects/1"
  LANGUAGES    C)

string(TOLOWER ${PROJECT_NAME} library_name)

# Include required CMake modules
include(CMakePackageConfigHelpers)
include(FetchContent)
include(GNUInstallDirs)

#-------------------------------------------------------------------------------
# LIBRARY configuration
#-------------------------------------------------------------------------------
add_library(${library_name})

add_library(${PROJECT_NAME}::${library_name} ALIAS ${library_name})

set_target_properties(${library_name} PROPERTIES
  SOVERSION ${PROJECT_VERSION_MAJOR}
  VERSION   ${PROJECT_VERSION})

#-------------------------------------------------------------------------------
# COMPONENT configuration
#-------------------------------------------------------------------------------
foreach(component apss core io)
  FetchContent_Declare(${library_name}-${component}
    GIT_REPOSITORY git@github.com:jiverson002/${library_name}-${component}.git)

  FetchContent_MakeAvailable(${library_name}-${component})

  target_sources(${library_name}
    PRIVATE $<TARGET_OBJECTS:${PROJECT_NAME}::${component}>)

  list(APPEND PROJECT_INCLUDE_DIRECTORIES
    ${${library_name}-${component}_SOURCE_DIR}/include)
endforeach()

# Add trailing '/' to each directory in the list to prevent CMake from appending
# the directory name to eh CMAKE_INSTALL_INCLUDEDIR.
list(TRANSFORM PROJECT_INCLUDE_DIRECTORIES APPEND "/")

#-------------------------------------------------------------------------------
# PACKAGE configuration
#-------------------------------------------------------------------------------
configure_package_config_file(${PROJECT_NAME}Config.cmake.in
                      cmake/${PROJECT_NAME}Config.cmake
  INSTALL_DESTINATION lib/cmake/${library_name})

write_basic_package_version_file(cmake/${PROJECT_NAME}ConfigVersion.cmake
  VERSION       ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion)

install(TARGETS ${library_name} EXPORT ${PROJECT_NAME}Targets
  RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR}
           COMPONENT   ${PROJECT_NAME}_Runtime
  LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
           COMPONENT          ${PROJECT_NAME}_Runtime
           NAMELINK_COMPONENT ${PROJECT_NAME}_Development
  ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
           COMPONENT   ${PROJECT_NAME}_Development
  INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT ${PROJECT_NAME}Targets
  FILE        ${PROJECT_NAME}Targets.cmake
  NAMESPACE   ${PROJECT_NAME}::
  DESTINATION lib/cmake/${library_name}
  COMPONENT   ${PROJECT_NAME}_Development)

install(DIRECTORY ${PROJECT_INCLUDE_DIRECTORIES}
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  COMPONENT   ${PROJECT_NAME}_Development)

install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/cmake/
  DESTINATION lib/cmake/${library_name}
  COMPONENT   ${PROJECT_NAME}_Development)
