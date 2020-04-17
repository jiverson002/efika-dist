[ ![Download](https://api.bintray.com/packages/jiverson002/public-conan/efika%3Ajiverson002/images/download.svg) ](https://bintray.com/jiverson002/public-conan/efika%3Ajiverson002/_latestVersion)

## Conan package recipe for [*Efika*](https://github.com/jiverson002/efika-dist.git)

High performance sparse fixed-radius library for sparse high-dimensional data.

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/jiverson002/public-conan/efika%3Ajiverson002).


## Issues

If you wish to report an issue or make a request for a package, please do so here:

[Issues Tracker](https://github.com/jiverson002/efika-dist/issues)


## For Users

### Basic setup

    $ conan install efika/0.0.1@jiverson002/unstable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    efika/0.0.1@jiverson002/unstable

    [options]
    efika:shared=True # False
    efika:fPIC=False # True
    efika:visibility="default" # "hidden"

    [generators]
    cmake

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and
not the root of the project directory. This is because conan generates
*conanbuildinfo* files specific to a single build configuration which by default
comes from an autodetected default profile located in ~/.conan/profiles/default.
If you pass different build configuration options to conan install, it will
generate different *conanbuildinfo* files. Thus, they should not be added to the
root of the project, nor committed to git.

## Build and package

The following command both runs all the steps of the conan file, and publishes
the package to the local system cache. This includes downloading dependencies
from "build_requires" and "requires", and then running the build() method.

    $ conan create . jiverson002/unstable

## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which
can be used to build and package efika.
It does *not* in any way apply or is related to the actual software being
packaged.

[MIT](LICENSE)
