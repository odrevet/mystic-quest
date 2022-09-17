# Install QuickJS

Download and uncompress QuickJS from https://bellard.org/quickjs/

`make && sudo make install`


# Generate jscript.js and assets from Mystic Quest ROM


jscript.js must be edited to remove integers leading 0 (invald js)

\(0\d

Then move jscript.js in the project directory

# Compile and run

`sh build.sh && ./jreader jscripts.js script_01e7`

# Sources

* https://bellard.org/quickjs/quickjs.html#QuickJS-C-API
* https://linuxtut.com/en/16cdbc69d4fd4a3dccbf/
 * https://github.com/Kozova1/quickjs-example