Fast code grepper
=

In preliminary tests, this appears to run about ten times as fast as
[Ack](http://beyondgrep.com/). This is my attempt at a programming grep
tool that is as fast as possible.

Indexing is done on triplets of ASCII characters. These are used to build
a search tree for each directory in the code base, which becomes a hidden
subdirectory called ".codegrep.index". The contents of this subdirectory
are a list of the files searched, and the search tree split out into
individual files by the decimal ASCII value of first character.

To use this, do the following.

* Put `cgrep` in your path.
* Set the environment variable `CODEGREPROOT` to the root of the directory
  tree you want to search.
* Run `build_c.sh` to build a C module that accelerates the indexer.
* Run `indexer.py` to index the files to be searched. For a large code base
  this is going to take some time.
* Now you can do searches like this:

```bash
cgrep foobar
```