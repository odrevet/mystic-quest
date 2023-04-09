# Install QuickJS

Download and uncompress QuickJS from https://bellard.org/quickjs/

`make && sudo make install`

# Compile

`sh build.sh`

Will generate the `jreader`  binary

# Usage


jreader take as parameter the jscript.js generated from mystic-editor and a function name:

`./jreader jscripts.js script_01e7`


# Sources

* https://bellard.org/quickjs/quickjs.html#QuickJS-C-API
* https://linuxtut.com/en/16cdbc69d4fd4a3dccbf/
* https://github.com/Kozova1/quickjs-example
