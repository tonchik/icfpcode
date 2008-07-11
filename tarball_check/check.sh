rm -r icfp08
tar -xzf icfp08.tgz
cd icfp08
if test -x bin/install ; then
bin/install
fi
bin/run