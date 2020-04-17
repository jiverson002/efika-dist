from conans import ConanFile, CMake, tools

class EfikaConan(ConanFile):
  name = "efika"
  version = "0.0.1"
  license = "MIT"
  author = "Jeremy Iverson (jiverson002@csbsju.edu)"
  url = "https://github.com/jiverson002/efika-dist"
  homepage = "https://github.com/users/jiverson002/projects/1"
  description = "High performance sparse fixed-radius library for sparse high-dimensional data."
  topics = ("hpc", "sfr", "apss")
  settings = "os", "compiler", "build_type", "arch"
  options = {
    "shared": [True, False],
    "fPIC": [True, False],
    "visibility": ["hidden", "default"]
  }
  default_options = {
    "shared": False,
    "fPIC": True,
    "visibility": "hidden"
  }
  exports = ["LICENSE"]
  exports_sources = "CMakeLists.txt", "EfikaConfig.cmake.in"

  def build(self):
    cmake = CMake(self)
    cmake.definitions["CMAKE_C_VISIBILITY_PRESET"] = self.options.visibility
    #cmake.verbose = True
    cmake.configure()
    cmake.build()
    #cmake.test()
    cmake.install()

  def package(self):
    self.copy("*.h", dst="include", src="include")
    self.copy("*efika.lib", dst="lib", keep_path=False)
    self.copy("*.dll", dst="bin", keep_path=False)
    self.copy("*.so", dst="lib", keep_path=False)
    self.copy("*.dylib", dst="lib", keep_path=False)
    self.copy("*.a", dst="lib", keep_path=False)
