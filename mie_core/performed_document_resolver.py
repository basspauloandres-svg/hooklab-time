#!/usr/bin/env python3
"""Performed-document resolver v0.1.

Separates the source lyric document from the subset evidenced as actually performed
in a specific recording. This never rewrites the documentary source. Whole sections
with zero matched lines between evidenced sections may be marked NOT_PERFORMED_CANDIDATE.
Isolated missing lines inside an otherwise evidenced section may receive a bounded
DERIVED_BRACKET timing window from adjacent aligned lines. All such derivations are
explicitly labelled and remain auditable.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--text',required=True);ap.add_argument('--windows',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 t=json.loads(Path(a.text).read_text());w=json.loads(Path(a.windows).read_text());wins={x['line_id']:x for x in w.get('windows',[])}
 units=t.get('units',[]);sections=defaultdict(list)
 for i,u in enumerate(units):sections[u.get('section','UNSPECIFIED')].append((i,u))
 sec_order=[]
 for u in units:
  s=u.get('section','UNSPECIFIED')
  if s not in sec_order:sec_order.append(s)
 evidenced={s:sum(1 for _,u in rows if u['line_id'] in wins) for s,rows in sections.items()}
 performed=[];excluded=[];derived=[]
 for si,s in enumerate(sec_order):
  rows=sections[s];n=evidenced[s]
  prev_ev=any(evidenced[ps]>0 for ps in sec_order[:si]);next_ev=any(evidenced[ns]>0 for ns in sec_order[si+1:])
  if n==0 and prev_ev and next_ev:
   for _,u in rows: excluded.append({'line_id':u['line_id'],'section':s,'status':'NOT_PERFORMED_CANDIDATE','reason':'WHOLE_SECTION_WITH_ZERO_ASR_MATCH_BOUNDED_BY_EVIDENCED_SECTIONS'})
   continue
  for pos,(idx,u) in enumerate(rows):
   z=dict(u);x=wins.get(u['line_id'])
   if x:
    z.update({'start_s':x['start_s'],'end_s':x['end_s'],'alignment_confidence':x.get('confidence'),'alignment_evidence':x.get('evidence')});performed.append(z);continue
   # Conservative bracket only for isolated gaps inside an evidenced section.
   left=next((wins.get(rows[j][1]['line_id']) for j in range(pos-1,-1,-1) if wins.get(rows[j][1]['line_id'])),None)
   right=next((wins.get(rows[j][1]['line_id']) for j in range(pos+1,len(rows)) if wins.get(rows[j][1]['line_id'])),None)
   if left and right and float(right['start_s'])>float(left['end_s']):
    z.update({'start_s':float(left['end_s']),'end_s':float(right['start_s']),'alignment_confidence':None,'alignment_evidence':'DERIVED_BRACKET_SECTION_CONTINUITY'})
    derived.append(u['line_id']);performed.append(z)
   else: performed.append(z)
 aligned=sum('start_s' in u for u in performed);ratio=aligned/len(performed) if performed else 0
 out={'schema':'TMT_PERFORMED_TEXT_OBJECT_v0.1','song_id':t.get('song_id'),'source_document_provenance':t.get('provenance'),
      'source_document_unit_count':len(units),'performed_candidate_unit_count':len(performed),'excluded_candidates':excluded,
      'derived_bracket_line_ids':derived,'units':performed,'repetition_groups':t.get('repetition_groups',[]),
      'alignment_coverage':ratio,'alignment_status':'ALIGNED' if ratio>=.95 else ('PARTIAL' if aligned else 'UNALIGNED'),
      'rule':'Source document is preserved. Performance subset and derived bracket timings are explicit evidence states, never silent corrections.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'source':len(units),'performed':len(performed),'excluded':len(excluded),'derived':derived,'coverage':ratio,'status':out['alignment_status']}))
if __name__=='__main__':main()
