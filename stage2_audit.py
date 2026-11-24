import pandas as pd,re,hashlib,json
from pathlib import Path
import matplotlib.pyplot as plt
P=Path('/mnt/data')
d=pd.read_csv(P/'stage2_120_provisional_coding_PRIVATE.csv').fillna('')
# Extract supporting sentences from the entire comment; no 500-character preview limit.
SPLIT=re.compile(r'(?<=[.!?])\s+|\n+')
patterns={
 'accuracy':r'\b(?:accurac\w*|inaccurac\w*|unreliab\w*|reliab\w*|wrong (?:answer|fact|information|result)|incorrect|mistak\w*|errors?|not correct)\b',
 'fabrication':r'\b(?:hallucinat\w*|fabricat\w*|made[- ]up|invented|fake (?:citations?|sources?|references?))\b',
 'verification':r'\b(?:verif\w*|fact[- ]check\w*|double[- ]check\w*|cross[- ]check\w*|check (?:the|its|their|your|my) (?:answers?|outputs?|sources?|references?|facts?|work)|oversight)\b',
 'source_evidence':r'\b(?:citations?|references?|sources?|evidence|peer[- ]review\w*)\b',
 'authenticity':r'\b(?:authentic\w*|disclos\w*|transparen\w*|AI[- ]generated|AI[- ]written|human[- ]written)\b',
 'bias_misinformation':r'\b(?:bias(?:ed)?|misinformation|disinformation|misleading|decepti\w*)\b'
}
ai=re.compile(r'\b(?:AI|GenAI|ChatGPT|GPT|LLM|Gemini|Claude|Copilot|language model|generative model|AI[- ]generated)\b',re.I)
exclude_detector=re.compile(r'\b(?:AI detectors?|AI checkers?|turnitin|zerogpt|copyleaks|AI detection)\b',re.I)
trust=re.compile(r'\b(?:trust|distrust|reliab\w*|unreliab\w*|accurac\w*|inaccurac\w*|hallucinat\w*|fabricat\w*|verif\w*|fact[- ]check\w*|fake (?:sources?|citations?|references?)|made[- ]up)\b',re.I)
rows=[]
for _,r in d.iterrows():
 t=str(r.text); ss=[x.strip() for x in SPLIT.split(t) if x.strip()]
 evidence=[]
 for j,s in enumerate(ss):
  if any(re.search(p,s,re.I) for p in patterns.values()):
   context=' '.join(ss[max(0,j-1):min(len(ss),j+2)])
   if ai.search(context):evidence.append(s[:420])
 evidence=list(dict.fromkeys(evidence))
 themes=[k for k,p in patterns.items() if any(re.search(p,s,re.I) for s in evidence)]
 detector_only=bool(exclude_detector.search(t)) and not bool(re.search(r'\b(?:output|answer|source|citation|reference|feedback|information|content|fact|hallucinat|accuracy|reliable)\b', ' '.join(evidence),re.I))
 status='candidate_contextual' if evidence else 'needs_manual_context';
 if detector_only:status='possible_detector_only'
 rows.append({'sample_id':r.sample_id,'group':r.stakeholder_group,'source_record_id_PRIVATE':r.id,'source_post_id_PRIVATE':r.post_id,'comment_full_text_PRIVATE':t,'characters':len(t),'evidence_sentence_count':len(evidence),'evidence_extract_PRIVATE':' || '.join(evidence[:4]),'credibility_theme_indicators':'; '.join(themes),'original_rule_stance':r.trust_stance_auto,'automated_relevance_flag':status,'human_relevance_decision':'NOT REVIEWED','human_trust_stance':'NOT CODED','human_theme_codes':'NOT CODED','coding_rationale':'','adjudication_notes':''})
a=pd.DataFrame(rows)
a.to_csv(P/'stage2_fulltext_audit_PRIVATE.csv',index=False)
# Conservative report: not a validated sample, no inferential claim
counts=a.groupby(['group','automated_relevance_flag']).size().unstack(fill_value=0)
counts.to_csv(P/'stage2_fulltext_audit_counts.csv')
fig,ax=plt.subplots(figsize=(8,4.8))
labels=['Educator-oriented','Student-oriented'];groups=['educators','students']; cats=['candidate_contextual','needs_manual_context','possible_detector_only']; bottom=[0,0]
for cat in cats:
 vals=[int(counts.loc[g,cat]) if cat in counts.columns else 0 for g in groups]
 ax.bar(labels,vals,bottom=bottom,label={'candidate_contextual':'Contextual keyword evidence','needs_manual_context':'Needs context review','possible_detector_only':'Possible detector-only'}[cat]);bottom=[x+y for x,y in zip(bottom,vals)]
ax.set_ylabel('Comments');ax.set_title('Full-text automated screening audit (n=120)');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.14),frameon=False,ncol=1);fig.tight_layout();fig.savefig(P/'stage2_fulltext_screening_chart.png',dpi=220,bbox_inches='tight');plt.close(fig)
report={'selected':len(a),'group_sizes':a.group.value_counts().to_dict(),'automated_screening_flags':counts.to_dict(orient='index'),'note':'All comments processed in full, but human relevance and qualitative coding are not yet complete. Rule stance and themes are not validated findings.'}
(P/'stage2_fulltext_audit_summary.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
