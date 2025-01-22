package bin;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

import shared.Timer;
import shared.Tools;
import tax.TaxTree;

public class Binner extends BinObject {
	
	/*--------------------------------------------------------------*/
	/*----------------        Initialization        ----------------*/
	/*--------------------------------------------------------------*/
	
	Binner(PrintStream outstream_){outstream=outstream_;}
	
	boolean parse(String arg, String a, String b) {
	
		if(a.equalsIgnoreCase("productMult")){
			productMult=Float.parseFloat(b);
		}

		else if(a.equalsIgnoreCase("maxDif0")){
			maxDif0=Float.parseFloat(b);
		}else if(a.equalsIgnoreCase("maxRatio0")){
			maxRatio0=Float.parseFloat(b);
		}else if(a.equalsIgnoreCase("maxGCDif0")){
			maxGCDif0=Float.parseFloat(b);
		}

		else if(a.equalsIgnoreCase("maxDif1")){
			maxDif1=Float.parseFloat(b);
		}else if(a.equalsIgnoreCase("maxRatio1")){
			maxRatio1=Float.parseFloat(b);
		}else if(a.equalsIgnoreCase("maxGCDif1")){
			maxGCDif1=Float.parseFloat(b);
		}

		else if(a.equalsIgnoreCase("maxDif2")){
			maxDif2=Float.parseFloat(b);
		}else if(a.equalsIgnoreCase("maxRatio2")){
			maxRatio2=Float.parseFloat(b);
		}else if(a.equalsIgnoreCase("maxGCDif2")){
			maxGCDif2=Float.parseFloat(b);
		}
		
		else {return false;}
		
		return true;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------            Binning           ----------------*/
	/*--------------------------------------------------------------*/
	
	public ArrayList<Cluster> makeClusters(ArrayList<? extends Bin> bins) {
		outstream.print("Making clusters from contig comparison: \t");
		phaseTimer.start();
//		Collections.sort(contigs); //Assume sorted
		ArrayList<Cluster> clusters=new ArrayList<Cluster>(1024);
		for(Bin c : bins) {
//			assert(c.counts!=null) : c.name();
			Cluster a=findBestCluster(c, clusters);
//			for(Cluster b : clusters) {assert(b!=null);}
			if(a==null) {
				a=c.toCluster(clusters.size());
				assert(a.counts!=null);
				clusters.add(a);
			}else {
				assert(a.counts!=null);
				a.add(c);
			}
		}
		Collections.sort(clusters);
		for(int i=0; i<clusters.size(); i++) {
			Cluster a=clusters.get(i);
			assert(a!=null);
			a.id=i;
		}
		phaseTimer.stopAndPrint();
		outstream.println("Made "+clusters.size()+" clusters from "+bins.size()+" elements.");
		return clusters;
	}
	
	public ArrayList<Cluster> refineClusters(ArrayList<Cluster> clusters) {
		System.err.println("Merging clusters.");

		if(sketchClusters) {sketcher.sketch(clusters, false);}
		else {
			for(Cluster c : clusters) {
				if(c.sketchedSize()>=2*c.size()) {c.clearTax();}
			}
		}
		phaseTimer.start();
//		for(int pass=1; pass<=20; pass++) {
//			int initial=clusters.size();
//			int removed=refineClustersPass(clusters, 2.5f, 1, TaxTree.SPECIES, false, false);
//			if(removed<1) {break;}
//			System.err.println("Refinement Pass "+pass+"a: Merged "+removed+"/"+initial+" clusters.");
//			if(sketchClusters) {sketcher.sketch(clusters, false);}
//		}
		int removedThisPhase=0;
		for(int pass=1; pass<=20; pass++) {
			int initial=clusters.size();
			int removed=refineClustersPass(clusters, 2.5f, Integer.MAX_VALUE, TaxTree.SPECIES, false, false);
			removedThisPhase+=removed;
			if(removed<1) {break;}
			System.err.println("Refinement Pass "+pass+"b: Merged "+removed+"/"+initial+" clusters.");
		}
		if(sketchClusters && removedThisPhase>0) {sketcher.sketch(clusters, false);}
		removedThisPhase=0;
		
		for(int pass=1; pass<=20; pass++) {
			int initial=clusters.size();
			int removed=refineClustersPass(clusters, 1.5f, Integer.MAX_VALUE, TaxTree.SPECIES, true, false);
			removedThisPhase+=removed;
			if(removed<1) {break;}
			System.err.println("Refinement Pass "+pass+"c: Merged "+removed+"/"+initial+" clusters.");
		}
		if(sketchClusters && removedThisPhase>0) {sketcher.sketch(clusters, false);}
		removedThisPhase=0;
		
		for(int pass=1; pass<=20; pass++) {
			int initial=clusters.size();
			int removed=refineClustersPass(clusters, 1.0f, Integer.MAX_VALUE, TaxTree.GENUS, true, true);
			removedThisPhase+=removed;
			if(removed<1) {break;}
			System.err.println("Refinement Pass "+pass+"d: Merged "+removed+"/"+initial+" clusters.");
		}
		if(sketchClusters && removedThisPhase>0) {sketcher.sketch(clusters, false);}
		removedThisPhase=0;
		
		for(int pass=1; pass<=20; pass++) {
			int initial=clusters.size();
			int removed=refineClustersPass(clusters, 1f, Integer.MAX_VALUE, -1, true, true);
			removedThisPhase+=removed;
			if(removed<1) {break;}
			System.err.println("Refinement Pass "+pass+"e: Merged "+removed+"/"+initial+" clusters.");
		}
		phaseTimer.stopAndPrint();
		return clusters;
	}
	
	public int refineClustersPass(ArrayList<Cluster> clusters, float stringency, int maxSizeToScan, int taxlevel, boolean allowNoTaxID, boolean allowHalfTaxID) {
		
		int removed=0;
		for(int i=clusters.size()-1; i>0; i--) {
			Cluster a=clusters.get(i);
			assert(a.id==i);
			if(a.numContigs()<=maxSizeToScan) {
				Cluster b=findBestCluster(a, clusters, stringency, i, taxlevel, allowNoTaxID, allowHalfTaxID);
				if(b!=null) {
					b.add(a);
					clusters.set(i, null);
					removed++;
				}
			}
		}
		if(removed>0) {
			Tools.condenseStrict(clusters);
			Collections.sort(clusters);
			for(int i=0; i<clusters.size(); i++) {clusters.get(i).id=i;}
		}
		return removed;
	}
	
	public Cluster findBestCluster(Bin c, ArrayList<Cluster> clusters) {
		//Decreasing pressure to make new clusters as the number of clusters grows.
		float mult=Tools.min(1f, (clusters.size()+64)/256f);
		if(c.size()<2000) {mult*=1.1f;}
		if(c.size()<1000) {mult*=1.1f;}
		if(c.size()<500) {mult*=1.1f;}
		if(c.depth<3.0f) {mult*=1.1f;}
		float maxDif=maxDif1*mult;
		float maxRatio=maxRatio1*mult;
		float maxProduct0=maxDif0*maxRatio0*productMult;
		float maxProduct=maxDif1*maxRatio1*productMult*mult;
		float maxGCDif=maxGCDif1;
		
		final float d=c.depth+.5f;
		final float gc=c.gc();
		Cluster best=null;
		float bestDif=10000;//Lower is better
		float bestRatio=10000;//Lower is better
		float bestProduct=10000;//Lower is better
		
		for(Cluster b : clusters) {
			if(b.size<1000) {break;}//Don't compare to tiny stuff
			initialComparisons++;
			final float d2=b.depth+0.5f;
			final float ratio=Tools.max(d, d2)/Tools.min(d, d2);
			final float gcDif=Math.abs(gc-b.gc());
			if(ratio>=maxRatio || gcDif>=maxGCDif) {continue;}
			if(c.size()>=8000 && b.size()>=8000 && c.taxid>0 && c.taxid==b.taxid) {return b;}
			initialComparisonsSlow++;
			final float simDif=SimilarityMeasures.calculateSimilarityAverage(b.counts, c.counts);
			final float product=simDif*ratio;
			
			if(simDif<maxDif && ratio<maxRatio && product<maxProduct) {
				if(product<bestProduct) {
					best=b;
					bestProduct=product;

					if(simDif<maxDif0 && ratio<maxRatio0 && product<maxProduct0 && gcDif<maxGCDif0) {
						return best;//Early exit
					}
				}
			}
		}
		return best;
	}
	
	public Cluster findBestCluster(Cluster a, ArrayList<Cluster> clusters, float stringency, 
			int limit, int taxlevel, boolean allowNoTaxID, boolean allowHalfTaxID) {
		float mult=(a.size<500 ? 2.0f : a.size<1000 ? 1.60f : a.size<2000 ? 1.40f : a.size<4000 ? 1.20f : 1f)*stringency;
		float maxDif=maxDif2*mult;
		float maxRatio=maxRatio2*mult;
		float maxProduct=maxDif2*maxRatio2*productMult*mult;
		float maxGCDif=maxGCDif2*stringency;
		
		final float d=a.depth+.5f;
		final float gc=a.gc();
		Cluster best=null;
		float bestProduct=10000;//Lower is better
		for(int i=0; i<limit; i++) {
			refinementComparisons++;
			Cluster b=clusters.get(i);
			if(b.size()<1000) {break;}
			if(a==b) {continue;}
			if(!allowHalfTaxID && (a.taxid<1 || b.taxid<1)) {continue;}
			if(!allowNoTaxID && a.taxid<1 && b.taxid<1) {continue;}
			if(taxlevel>=0 && tree!=null && a.taxid!=b.taxid && a.taxid>0 && b.taxid>0) {
				int commonAncestorLevel=tree.commonAncestorLevel(a.taxid, b.taxid);
				if(commonAncestorLevel>taxlevel) {continue;}
			}
			final float d2=b.depth+0.5f;
			final float ratio=Tools.max(d, d2)/Tools.min(d, d2);
			final float gcDif=Math.abs(gc-b.gc());
			if(ratio>=maxRatio || gcDif>=maxGCDif) {continue;}
			refinementComparisonsSlow++;
			final float simDif=SimilarityMeasures.calculateSimilarityAverage(b.counts, a.counts);
			final float product=simDif*ratio;
			if(simDif<maxDif && ratio<maxRatio && product<maxProduct) {
				if(product<bestProduct) {
					best=b;
					bestProduct=product;
				}
			}
		}
		return best;
	}
	
	public ArrayList<Bin> clusterByTaxid(ArrayList<? extends Bin> bins){
		outstream.print("Clustering by Taxid: \t");
		phaseTimer.start();
		Collections.sort(bins);
		HashMap<Integer, Bin> map=new HashMap<Integer, Bin>();
		int clustersMade=0;
		int contigsClustered=0;

		ArrayList<Bin> out=new ArrayList<Bin>();
		for(int i=0; i<bins.size(); i++) {
			Bin b=bins.get(i);
			if(b.taxid()>0) {
				Integer key=Integer.valueOf(b.taxid());
				Bin old=map.get(key);
				if(old==null) {
					map.put(key, b);
					b=null;
				}else if(old.getClass()==Cluster.class) {
					//Todo: Write "similar" function.
					((Cluster)old).add(b);
					contigsClustered++;
					b=null;
				}else {
					Cluster a=new Cluster(clustersMade);
					a.add(old);
					a.add(b);
					map.put(key, a);
					clustersMade++;
					contigsClustered++;
					b=null;
				}
			}
			if(b!=null) {out.add(b);}
		}
		
		out.addAll(map.values());
		Collections.sort(out);
		
		phaseTimer.stopAndPrint();
		outstream.println("Made "+clustersMade+" clusters containing "+contigsClustered+"/"+bins.size()+" elements.");
		return out;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------            Fields            ----------------*/
	/*--------------------------------------------------------------*/
	
	//Greedy selection when forming clusters
	float maxDif0=0.04f;
	float maxRatio0=1.4f;
	float maxGCDif0=0.015f;
	
	//Optimal selection when forming clusters
	float maxDif1=0.10f;
	float maxRatio1=2.0f;
	float maxGCDif1=0.02f;
	
	//When merging clusters
	float maxDif2=0.14f;
	float maxRatio2=2.6f;
	float maxGCDif2=0.03f;
	
	float productMult=0.75f;

	long initialComparisons=0;
	long refinementComparisons=0;
	long initialComparisonsSlow=0;
	long refinementComparisonsSlow=0;
	BinSketcher sketcher;
	TaxTree tree;
	
	/*--------------------------------------------------------------*/
	/*----------------         Final Fields         ----------------*/
	/*--------------------------------------------------------------*/
	
	final Timer phaseTimer=new Timer();
	final PrintStream outstream;
	
}
