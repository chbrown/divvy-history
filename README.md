## Historical [Divvy](http://divvybikes.com/) [data](http://divvybikes.com/stations/json)

Thanks for the space, GitHub!

    git clone git://github.com/chbrown/divvy-history.git
    cd divvy-history
    git checkout appfog

Run locally (as on appfog):

    pip install -r requirements.txt
    gunicorn -c settings.py wsgi:application

Push to appfog:

    af env-add divvy GITHUB_TOKEN=$GITHUB_TOKEN
    af push divvy

(Current running at http://divvy2.aws.af.cm/.)

Or to run sync and fetch locally, you could set up a crontab like so:

    *  *  * * * cd /home/chbrown/src/divvy-history && ./fetch
    0 */6 * * * cd /home/chbrown/src/divvy-history && ./sync


* `fetch` should run every minute
* `sync` can run however often you like. The above crontab will run it every six hours.


## Patches:

[`patches.json`](patches.json) follows
[RFC 6902](http://tools.ietf.org/html/rfc6902) for describing JSON patches with JSON.


## License

Copyright © 2013 Christopher Brown. [MIT Licensed](LICENSE).
