## Historical Divvy data

Thanks, Github.

    git clone git://github.com/chbrown/divvy-history.git
    cd divvy-history
    pip install -r requirements.txt
    ./cycle

## Collection practice:

Here's my `crontab -l` on an EC2 machine:

    *  *  * * * cd /home/chbrown/src/divvy-history && ./patch
    0 */6 * * * cd /home/chbrown/src/divvy-history && ./push

`patch` runs every minute, `push` runs every six hours.
`push` could easily run much more often, but I didn't want to flood my GitHub record with 1,440 commits every day.

## Patches:

[`patches.json`](patches.json) follows [RFC 6902](http://tools.ietf.org/html/rfc6902) for describing JSON patches with JSON.

Until 2013-07-05, there was not necessarily one line (one patch) per minute; if there was only one patch entry (for the `executionTime`, which *does* change every minute), but no change to any station's `availableBikes` or other similarly significant value, that fetch would simply be ignored.

## TODO

1. After retrofitting is complete and we're entirely on the daily schedule:
    * Delete `patch`
    * Update crontab (to use `fetch` instead of `patch`)
    * Remove "requests" from `requirements.txt`

## License

Copyright © 2013 Christopher Brown. [MIT Licensed](LICENSE).
