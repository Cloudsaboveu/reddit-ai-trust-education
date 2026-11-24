"""Reproducible, AI-assisted research coding. Not independently human-validated."""
from pathlib import Path
import pandas as pd, re, hashlib, json
import matplotlib.pyplot as plt
P=Path('/mnt/data')
a=pd.read_csv(P/'stage2_fulltext_audit_PRIVATE.csv').fillna('')
s=pd.read_csv(P/'stage2_120_provisional_coding_PRIVATE.csv').fillna('')
source=pd.read_csv(P/'Data 2.csv',sep=';',dtype=str,encoding='utf-8-sig').fillna('')
source['stakeholder_group']=source.stakeholder_group.replace({'educator':'educators'})
com=source[(source.type=='comment')&source.stakeholder_group.isin(['students','educators'])].copy()
# Use original candidate criteria without executing prior scripts or modifying original files.
ai=r'\b(?:AI|gen\s?ai|generative\s+ai|chat\s?gpt|gpt[-\s]?\d*|llms?|language models?|gemini|claude|copilot|grok|bot|model|generated)\b'
cred=r'\b(?:trust(?:worthy)?|distrust|reliab\w*|unreliab\w*|accurac\w*|inaccurac\w*|hallucinat\w*|fabricat\w*|invent(?:ed|ing)?|made[- ]up|fake (?:citation|source|reference|information)|fact[- ]check\w*|verif\w*|double[- ]check\w*|cross[- ]check\w*|wrong (?:answer|information|fact|citation)|incorrect (?:answer|information|fact)|misinformation|misleading|authentic\w*|disclos\w*|citations?|references?|sources?)\b'
strong=r'\b(?:hallucinat\w*|fabricat\w*|fact[- ]check\w*|verif\w*|double[- ]check\w*|cross[- ]check\w*|unreliab\w*|inaccurac\w*|distrust|trustworthy|not trust|don.t trust|can.t trust|shouldn.t trust|made[- ]up (?:citations?|sources?|references?|facts?)|fake (?:citations?|sources?|references?))\b'
split=lambda t:re.split(r'(?<=[.!?])\s+|\n+',str(t))
def proximity(t):
 ss=split(t); near=strongnear=0
 for i,sen in enumerate(ss):
  context=' '.join(ss[max(0,i-1):min(len(ss),i+2)])
  if re.search(ai,context,re.I) and re.search(cred,sen,re.I):
   near+=1;strongnear+=bool(re.search(strong,sen,re.I))
 return near,strongnear
com[['near','strongnear']]=pd.DataFrame(com.text.map(proximity).tolist(),index=com.index)
com=com[(com.near>0)&(com.strongnear>0)].copy()
used=set(a.source_record_id_PRIVATE)
usedposts=set(a.source_post_id_PRIVATE)
old=pd.read_csv(P/'stage2_selected_120_review.csv',dtype=str).fillna('')
excluded_prior=set(old.loc[old.relevance_review=='exclude_preview','id'])
com=com[~com.id.isin(used|excluded_prior)&~com.post_id.isin(usedposts)]
com['hash']=com.id.map(lambda x:hashlib.sha256(('20261123'+x).encode()).hexdigest())
com=com.sort_values(['stakeholder_group','strongnear','near','hash'],ascending=[True,False,False,True])
# Preserve previous 13 assistant-reviewed includes, and replace 7 assistant-reviewed excludes.
keep=a[a.human_relevance_decision!='ASSISTANT_REVIEW_EXCLUDE'].copy()
new=[]
for group in ['educators','students']:
 needed=60-sum(keep.group==group)
 pool=com[com.stakeholder_group==group].drop_duplicates('post_id').head(needed)
 if len(pool)<needed:
  # Broaden to weaker contextual matches, explicitly flagged as such in output.
  extra=source[(source.type=='comment') & (source.stakeholder_group==group) & (~source.id.isin(used|excluded_prior)) & (~source.post_id.isin(usedposts|set(pool.post_id)))].copy()
  extra=extra[extra.text.str.contains(ai,flags=re.I,regex=True) & extra.text.str.contains(cred,flags=re.I,regex=True)]
  extra['hash']=extra.id.map(lambda x:hashlib.sha256(('20261123'+x).encode()).hexdigest())
  extra=extra.sort_values('hash').drop_duplicates('post_id').head(needed-len(pool))
  pool=pd.concat([pool,extra])
 if len(pool)!=needed: raise RuntimeError(f'Insufficient replacement candidates for {group}')
 for _,r in pool.iterrows():
  new.append({'sample_id':'R'+str(len(new)+1).zfill(3),'group':group,'source_record_id_PRIVATE':r.id,'source_post_id_PRIVATE':r.post_id,'comment_full_text_PRIVATE':r.text,'human_relevance_decision':'NOT REVIEWED','human_trust_stance':'','human_theme_codes':'','coding_rationale':'','automated_relevance_flag':'replacement_rule_candidate'})
final=pd.concat([keep,pd.DataFrame(new)],ignore_index=True).sort_values(['group','sample_id']).reset_index(drop=True)
assert len(final)==120 and all(final.group.value_counts()==60)
assert final.source_post_id_PRIVATE.nunique()==120
patterns={
 'ACC':r'\b(?:accurac\w*|inaccurac\w*|unreliab\w*|reliab\w*|wrong (?:answer|information|fact|result)|incorrect|mistak\w*|errors?|not correct)\b',
 'HAL':r'\b(?:hallucinat\w*|fabricat\w*|made[- ]up|invent(?:ed|ing)?|fake (?:citations?|sources?|references?))\b',
 'VER':r'\b(?:verif\w*|fact[- ]check\w*|double[- ]check\w*|cross[- ]check\w*|check (?:the|its|their|your|my) (?:answers?|outputs?|sources?|references?|facts?|work)|oversight)\b',
 'AUT':r'\b(?:authentic\w*|disclos\w*|transparen\w*|AI[- ]generated|AI[- ]written|human[- ]written)\b',
 'SRC':r'\b(?:citations?|references?|sources?|evidence|peer[- ]review\w*)\b',
 'BIA':r'\b(?:bias(?:ed)?|misinformation|disinformation|misleading|decepti\w*)\b'}
neg=r'\b(?:don.t trust|do not trust|can.t trust|cannot trust|shouldn.t trust|not reliable|unreliable|inaccurate|hallucinat\w*|fabricat\w*|made[- ]up|wrong|incorrect|errors?|fake (?:citation|source|reference)|not accurate|misleading)\b'
conditional=r'\b(?:double[- ]check|fact[- ]check|verif\w*|cross[- ]check|check (?:the|its|their|your|my) (?:work|answer|output|sources?|information)|human[- ]in[- ]the[- ]loop|oversight|helpful|useful|can help|with caution|be careful|but|however|as long as|only if|depending on)\b'
positive=r'\b(?:trust (?:it|ai|chatgpt|the output)|reliable|accurate|works well|great tool|very helpful|useful|good at)\b'
def stance(t):
 d=bool(re.search(neg,t,re.I)); c=bool(re.search(conditional,t,re.I)); p=bool(re.search(positive,t,re.I))
 return 'C' if d and (c or p) else 'D' if d else 'C' if c else 'T' if p else 'U'
def evidence(t):
 sentences=[z.strip() for z in split(t) if z.strip()]
 matches=[]
 for i,z in enumerate(sentences):
  context=' '.join(sentences[max(0,i-1):min(len(sentences),i+2)])
  if re.search(ai,context,re.I) and any(re.search(p,z,re.I) for p in patterns.values()):matches.append(z)
 return ' | '.join(matches[:3])[:750]
final['theme_codes_provisional']=final.apply(lambda r:r.human_theme_codes if r.human_relevance_decision=='ASSISTANT_REVIEW_INCLUDE' and str(r.human_theme_codes).strip() else ';'.join(k for k,p in patterns.items() if re.search(p,r.comment_full_text_PRIVATE,re.I)) or 'OTH',axis=1)
final['stance_provisional']=final.apply(lambda r:r.human_trust_stance if r.human_relevance_decision=='ASSISTANT_REVIEW_INCLUDE' and str(r.human_trust_stance).strip() else stance(r.comment_full_text_PRIVATE),axis=1)
final['coding_method']=final.human_relevance_decision.map(lambda x:'assistant full-text interpretive review (not independent human verification)' if x=='ASSISTANT_REVIEW_INCLUDE' else 'automated full-text rules (not qualitatively verified)')
final['eligibility_status']=final.human_relevance_decision.map(lambda x:'AI-assisted review: eligible' if x=='ASSISTANT_REVIEW_INCLUDE' else 'candidate: not manually verified')
final['evidence_extract_PRIVATE']=final.comment_full_text_PRIVATE.map(evidence)
final['independent_validation_status']='PENDING'
final.to_csv(P/'stage2_final_120_working_PRIVATE.csv',index=False)
counts=pd.crosstab(final.group,final.stance_provisional).reindex(index=['educators','students'],columns=['T','D','C','U'],fill_value=0)
themes=pd.DataFrame([{'group':g,**{k:int(final.loc[final.group==g,'theme_codes_provisional'].map(lambda s:k in s.split(';')).sum()) for k in patterns}} for g in ['educators','students']]).set_index('group')
counts.to_csv(P/'stage2_working_stance_counts.csv');themes.to_csv(P/'stage2_working_theme_counts.csv')
# Plot transparent provisional results
plt.rcParams.update({'font.size':12})
fig,ax=plt.subplots(figsize=(10,5)); x=range(2);bot=[0,0]
for k,label in [('T','Trust'),('D','Distrust'),('C','Conditional / mixed'),('U','Unclear')]:
 vals=counts[k].tolist();ax.bar(x,vals,bottom=bot,label=label);bot=[a+b for a,b in zip(bot,vals)]
ax.set_xticks([0,1],['Educator-oriented','Student-oriented']);ax.set_ylabel('Comments');ax.set_title('PROVISIONAL: AI-assisted trust-stance classifications (60 per group)');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.12),ncol=4,frameon=False);fig.tight_layout();fig.savefig(P/'stage2_working_stance_chart.png',dpi=220,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(10,5)); y=list(range(6));h=.36
ax.barh([i-h/2 for i in y],themes.loc['educators'].values,height=h,label='Educator-oriented');ax.barh([i+h/2 for i in y],themes.loc['students'].values,height=h,label='Student-oriented');ax.set_yticks(y,['Accuracy','Hallucinations','Verification','Authenticity','Source credibility','Bias / misinformation']);ax.invert_yaxis();ax.set_xlabel('Comments with provisional theme codes (overlap allowed)');ax.set_title('PROVISIONAL: AI-assisted credibility themes');ax.legend();fig.tight_layout();fig.savefig(P/'stage2_working_themes_chart.png',dpi=220,bbox_inches='tight');plt.close(fig)
summary={'source_comments':int((source.type=='comment').sum()),'previous_selected':120,'prior_assistant_reviewed_included':int((a.human_relevance_decision=='ASSISTANT_REVIEW_INCLUDE').sum()),'prior_assistant_reviewed_excluded':int((a.human_relevance_decision=='ASSISTANT_REVIEW_EXCLUDE').sum()),'replacements':len(new),'working_sample':len(final),'groups':final.group.value_counts().to_dict(),'unique_parent_posts':final.source_post_id_PRIVATE.nunique(),'independently_human_validated':0,'stance_provisional':counts.to_dict(orient='index'),'themes_provisional':themes.to_dict(orient='index')}
(P/'stage2_working_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
