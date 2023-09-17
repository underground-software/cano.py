#!/bin/bash
#
# update_all_remotes.sh
#
# purpose: update all git repos in a directory

# default to /var/git but overwritable by setting
# the value of PRE in the calling environment
PRE=${PRE:-/var/git}

# iterate through git repo root
for x in $(ls $PRE); do 
	# if a directory has a file called 'HEAD',
	# assume it's probably a bare git repository
	if [ -d $PRE/$x ] && [ -f $PRE/$x/HEAD ]; then
		# update in subshell to maintain
		# wokring directory in calling shell
		(
		cd $PRE/$x;
		URL=$(git remote -v | head -n 1 | awk '{ print $2 }')
		TMP=$(mktemp -d)
		# locally clone fresh repo for new changes
		git clone $URL $TMP
		cd $TMP
		# use to force update bare repo
		git push -f $PRE/$x master
		cd
		# and discard after use
		rm -rf $TMP
		)

	fi
done

