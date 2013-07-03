## Historical Divvy data

Thanks, Github.

    git clone git://github.com/chbrown/divvy-history.git
    cd divvy-history
    pip install -r requirements.txt
    ./cycle

Or add these via `crontab -e`:

    * * * * * cd /usr/local/divvy-history && ./cycle >>/tmp/cron.log 2>&1
    0 */12 * * * cd /usr/local/divvy-history && ./commit

## License

Copyright © 2013 Christopher Brown. [MIT Licensed](LICENSE).
