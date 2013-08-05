## Historical Divvy data

### Setup

    git clone git://github.com/chbrown/divvy-history.git
    cd divvy-history
    python setup.py install

## Scraping

    *  *  * * * /usr/local/bin/divvy fetch
    0 */6 * * * /usr/local/bin/divvy sync

- `divvy fetch` runs every minute.
- `divvy sync` runs every six hours. It could easily run much more often, but I didn't want to flood my GitHub record with 1,440 commits every day.

## Patches

Patching follows [RFC 6902](http://tools.ietf.org/html/rfc6902) for describing JSON patches with JSON.

## License

Copyright © 2013 Christopher Brown. [MIT Licensed](LICENSE).
