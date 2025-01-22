package bin;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

import fileIO.ByteStreamWriter;
import fileIO.ReadWrite;
import shared.Parse;
import shared.Parser;
import shared.PreParser;
import shared.Shared;
import shared.Timer;
import shared.Tools;
import sketch.DisplayParams;
import sketch.Sketch;
import stream.ConcurrentReadInputStream;
import stream.ConcurrentReadOutputStream;
import stream.Read;
import structures.ByteBuilder;
import structures.ListNum;
import template.Accumulator;
import template.ThreadWaiter;
import tracker.ReadStats;

/**
 * Prototype for metagenome contig binning.
 * 
 * @author Brian Bushnell
 * @date December 6, 2024
 *
 */
public class QuickBin extends BinObject implements Accumulator<QuickBin.ProcessThread> {
	
	/*--------------------------------------------------------------*/
	/*----------------        Initialization        ----------------*/
	/*--------------------------------------------------------------*/
	
	/**
	 * Code entrance from the command line.
	 * @param args Command line arguments
	 */
	public static void main(String[] args){
		//Start a timer immediately upon code entrance.
		Timer t=new Timer();
		
		//Create an instance of this class
		QuickBin x=new QuickBin(args);
		
		//Run the object
		x.process(t);
		
		//Close the print stream if it was redirected
		Shared.closeStream(x.outstream);
	}
	
	/**
	 * Constructor.
	 * @param args Command line arguments
	 */
	public QuickBin(String[] args){
		
		{//Preparse block for help, config files, and outstream
			PreParser pp=new PreParser(args, getClass(), false);
			args=pp.args;
			outstream=pp.outstream;
		}
		
		//Set shared static variables prior to parsing
		ReadWrite.USE_PIGZ=ReadWrite.USE_UNPIGZ=true;
		ReadWrite.setZipThreads(Shared.threads());
		
		{//Parse the arguments
			loader=new DataLoader(outstream);
			binner=new Binner(outstream);
			final Parser parser=parse(args);
			Parser.processQuality();
			
			overwrite=ReadStats.overwrite=parser.overwrite;
			append=ReadStats.append=parser.append;
			
			loader.in1=parser.in1;
			loader.in2=parser.in2;

			outPattern=parser.out1;
			extout=parser.extout;
		}

		validateParams();
		checkFileExistence(); //Ensure files can be read and written
		loader.checkInput();
		
		binner.tree=loader.loadTree();
		sketcher=(sketchContigs || sketchClusters || sketchOutput) ? new BinSketcher(16, 2000) : null;
		binner.sketcher=loader.sketcher=sketcher;
		Sketch.defaultParams.format=DisplayParams.FORMAT_JSON;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------    Initialization Helpers    ----------------*/
	/*--------------------------------------------------------------*/
	
	/** Parse arguments from the command line */
	private Parser parse(String[] args){
		
		//Create a parser object
		Parser parser=new Parser();
		
		//Set any necessary Parser defaults here
		//parser.foo=bar;
		
		//Parse each argument
		for(int i=0; i<args.length; i++){
			String arg=args[i];
			
			//Break arguments into their constituent parts, in the form of "a=b"
			String[] split=arg.split("=");
			String a=split[0].toLowerCase();
			String b=split.length>1 ? split[1] : null;
			if(b!=null && b.equalsIgnoreCase("null")){b=null;}
			
			if(a.equals("verbose")){
				verbose=Parse.parseBoolean(b);
			}
			
			else if(a.equals("clusterbytax") || a.equals("clusterbytaxid")){
				clusterByTaxid=Parse.parseBoolean(b);
			}else if(a.equals("clusterbytet") || a.equals("clusterbytetramer")){
				clusterByTetramer=Parse.parseBoolean(b);
			}else if(a.equals("refine") || a.equals("refineclusters")){
				refineClusters=Parse.parseBoolean(b);
			}
			
			else if(a.equalsIgnoreCase("sketchcontigs")){
				sketchContigs=Parse.parseBoolean(b);
			}else if(a.equalsIgnoreCase("sketchclusters") || a.equalsIgnoreCase("sketchbins")){
				sketchClusters=Parse.parseBoolean(b);
			}else if(a.equalsIgnoreCase("sketchoutput")){
				sketchOutput=Parse.parseBoolean(b);
			}else if(a.equalsIgnoreCase("sketch")){
				sketchClusters=sketchContigs=sketchOutput=Parse.parseBoolean(b);
			}else if(a.equalsIgnoreCase("density")){
				float f=Float.parseFloat(b);
				if(f<1) {sketchDensity=f;}
				else {sketchDensity=1/f;}
				
			}else if(a.equals("sketchbulk") || a.equalsIgnoreCase("sketchinbulk") || a.equals("bulk")){
				sketchInBulk=Parse.parseBoolean(b);
			}else if(a.equals("sketchsectionsize")){
				BinSketcher.sectionSize=Tools.mid(1, Integer.parseInt(b), 10000);
			}else if(a.equals("quant") || a.equals("quantize") || a.equals("quantizer")){
				BinObject.setQuant(Tools.max(1, Integer.parseInt(b)));
			}
			
			else if(a.equals("parse_flag_goes_here")){
				long fake_variable=Parse.parseKMG(b);
				//Set a variable here
			}else if(binner.parse(arg, a, b)){
				//do nothing
			}else if(loader.parse(arg, a, b)){
				//do nothing
			}else if(SimilarityMeasures.parse(arg, a, b)){
				//do nothing
			}else if(parser.parse(arg, a, b)){//Parse standard flags in the parser
				//do nothing
			}else{
				outstream.println("Unknown parameter "+args[i]);
				assert(false) : "Unknown parameter "+args[i];
			}
		}
		
		return parser;
	}
	
	/** Ensure parameter ranges are within bounds and required parameters are set */
	private boolean validateParams(){
//		assert(minfoo>0 && minfoo<=maxfoo) : minfoo+", "+maxfoo;
//		assert(false) : "TODO";
		return true;
	}
	
	/** Ensure files can be read and written */
	private void checkFileExistence(){
		//Ensure output files can be written
		String o=(outPattern!=null && outPattern.indexOf('%')<0) ? outPattern : null;
		if(!Tools.testOutputFiles(overwrite, append, false, o)){
			throw new RuntimeException("\n\noverwrite="+overwrite+"; Can't write to output file "+o+"\n");
		}
	}
	
	/*--------------------------------------------------------------*/
	/*----------------         Outer Methods        ----------------*/
	/*--------------------------------------------------------------*/

	/** Create read streams and process all data */
	void process(Timer t){
		
		Timer t2=new Timer();
		
		contigList=loader.loadData();

		@SuppressWarnings("unchecked")
		ArrayList<? extends Bin> bins=(ArrayList<Contig>) contigList.clone();
		if(clusterByTaxid) {
			bins=binner.clusterByTaxid(bins);
		}
		
		ArrayList<Cluster> clusters;
		if(clusterByTetramer) {
			clusters=binner.makeClusters(bins);
		}else {
			clusters=new ArrayList<Cluster>(bins.size());
			for(Bin b : bins) {clusters.add(b.toCluster(b.id()));}
		}
		
		if(refineClusters) {
			clusters=binner.refineClusters(clusters);
		}
		t2.stop();
		for(int i=0; i<clusters.size(); i++) {clusters.get(i).id=i;}
		
		if(sketchOutput) {
			System.err.println("Sketching output.");
			sketcher.sketch(clusters, true);
		}
		
		System.err.println("\nFinal clusters:");
		for(int i=0; i<clusters.size(); i++) {
			Cluster a=clusters.get(i);
			if(a.size>=4000 || a.contigs.size()>1){
				System.out.println(a.toBytes());
			}
			if(a.size<1000 || i>10) {break;}
		}
		
		outputClusters(outPattern, clusters, minBasesPerCluster, minContigsPerCluster);
//		
//		//Create a read input stream
//		final ConcurrentReadInputStream cris=makeCris(ffin1, ffin2);
//		
//		//Optionally create a read output stream
//		final ConcurrentReadOutputStream ros=makeCros(outPattern);
//		
//		//Reset counters
//		readsProcessed=readsOut=0;
//		basesProcessed=basesOut=0;
//		
//		//Process the reads in separate threads
//		spawnThreads(cris, ros);
		
		if(verbose){outstream.println("Finished; closing streams.");}
		
//		//Write anything that was accumulated by ReadStats
//		errorState|=ReadStats.writeAll();
//		//Close the read streams
//		errorState|=ReadWrite.closeStreams(cris, ros);
		
		//Report timing and results
		outstream.println();
		t.stopAndPrint();
//		outstream.println(Tools.timeReadsBasesProcessed(t, readsProcessed, basesProcessed, 8));
//		outstream.println(Tools.readsBasesOut(readsProcessed, basesProcessed, readsOut, basesOut, 8, false));

		outstream.println("Initial Fast Comparisons:    \t"+binner.initialComparisons);
		outstream.println("Initial Slow Comparisons:    \t"+binner.initialComparisonsSlow);
		outstream.println("Refinement Fast Comparisons: \t"+binner.refinementComparisons);
		outstream.println("Refinement Slow Comparisons: \t"+binner.refinementComparisonsSlow);
		float cps=((binner.initialComparisonsSlow+binner.refinementComparisonsSlow)/(float)t2.elapsed)*1000000000;
		outstream.println("Comparisons Per Second:      \t"+Tools.padKMB((long)cps, 0));
		
		printL90(clusters);
		
		//Throw an exception of there was an error in a thread
		if(errorState){
			throw new RuntimeException(getClass().getName()+" terminated in an error state; the output may be corrupt.");
		}
	}
	
	private void printL90(ArrayList<Cluster> list) {
		long sum=0;
		for(Cluster c : list) {sum+=c.size;}
		long c99=(long)(0.99f*sum);
		long c95=(long)(0.95f*sum);
		long c90=(long)(0.90f*sum);
		long c80=(long)(0.80f*sum);
		long c50=(long)(0.50f*sum);
		
		
		long prev=0, sum2=0;
		for(int i=0; i<list.size(); i++) {
			Cluster c=list.get(i);
			long size=c.size;
			prev=sum2;
			sum2+=size;
			int num=i+1;

			if(sum2>=c99 && prev<c99) {System.err.println("L99: "+size+"\t"+"N99: "+num);}
			if(sum2>=c95 && prev<c95) {System.err.println("L95: "+size+"\t"+"N95: "+num);}
			if(sum2>=c90 && prev<c90) {System.err.println("L90: "+size+"\t"+"N90: "+num);}
			if(sum2>=c80 && prev<c80) {System.err.println("L80: "+size+"\t"+"N80: "+num);}
			if(sum2>=c50 && prev<c50) {System.err.println("L50: "+size+"\t"+"N50: "+num);}
		}
	}
	
	private void outputClusters(String pattern, ArrayList<Cluster> clusters, long minBases, int minContigs) {
//		if(pattern==null) {return;}
		if(pattern!=null) {outstream.println("Writing clusters to "+pattern);}
		
		if(pattern!=null && pattern.indexOf('%')>=0) {
			final ByteStreamWriter chaff=ByteStreamWriter.makeBSW(pattern.replace("%", "chaff"), overwrite, append, true);
			final ByteBuilder bb=new ByteBuilder(8192);
			for(int i=0; i<clusters.size(); i++) {
				Cluster a=clusters.get(i);
				if(a.size>=minBases || a.contigs.size()>=minContigs) {
					String fname=pattern.replace("%", Integer.toString(i));
					final ByteStreamWriter bsw=ByteStreamWriter.makeBSW(fname, overwrite, append, true);
					printCluster(a, bsw, bb, -1);
					bsw.poison();
					clustersWritten++;
					contigsWritten+=a.contigs.size();
					basesWritten+=a.size;
				}else {
					printCluster(a, chaff, bb, i+1);
				}
			}
			chaff.poisonAndWait();
		}else {
			final ByteBuilder bb=new ByteBuilder(8192);
			final ByteStreamWriter bsw=ByteStreamWriter.makeBSW(pattern, overwrite, append, true);
			for(int i=0; i<clusters.size(); i++) {
				Cluster a=clusters.get(i);
				printCluster(a, bsw, bb, i+1);
				clustersWritten++;
				contigsWritten+=a.contigs.size();
				basesWritten+=a.size;
			}
			if(bsw!=null) {bsw.poisonAndWait();}
		}
		float cpct=contigsWritten*100f/loader.contigsLoaded;
		float bpct=basesWritten*100f/loader.basesLoaded;
		outstream.println("\nMetric   \t        In\t       Out\tPercent");
		outstream.println("Clusters \t"+Tools.padLeft(0, 10)+"\t"+Tools.padLeft(clustersWritten, 10));
		outstream.println("Contigs  \t"+Tools.padLeft(loader.contigsLoaded, 10)+"\t"+
				Tools.padLeft(contigsWritten, 10)+"\t"+Tools.format("%.2f%%", cpct));
		outstream.println("Bases    \t"+Tools.padLeft(loader.basesLoaded, 10)+"\t"+
				Tools.padLeft(basesWritten, 10)+"\t"+Tools.format("%.2f%%", bpct));
	}
	
	private void printCluster(Cluster a, ByteStreamWriter bsw, ByteBuilder bb, int id) {
		ArrayList<Contig> contigs=a.contigs;
		Collections.sort(contigs);
		for(Contig c : contigs) {
			c.appendTo(bb, id);
			if(bb.length>4096) {
				if(bsw!=null) {bsw.print(bb);}
				bb.clear();
			}
		}
		if(bsw!=null && !bb.isEmpty()) {bsw.print(bb);}
		bb.clear();
	}
	
//	private ConcurrentReadInputStream makeCris(FileFormat ff1, FileFormat ff2){
//		ConcurrentReadInputStream cris=ConcurrentReadInputStream.getReadInputStream(maxReads, true, ff1, ff2);
//		cris.start(); //Start the stream
//		if(verbose){outstream.println("Started cris");}
//		boolean paired=cris.paired();
////		if(!ffin1.samOrBam()){outstream.println("Input is being processed as "+(paired ? "paired" : "unpaired"));}
//		return cris;
//	}
//	
//	private ConcurrentReadOutputStream makeCros(String fname){
//		if(fname==null) {return null;}
//		FileFormat ff=FileFormat.testOutput(fname, FileFormat.FASTA, null, true, overwrite, append, false);
//
//		//Select output buffer size based on whether it needs to be ordered
//		final int buff=8;
//
//		final ConcurrentReadOutputStream ros=ConcurrentReadOutputStream.getStream(ff, null, buff, null, false);
//		ros.start(); //Start the stream
//		return ros;
//	}
	
	/*--------------------------------------------------------------*/
	/*----------------         Inner Methods        ----------------*/
	/*--------------------------------------------------------------*/
	
	
	
	/*--------------------------------------------------------------*/
	/*----------------       Thread Management      ----------------*/
	/*--------------------------------------------------------------*/
	
	/** Spawn process threads */
	private void spawnThreads(final ConcurrentReadInputStream cris, final ConcurrentReadOutputStream ros){
		
		//Do anything necessary prior to processing
		
		//Determine how many threads may be used
		final int threads=Shared.threads();
		
		//Fill a list with ProcessThreads
		ArrayList<ProcessThread> alpt=new ArrayList<ProcessThread>(threads);
		for(int i=0; i<threads; i++){
			alpt.add(new ProcessThread(cris, ros, i));
		}
		
		//Start the threads and wait for them to finish
		boolean success=ThreadWaiter.startAndWait(alpt, this);
		errorState&=!success;
		
		//Do anything necessary after processing
		
	}
	
	@Override
	public final void accumulate(ProcessThread pt){
		synchronized(pt) {
//			readsProcessed+=pt.readsProcessedT;
//			basesProcessed+=pt.basesProcessedT;
//			readsOut+=pt.readsOutT;
//			basesOut+=pt.basesOutT;
			errorState|=(!pt.success);
		}
	}
	
	@Override
	public final boolean success(){return !errorState;}
	
	/*--------------------------------------------------------------*/
	/*----------------         Inner Classes        ----------------*/
	/*--------------------------------------------------------------*/
	
	/** This class is static to prevent accidental writing to shared variables.
	 * It is safe to remove the static modifier. */
	static class ProcessThread extends Thread {
		
		//Constructor
		ProcessThread(final ConcurrentReadInputStream cris_, final ConcurrentReadOutputStream ros_, final int tid_){
			cris=cris_;
			ros=ros_;
			tid=tid_;
		}
		
		//Called by start()
		@Override
		public void run(){
			//Do anything necessary prior to processing
			
			//Process the reads
			processInner();
			
			//Do anything necessary after processing
			
			//Indicate successful exit status
			success=true;
		}
		
		/** Iterate through the reads */
		void processInner(){
			
			//Grab the first ListNum of reads
			ListNum<Read> ln=cris.nextList();

			//Check to ensure pairing is as expected
			if(ln!=null && !ln.isEmpty()){
				Read r=ln.get(0);
//				assert(ffin1.samOrBam() || (r.mate!=null)==cris.paired()); //Disabled due to non-static access
			}

			//As long as there is a nonempty read list...
			while(ln!=null && ln.size()>0){
//				if(verbose){outstream.println("Fetched "+reads.size()+" reads.");} //Disabled due to non-static access
				
				processList(ln);
				
				//Notify the input stream that the list was used
				cris.returnList(ln);
//				if(verbose){outstream.println("Returned a list.");} //Disabled due to non-static access
				
				//Fetch a new list
				ln=cris.nextList();
			}

			//Notify the input stream that the final list was used
			if(ln!=null){
				cris.returnList(ln.id, ln.list==null || ln.list.isEmpty());
			}
		}
		
		void processList(ListNum<Read> ln){

			//Grab the actual read list from the ListNum
			final ArrayList<Read> reads=ln.list;
			
			//Loop through each read in the list
			for(int idx=0; idx<reads.size(); idx++){
				final Read r1=reads.get(idx);
				final Read r2=r1.mate;
				
				//Validate reads in worker threads
				if(!r1.validated()){r1.validate(true);}
				if(r2!=null && !r2.validated()){r2.validate(true);}

				//Track the initial length for statistics
				final int initialLength1=r1.length();
				final int initialLength2=r1.mateLength();

				//Increment counters
				readsProcessedT+=r1.pairCount();
				basesProcessedT+=initialLength1+initialLength2;
				
				{
					//Reads are processed in this block.
					boolean keep=processReadPair(r1, r2);
					
					if(!keep){reads.set(idx, null);}
					else{
						readsOutT+=r1.pairCount();
						basesOutT+=r1.pairLength();
					}
				}
			}

			//Output reads to the output stream
			if(ros!=null){ros.add(reads, ln.id);}
		}
		
		/**
		 * Process a read or a read pair.
		 * @param r1 Read 1
		 * @param r2 Read 2 (may be null)
		 * @return True if the reads should be kept, false if they should be discarded.
		 */
		boolean processReadPair(final Read r1, final Read r2){
			throw new RuntimeException("TODO: Implement this method."); //TODO
//			return true;
		}

		/** Number of reads processed by this thread */
		protected long readsProcessedT=0;
		/** Number of bases processed by this thread */
		protected long basesProcessedT=0;
		
		/** Number of reads retained by this thread */
		protected long readsOutT=0;
		/** Number of bases retained by this thread */
		protected long basesOutT=0;
		
		/** True only if this thread has completed successfully */
		boolean success=false;
		
		/** Shared input stream */
		private final ConcurrentReadInputStream cris;
		/** Shared output stream */
		private final ConcurrentReadOutputStream ros;
		/** Thread ID */
		final int tid;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------            Fields            ----------------*/
	/*--------------------------------------------------------------*/

	/** Primary output file path; should contain % symbol for bins */
	private String outPattern=null;
	
	/** Override output file extension */
	private String extout=null;
	
	private ArrayList<Contig> contigList;
	private ArrayList<Bin> binList;
	
	int minBasesPerCluster=8000;
	int minContigsPerCluster=2;
	boolean clusterByTaxid=true;
	boolean clusterByTetramer=true;
	boolean refineClusters=true;
	
	/*--------------------------------------------------------------*/

//	/** Number of reads processed */
//	protected long readsProcessed=0;
//	/** Number of bases processed */
//	protected long basesProcessed=0;
//
//	/** Number of reads retained */
//	protected long readsOut=0;
//	/** Number of bases retained */
//	protected long basesOut=0;

	private long clustersWritten=0;
	private long contigsWritten=0;
	private long basesWritten=0;
	
	private DataLoader loader;
	private Binner binner;
	
	/*--------------------------------------------------------------*/
	/*----------------         Final Fields         ----------------*/
	/*--------------------------------------------------------------*/

//	private final Timer phaseTimer=new Timer();
	
	private final BinSketcher sketcher;
	
	@Override
	public final ReadWriteLock rwlock() {return rwlock;}
	private final ReadWriteLock rwlock=new ReentrantReadWriteLock();
	
	/*--------------------------------------------------------------*/
	/*----------------        Common Fields         ----------------*/
	/*--------------------------------------------------------------*/
	
	/** Print status messages to this output stream */
	private PrintStream outstream=System.err;
	/** Print verbose messages */
	public static boolean verbose=false;
	/** True if an error was encountered */
	public boolean errorState=false;
	/** Overwrite existing output files */
	private boolean overwrite=true;
	/** Append to existing output files */
	private boolean append=false;
	
}
