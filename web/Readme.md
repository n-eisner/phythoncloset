Prerequisites
===
- on Mac OS X/Linux
	1. Latest Python 2.7 (homebrew's `brew install python` on OS X)
- on Windows
	1. Cygwin (for unix compatibility layer)
	2. Latest Python 2.7 version under cygwin
- on BOTH
	1. Fabric
		- `pip install Fabric`
	2. git
		- though package manager, homebrew, or cygwin

Setup
===
1. `git clone ssh://git@24.199.55.106:3412/pyp`
	- use git to clone this directory onto your computer
2. `fab setup_local`
	- it will prompt you to create a superuser for your local install, create one for yourself so you can log in
3. link the data(support) directory to `data` in the top level pyp directory

Put in place test data
===
1. `mkdir ../finance/support`
	- creates the folder support within the folder finance in the same directory the pyp directory is in
2. download [http://arrow.rohunbansal.com/6100904](http://arrow.rohunbansal.com/6100904)
3. extract the zip file into the support directory you created in step 1

Import test data into local database
===
1. `fab import_securities`
2. `fab import_search_data`


Run local development server
===
1. `fab run` or `./server.sh`
2. open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the site
	- any changes you make to the source files will be reloaded automatically

Misc.
===
Enter python virtualenv
---
1. `source venv/bin/activate`
