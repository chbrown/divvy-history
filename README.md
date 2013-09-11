## Historical Divvy data

### Setup

    git clone git://github.com/chbrown/divvy-history.git
    cd divvy-history
    python setup.py install


## Scraping

    *  *  * * * /usr/local/bin/divvy fetch
    0 */6 * * * /usr/local/bin/divvy push

- `divvy fetch` runs every minute.
- `divvy push` runs every six hours. It could easily run much more often, but I didn't want to flood my GitHub record with 1,440 commits every day.


## Patches

Patching follows [RFC 6902](http://tools.ietf.org/html/rfc6902) for describing JSON patches with JSON.


## OS-specific installation

On built-in Python in Arch Linux you might want to use the following instead:

    python2 setup.py develop --script-dir=/usr/local/bin


## License

Copyright © 2013 Christopher Brown. [MIT Licensed](LICENSE).
