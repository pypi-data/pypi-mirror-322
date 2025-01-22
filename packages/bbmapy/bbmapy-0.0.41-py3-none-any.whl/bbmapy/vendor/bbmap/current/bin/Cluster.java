package bin;

import java.util.ArrayList;

import json.JsonObject;
import shared.Tools;
import sketch.Sketch;
import sketch.SketchMakerMini;
import stream.Read;
import structures.ByteBuilder;

public class Cluster extends Bin {

	public Cluster(int id_) {id=id_;}
	
	public Cluster(int id_, Contig c) {
		id=id_;
		add(c);
	}
	
	@Override
	public Cluster toCluster(int id_) {
		id=id_;
		return this;
	}
	
	public void add(Bin b) {
		if(b.getClass()==Cluster.class) {add((Cluster)b);}
		else {add((Contig)b);}
	}
	
	public void add(Contig c) {
		if(contigs.size()==0) {
			topHit=c.topHit;
			secondHit=c.secondHit;
			taxid=c.taxid;
			genusTaxid=c.genusTaxid;
			sketchedSize=c.sketchedSize;
		}
		contigs.add(c);
		kmers+=c.kmers;
		invKmers=1f/kmers;
		if(counts==null) {counts=c.counts.clone();}
		else {Tools.add(counts, c.counts);}
		size+=c.bases.length;
		depthSum+=c.depth*c.bases.length;
		depth=(float)(depthSum/size);
		gcSum+=c.gcSum;
		assert(gcSum>0);
	}
	
	public void add(Cluster clust) {
		for(Contig c : clust.contigs) {add(c);}
	}
	
	@Override
	public long size() {return size;}

	@Override
	public Sketch toSketch(SketchMakerMini smm, Read r) {
		String name=Long.toString(id);
		if(r==null) {r=new Read(null, null, name, id);}
		r.id=name;
		r.numericID=id;
		for(Contig c : contigs) {
			r.bases=c.bases;
			smm.processReadNucleotide(r);
		}
		return smm.toSketch(0);
	}
	
	public ByteBuilder toBytes() {
		ByteBuilder bb=new ByteBuilder();
		bb.append("Cluster ").append(id).append(":");
		bb.tab().append("Size ").append(size);
		bb.tab().append("Contigs ").append(contigs.size());
		bb.tab().append("GC ").append(gc(), 3);
		bb.tab().append("Depth ").append(depth, 1);
		if(topHit!=null) {topHit.appendTo(bb.nl().tab().tab());}
		if(secondHit!=null) {secondHit.appendTo(bb.nl().tab().tab());}
		return bb;
	}
	
	@Override
	public int numContigs() {return contigs.size();}
	
	public long size;
	public ArrayList<Contig> contigs=new ArrayList<Contig>(8);
	
}
