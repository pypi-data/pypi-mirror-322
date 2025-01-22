package bin;

import dna.AminoAcid;
import json.JsonObject;
import shared.Shared;
import shared.Tools;
import sketch.Sketch;
import sketch.SketchMakerMini;
import stream.Read;
import structures.ByteBuilder;

public class Contig extends Bin {

	public Contig(String name_, byte[] bases_, int id_) {
		name=name_;
		bases=bases_;
		id=id_;
	}
	
	@Override
	public Cluster toCluster(int id_) {
		Cluster c=new Cluster(id_);
		c.add(this);
		return c;
	}
	
	public void loadCounts() {
		assert(kmers==0);
		counts=new int[canonicalKmers];
		kmers=countKmers(bases, counts);
		invKmers=1f/Tools.max(1, kmers);
		for(byte b : bases) {
			int x=AminoAcid.baseToNumber[b];
			gcSum+=(x==1 || x==2) ? 1 : 0;
		}
		//This assertion can fail; I saw an all A/T contig
//		assert(gcSum>0) : gcSum+", "+kmers+", "+new String(bases);
	}
	
	/** In fasta format */
	public void appendTo(ByteBuilder bb, int cluster) {
		bb.append('>').append(name);
		if(cluster>=0) {bb.tab().append("cluster_").append(cluster);}
		bb.nl();
		final int wrap=Shared.FASTA_WRAP;
		for(int i=0; i<bases.length; i+=wrap) {
			//Now with modified append I can just append(bases, wrap)
			bb.append(bases, i, wrap).nl();
		}
	}
	
	@Override
	public long size() {return bases.length;}

	@Override
	public Sketch toSketch(SketchMakerMini smm, Read r) {
		String name=Long.toString(id);
		if(r==null) {r=new Read(null, null, name, id);}
		r.id=name;
		r.numericID=id;
		r.bases=bases;
		smm.processReadNucleotide(r);
		return smm.toSketch(0);
	}
	
	@Override
	public int numContigs() {return 1;}
	
	public final String name;
	public final byte[] bases;
	
}
