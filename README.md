**rescache** is a simple command line tool for managing the shared resource cache for the EVE Online client.

You run it from the install folder for EVE, in a command window. Run it with no arguments to show a list of commands (and the current cache location).

The rescache tool has the following commands:
* verify - scans all the files in the index and calculates the md5 checksum used to verify the contents of the files. If the checksum for any file doesn't match the index, the file is deleted.
* download - downloads any files listed in the index that are not found in the cache.
* purge - purges any extra files from the cache.
* move - moves the rescache to a new location. This moves the folder itself and updates the registry entry the client uses to find the cache.
* diff - scans the cache against the index and reports the number of files missing and extra files.

Neither the EVE Launcher nor the EVE client should be running while using this tool.
 
