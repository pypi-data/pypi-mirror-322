package bin;

import json.JsonObject;

public abstract class Bin extends BinObject implements Sketchable {
	
	@Override
	public final int id() {return id;}
	
	@Override
	public final int taxid() {return taxid;}

	@Override
	public final float gc() {return gcSum/(float)size();}
	
	@Override
	/** Biggest first */
	public final int compareTo(Sketchable o) {
		if(size()!=o.size()) {return size()>o.size() ? -1 : 1;}//Biggest first
		return o.id()-id();
	}
	
	@Override
	public final void setFrom(JsonObject all) {
		assert(sketchedSize<size());
		clearTax();
		JsonObject top=null, second=null;
		if(all!=null && all.jmapSize()>0) {
			for(String key : all.jmap.keySet()){
				JsonObject hit=all.jmap.get(key);
				if(top==null) {top=hit;}
				else {
					if(hit.getLong("TaxID")!=1806490) {//Achromobacter sp. ATCC35328; messes with E.coli.
						second=hit;
						break;
					}
				}
			}
		}
		topHit=(top==null ? null : new SketchRecord(top));
		secondHit=(second==null ? null : new SketchRecord(second));
		taxid=(topHit==null ? -1 : topHit.taxid);
		genusTaxid=(topHit==null ? -1 : topHit.genusTaxid);
		sketchedSize=size();
	}
	
	@Override
	public final void clearTax() {
		taxid=genusTaxid=-1;
		topHit=secondHit=null;
		sketchedSize=0;
	}
	
	@Override
	public void setID(int id_) {id=id_;}

	public final long sketchedSize() {return sketchedSize;}
//	public final boolean needsTaxUpdate() {return needsTaxUpdate;}
	
	public abstract Cluster toCluster(int id_);
	
	public int id;
	
	public int kmers;
	public float invKmers;
	
	public int[] counts;
	public long depthSum;
	public float depth;
	public long gcSum;
	public long sketchedSize;

//	public boolean needsTaxUpdate=true;
	public int taxid;
	public int genusTaxid;
	SketchRecord topHit;
	SketchRecord secondHit;
	
}
