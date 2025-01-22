package bin;

import java.io.File;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map.Entry;

import bloom.BloomFilter;
import bloom.KmerCountAbstract;
import fileIO.ByteFile;
import fileIO.FileFormat;
import shared.LineParser2;
import shared.LineParserS1;
import shared.LineParserS4;
import shared.Parse;
import shared.Shared;
import shared.Timer;
import shared.Tools;
import stream.ConcurrentReadInputStream;
import stream.FASTQ;
import stream.FastaReadInputStream;
import stream.Read;
import stream.SamLine;
import stream.SamLineStreamer;
import structures.ListNum;
import tax.TaxTree;
import ukmer.Kmer;

public class DataLoader extends BinObject {
	
	/*--------------------------------------------------------------*/
	/*----------------        Initialization        ----------------*/
	/*--------------------------------------------------------------*/
	
	DataLoader(PrintStream outstream_){outstream=outstream_;}
	
	boolean parse(String arg, String a, String b) {
	
		if(a.equals("tree")){
			if(b==null || b.equalsIgnoreCase("t") || b.equalsIgnoreCase("true")) {
				treePath="auto";
			}else if(b.equalsIgnoreCase("f") || b.equalsIgnoreCase("false")) {
				treePath=null;
			}else {
				treePath=b;
			}
		}else if(a.equals("reads")){
			maxReads=Parse.parseKMG(b);
		}
		
		else if(a.equals("bloomk") || a.equals("kbloom")){
			bloomkbig=Integer.parseInt(b);
			bloomkbig=Kmer.getKbig(bloomkbig);
		}else if(a.equals("bits") || a.equals("cbits")){
			cbits=Integer.parseInt(b);
		}else if(a.equals("ref") || a.equals("contigs") || a.equals("scaffolds") || a.equals("in")){
			ref=b;
		}else if(a.equals("readsin") || a.equals("reads1") || a.equals("read1") || a.equals("readsin1") || a.equals("in1") || a.equals("input1")){
			in1=b;
		}else if( a.equals("reads2") || a.equals("read2") || a.equals("readsin2") || a.equals("in2") || a.equals("input2")){
			in2=b;
		}else if(a.equals("cov") || a.equals("covstats")){
			covstats=b;
		}else if(a.equals("ignoremissingcontigs")){
			ignoreMissingContigs=Parse.parseBoolean(b);
		}else if(a.equals("hashes")){
			hashes=Integer.parseInt(b);
		}
		
		else {return false;}
		
		return true;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------          Validation          ----------------*/
	/*--------------------------------------------------------------*/
	
	void checkInput() {
		ffin1=FileFormat.testInput(in1, FileFormat.FASTQ, null, true, true);
		ffin2=FileFormat.testInput(in2, FileFormat.FASTQ, null, true, true);

		if(ref==null && ffin1!=null && ffin2==null && ffin1.fasta()) {
			ref=in1;
			in1=in2=null;
			ffin1=ffin2=null;
		}
		assert(ref!=null) : "An assembly is required; specify it with the 'ref=' flag.";

		doPoundReplacement(); //Replace # with 1 and 2
		adjustInterleaving(); //Make sure interleaving agrees with number of input and output files
		fixExtensions(); //Add or remove .gz or .bz2 as needed
		checkFileExistence(); //Ensure files can be read and written
		checkStatics(); //Adjust file-related static fields as needed for this program
	}
	
	/** Replace # with 1 and 2 in headers */
	private void doPoundReplacement(){
		//Do input file # replacement
		if(in1!=null && in2==null && in1.indexOf('#')>-1 && !new File(in1).exists()){
			in2=in1.replace("#", "2");
			in1=in1.replace("#", "1");
		}
		
		//Ensure there is an input file
//		if(in1==null){throw new RuntimeException("Error - at least one input file is required.");}
	}
	
	/** Add or remove .gz or .bz2 as needed */
	private void fixExtensions(){
		in1=Tools.fixExtension(in1);
		in2=Tools.fixExtension(in2);
	}
	
	/** Ensure files can be read and written */
	private void checkFileExistence(){
		//Ensure input files can be read
		if(!Tools.testInputFiles(false, true, in1, in2, ref, covstats)){
			throw new RuntimeException("\nCan't read some input files.\n");  
		}
		
		//Ensure that no file was specified multiple times
		if(!Tools.testForDuplicateFiles(true, in1, in2, ref, covstats)){
			throw new RuntimeException("\nSome file names were specified multiple times.\n");
		}
	}
	
	/** Make sure interleaving agrees with number of input and output files */
	private void adjustInterleaving(){
		//Adjust interleaved detection based on the number of input files
		if(in2!=null){
			if(FASTQ.FORCE_INTERLEAVED){outstream.println("Reset INTERLEAVED to false because paired input files were specified.");}
			FASTQ.FORCE_INTERLEAVED=FASTQ.TEST_INTERLEAVED=false;
		}
	}
	
	/** Adjust file-related static fields as needed for this program */
	private static void checkStatics(){
		//Adjust the number of threads for input file reading
		if(!ByteFile.FORCE_MODE_BF1 && !ByteFile.FORCE_MODE_BF2 && Shared.threads()>2){
			ByteFile.FORCE_MODE_BF2=true;
		}
		
		assert(FastaReadInputStream.settingsOK());
	}
	
	/*--------------------------------------------------------------*/
	/*----------------            Wrapper           ----------------*/
	/*--------------------------------------------------------------*/
	
	ArrayList<Contig> loadData() {
		//Turn off read validation in the input threads to increase speed
		final boolean vic=Read.VALIDATE_IN_CONSTRUCTOR;
		Read.VALIDATE_IN_CONSTRUCTOR=Shared.threads()<4;
		
		HashMap<String, Contig> contigMap=null;
		if(covstats!=null) {
			contigMap=makeContigMap(ref, minContigToLoad);
			calcDepthFromCovStats(covstats, contigMap, minContigToLoad);
		}else if(ffin1!=null && ffin1.samOrBam()) {
			contigMap=makeContigMap(ref, minContigToLoad);
			calcDepthFromSam(ffin1, contigMap);
		}
		
		ArrayList<Contig> contigList=(contigMap!=null ? new ArrayList<Contig>(contigMap.values()) : 
			makeContigList(ref, minContigToLoad));
		contigMap=null;
		Collections.sort(contigList);
		
		if(ffin1==null && !depthCalculated) {
			calcDepthFromHeader(contigList);
		}else if(ffin1!=null && !ffin1.samOrBam() && !depthCalculated) {
			BloomFilter bloomFilter=makeBloomFilter(in1, in2);
			calcDepthFromBloomFilter(contigList, bloomFilter);
			bloomFilter=null;
		}
		assert(depthCalculated);
		
		
		if(sketchContigs) {
			System.err.println("Sketching contigs. ");
			sketcher.sketch(contigList, true);
		}
		
		makeSpectra(contigList);//Done last because it needs memory
		
		//Reset read validation
		Read.VALIDATE_IN_CONSTRUCTOR=vic;
		return contigList;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------         Data Loading         ----------------*/
	/*--------------------------------------------------------------*/
	
	TaxTree loadTree() {
		if("auto".equals(treePath)){treePath=TaxTree.defaultTreeFile();}
		if(treePath!=null) {
			tree=TaxTree.loadTaxTree(treePath, outstream, false, false);
		}
		return tree;
	}
	
	HashMap<String, Contig> makeContigMap(String fname, int minlen){
		outstream.print("Loading contigs:\t");
		phaseTimer.start();
		FileFormat ff=FileFormat.testInput(fname, FileFormat.FASTA, null, true, true);
		HashMap<String, Contig> map=new HashMap<String, Contig>();

		ConcurrentReadInputStream cris=ConcurrentReadInputStream.getReadInputStream(maxReads, true, ff, null);
		cris.start(); //Start the stream
		if(verbose){outstream.println("Started cris");}
		
		//Grab the first ListNum of reads
		ListNum<Read> ln=cris.nextList();

		//Check to ensure pairing is as expected
		if(ln!=null && !ln.isEmpty()){
			Read r=ln.get(0);
			assert(r.mate==null);
		}

		//As long as there is a nonempty read list...
		while(ln!=null && ln.size()>0){
			
			for(Read r : ln) {
				contigsLoaded++;
				basesLoaded+=r.length();
				if(r.length()>=minlen) {
					Contig c=new Contig(r.name(), r.bases, (int)(r.numericID));
					assert(!map.containsKey(c.name)) : "Duplicate contig name: "+c.name;
					map.put(c.name, c);
				}
			}
			
			//Notify the input stream that the list was used
			cris.returnList(ln);
//			if(verbose){outstream.println("Returned a list.");} //Disabled due to non-static access
			
			//Fetch a new list
			ln=cris.nextList();
		}

		//Notify the input stream that the final list was used
		if(ln!=null){
			cris.returnList(ln.id, ln.list==null || ln.list.isEmpty());
		}
		phaseTimer.stopAndPrint();
		return map;
	}
	
	ArrayList<Contig> makeContigList(String fname, int minlen){
		assert(fname!=null) : "No contigs specified.";
		outstream.print("Loading contigs:\t");
		phaseTimer.start();
		FileFormat ff=FileFormat.testInput(fname, FileFormat.FASTA, null, true, true);
		ArrayList<Contig> list=new ArrayList<Contig>();

		ConcurrentReadInputStream cris=ConcurrentReadInputStream.getReadInputStream(maxReads, true, ff, null);
		cris.start(); //Start the stream
		if(verbose){outstream.println("Started cris");}
		
		//Grab the first ListNum of reads
		ListNum<Read> ln=cris.nextList();

		//Check to ensure pairing is as expected
		if(ln!=null && !ln.isEmpty()){
			Read r=ln.get(0);
			assert(r.mate==null);
		}

		//As long as there is a nonempty read list...
		while(ln!=null && ln.size()>0){
			
			for(Read r : ln) {
				contigsLoaded++;
				basesLoaded+=r.length();
				if(r.length()>=minlen) {
					Contig c=new Contig(r.name(), r.bases, (int)(r.numericID));
					list.add(c);
				}
			}
			
			//Notify the input stream that the list was used
			cris.returnList(ln);
//			if(verbose){outstream.println("Returned a list.");} //Disabled due to non-static access
			
			//Fetch a new list
			ln=cris.nextList();
		}

		//Notify the input stream that the final list was used
		if(ln!=null){
			cris.returnList(ln.id, ln.list==null || ln.list.isEmpty());
		}
		phaseTimer.stopAndPrint();
		return list;
	}
	
	BloomFilter makeBloomFilter(String in1, String in2) {
//		if(ffin1.samOrBam()) {return null;}
		outstream.print("Making Bloom filter: \t");
		KmerCountAbstract.CANONICAL=true;
		bloomkbig=Kmer.getKbig(bloomkbig);
		int bloomk=Kmer.getK(bloomkbig);
		BloomFilter filter=new BloomFilter(in1, in2, null, bloomk, bloomkbig, cbits, hashes, 1,
				true, false, false, 0.5f);
		phaseTimer.stopAndPrint();
		outstream.println(filter.filter.toShortString());
		return filter;
	}
	
	void calcDepthFromCovStats(String fname, HashMap<String, Contig> contigMap, int minlen) {
		ByteFile bf=ByteFile.makeByteFile(fname, true);
		outstream.print("Loading covstats file ("+fname+"): \t");
		byte[] line=null;
		LineParser2 lp=new LineParser2('\t');
		int found=0;
		for(line=bf.nextLine(); line!=null; line=bf.nextLine()){
			if(Tools.startsWith(line, '#')) {
				//header
				assert(Tools.startsWith(line, "#ID\tAvg_fold")) : new String(line);
			}else {
				lp.set(line);
				String name=lp.parseString();
				float depth=lp.parseFloat();
				Contig c=contigMap.get(name);
				assert(c!=null || minlen>0 || ignoreMissingContigs) : "Can't find contig that is specified in covstats: "+name;
				if(c!=null) {
					if(c!=null) {
						c.depth=depth;
						found++;
					}
				}
			}
		}
		assert(found<=contigMap.size()) : "Duplicate entries found in covstats file.";
		assert(found==contigMap.size() || minlen>0) : "Some contigs were not found in covstats file.";
		assert(found>0) : "No matching entries found in covstats file.";
		depthCalculated=true;
		phaseTimer.stopAndPrint();
	}
	
	void calcDepthFromSam(FileFormat ff, HashMap<String, Contig> contigMap) {
		SamLineStreamer ss=null;
		outstream.print("Loading sam file: \t");
		final int streamerThreads=Tools.min(4, Shared.threads());
		ss=new SamLineStreamer(ff, streamerThreads, false, maxReads);
		ss.start();
		processSam(ss, contigMap);
		for(Entry<String, Contig> e : contigMap.entrySet()) {
			Contig c=e.getValue();
			c.depth=c.depthSum/(Tools.max(1f, c.bases.length));
		}
		depthCalculated=true;
		phaseTimer.stopAndPrint();
	}
	
	private void processSam(SamLineStreamer ss, HashMap<String, Contig> contigMap) {
		ListNum<SamLine> ln=ss.nextLines();
		ArrayList<SamLine> reads=(ln==null ? null : ln.list);

		while(ln!=null && reads!=null && reads.size()>0){

			for(int idx=0; idx<reads.size(); idx++){
				SamLine sl=reads.get(idx);
				if(sl.mapped()) {
					String rname=sl.rnameS();
					Contig c=contigMap.get(rname);
					assert(c!=null) : "Can't find contig for rname "+rname;
					c.depthSum+=sl.length();
				}
			}
			ln=ss.nextLines();
			reads=(ln==null ? null : ln.list);
		}
	}
	
	public void calcDepthFromHeader(Collection<Contig> list) {
		outstream.print("Parsing depth from contig headers: \t");
		LineParserS1 lps=new LineParserS1('_');
		LineParserS4 lpt=new LineParserS4(",,=,");
		for(Contig c : list) {c.depth=parseDepth(c.name, lps, lpt);}
		depthCalculated=true;
		phaseTimer.stopAndPrint();
	}
	
	//Spades: NODE_1_length_954719_cov_311.305635
	//Tadpole: >contig_0,length=170913,cov=101.4,min=166,max=189,...
	public static float parseDepth(String name) {
		float depth=0;
		if(name.startsWith("NODE_") && name.contains("_cov_")){
			LineParserS1 lp=new LineParserS1('_');
			lp.set(name);
			depth=lp.parseFloat(5);
		}else if(name.startsWith("contig_") && name.contains(",cov=")) {
			LineParserS4 lp=new LineParserS4(",,=,");
			lp.set(name);
			depth=lp.parseFloat(3);
		}
		return depth;
	}
	
	public static float parseDepth(String name, LineParserS1 lps, LineParserS4 lpt) {
		float depth=0;
		if(name.startsWith("NODE_") && name.contains("_cov_")){
			lps.set(name);
			depth=lps.parseFloat(5);
		}else if(name.startsWith("contig_") && name.contains(",cov=")) {
			lpt.set(name);
			depth=lpt.parseFloat(3);
		}
		return depth;
	}
	
	public void calcDepthFromBloomFilter(Collection<Contig> list, BloomFilter bf) {
		outstream.print("Calculating depth from Bloom filter: \t");
		for(Contig c : list) {c.depth=bf.averageCount(c.bases);}
		depthCalculated=true;
		phaseTimer.stopAndPrint();
	}
	
	public void makeSpectra(ArrayList<Contig> list) {
		outstream.print("Calculating kmer frequency spectra: \t");
		phaseTimer.start();
		for(Contig c : list) {
			c.loadCounts();
			assert(c.counts!=null && c.kmers>0);
		}
		phaseTimer.stopAndPrint();
	}
	
	/*--------------------------------------------------------------*/
	/*----------------            Fields            ----------------*/
	/*--------------------------------------------------------------*/

	/** Assembly path */
	String ref=null;
	
	private String covstats=null;
	
	/** Primary read input file path */
	String in1=null;
	/** Secondary read input file path */
	String in2=null;
	
	/** Primary read input file */
	FileFormat ffin1;
	/** Secondary read input file */
	FileFormat ffin2;
	
	boolean depthCalculated=false;
	boolean ignoreMissingContigs=false;
	
	long contigsLoaded=0;
	long basesLoaded=0;
	
	private int bloomkbig=31;
	private int cbits=16;
	private int hashes=3;
	
	BinSketcher sketcher;

	int minContigToLoad=0;
	
	/** Quit after processing this many input reads; -1 means no limit */
	private long maxReads=-1;
	
	String treePath="auto";
	TaxTree tree;
	
	/*--------------------------------------------------------------*/
	/*----------------         Final Fields         ----------------*/
	/*--------------------------------------------------------------*/
	
	final Timer phaseTimer=new Timer();
	final PrintStream outstream;
	
}
