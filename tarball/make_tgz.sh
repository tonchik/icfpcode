#!/usr/bin/sh
NAME=icfp08
rm -f $NAME.tgz
tar cf - $NAME/ | gzip > $NAME.tgz
