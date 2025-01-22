#!/bin/bash

usage(){
echo "
Written by Brian Bushnell
Last modified January 7, 2024

Description:  Bins contigs using coverage, kmer frequencies, and
reference-based sequence comparison using BBSketch.
If reads or covstats are provided, coverage will be calculated from those;
otherwise, it will be parsed from contig headers.

Usage:  quickbin.sh contigs=<file> out=<pattern>

File parameters:
contigs=<file>  (in) Assembly input; only required parameter.
covstats=<file> Covstats file from BBMap or Pileup.
readsin=<file>  Read input (fastq or sam).
readsin2=<file> Read 2 input if fastq reads are in two files.
out=<pattern>   Output pattern.  If this contains a % symbol, like bin%.fa,
                one file will be created per bin.  If not, all contigs will
                be written to the same file, with the name modified to
                indicate their bin number.

Processing parameters:
None yet!

Java Parameters:
-Xmx            This will set Java's memory usage, overriding autodetection.
                -Xmx20g will specify 20 gigs of RAM, and -Xmx200m will
                specify 200 megs. The max is typically 85% of physical memory.
-eoom           This flag will cause the process to exit if an out-of-memory
                exception occurs.  Requires Java 8u92+.
-da             Disable assertions.

Please contact Brian Bushnell at bbushnell@lbl.gov if you encounter any problems.
"
}

#This block allows symlinked shellscripts to correctly set classpath.
pushd . > /dev/null
DIR="${BASH_SOURCE[0]}"
while [ -h "$DIR" ]; do
  cd "$(dirname "$DIR")"
  DIR="$(readlink "$(basename "$DIR")")"
done
cd "$(dirname "$DIR")"
DIR="$(pwd)/"
popd > /dev/null

#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
CP="$DIR""current/"

z="-Xmx4g"
z2="-Xms4g"
set=0

if [ -z "$1" ] || [[ $1 == -h ]] || [[ $1 == --help ]]; then
	usage
	exit
fi

calcXmx () {
	source "$DIR""/calcmem.sh"
	setEnvironment
	parseXmx "$@"
	if [[ $set == 1 ]]; then
		return
	fi
	freeRam 4000m 84
	z="-Xmx${RAM}m"
	z2="-Xms${RAM}m"
}
calcXmx "$@"

quickbin() {
	local CMD="java $EA $EOOM $z -cp $CP bin.QuickBin $@"
	echo $CMD >&2
	eval $CMD
}

quickbin "$@"
