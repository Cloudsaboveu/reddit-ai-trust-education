import pandas as pd, numpy as np, re, json
from pathlib import Path
D=Path('/mnt/data'); src=pd.read_csv(D/'Data 2.csv',sep=';',dtype=str,encoding='utf-8-sig').fillna('')
src['stakeholder_group']=src.stakeholder_group.replace({'educator':'educators'})
com=src[(src.type=='comment') & src.stakeholder_group.isin(['students','educators'])].copy()
old=pd.read_csv(D/'stage2_selected_120_review.csv',dtype=str).fillna(''); old_ids=set(old.id)
# rule-based relevance: require GenAI context AND substantive output reliability/credibility in same comment.
ai=r'\b(?:AI|gen\s?ai|generative\s+ai|chat\s?gpt|gpt[-\s]?\d*|llms?|language models?|gemini|claude|copilot|grok|bot|model|generated)\b'
cred=r'\b(?:trust(?:worthy)?|distrust|reliab\w*|unreliab\w*|accurac\w*|inaccurac\w*|hallucinat\w*|fabricat\w*|invent(?:ed|ing)?|made[- ]up|fake (?:citation|source|reference|information)|fact[- ]check\w*|verif\w*|double[- ]check\w*|cross[- ]check\w*|wrong (?:answer|information|fact|citation)|incorrect (?:answer|information|fact)|misinformation|misleading|authentic\w*|disclos\w*|citations?|references?|sources?)\b'
strong=r'\b(?:hallucinat\w*|fabricat\w*|fact[- ]check\w*|verif\w*|double[- ]check\w*|cross[- ]check\w*|unreliab\w*|inaccurac\w*|distrust|trustworthy|not trust|don.t trust|can.t trust|shouldn.t trust|made[- ]up (?:citations?|sources?|references?|facts?)|fake (?:citations?|sources?|references?))\b'
# use sentences / windows to require topical proximity, while also keeping strong references to output credibility
split=lambda t: re.split(r'(?<=[.!?])\s+|\n+',str(t))
def score(t):
    sentences=split(t); near=0; strongnear=0
    for i,s in enumerate(sentences):
        w=' '.join(sentences[max(0,i-1):min(len(sentences),i+2)])
        if re.search(ai,w,re.I) and re.search(cred,s,re.I):
            near+=1
            if re.search(strong,s,re.I):strongnear+=1
    return near,strongnear
com[['near','strongnear']]=pd.DataFrame(com.text.map(score).tolist(),index=com.index)
com['eligible_auto']=(com.near>0)&(com.strongnear>0)
# conservative review of original 120 preview decisions: retain original exclusions, full text rule can promote uncertain, but cannot imply human validation
prior=old.set_index('id')
com['prior_review']=com.id.map(prior.relevance_review).fillna('new_candidate')
com.loc[com.prior_review=='exclude_preview','eligible_auto']=False
# Deterministic prioritisation with previous likely-relevant comments first; one comment per parent post.
com['rank_prior']=com.prior_review.map({'likely_relevant_preview':0,'needs_full_text_review':1,'new_candidate':2,'exclude_preview':3}).fillna(3)
com['random_key']=com.id.map(lambda x:int(__import__('hashlib').sha256(('20261123'+x).encode()).hexdigest()[:12],16))
com=com.sort_values(['stakeholder_group','rank_prior','strongnear','near','random_key'],ascending=[True,True,False,False,True])
selected=[]
for g in ['educators','students']:
    pool=com[(com.stakeholder_group==g)&com.eligible_auto].copy()
    first=pool.drop_duplicates('post_id').head(60)
    if len(first)<60: first=pd.concat([first,pool[~pool.id.isin(first.id)].head(60-len(first))])
    selected.append(first)
S=pd.concat(selected).copy(); S['sample_id']=['E%03d'%i for i in range(1,61)]+['S%03d'%i for i in range(1,61)]
# Theme detection is keyword based; require context check on interpretation
patterns={
 'ACC':r'\b(?:accurac\w*|inaccurac\w*|reliab\w*|unreliab\w*|wrong|incorrect|correct|mistak\w*|errors?|false|truth|true)\b',
 'HAL':r'\b(?:hallucinat\w*|fabricat\w*|made[- ]up|invent(?:ed|ing)?|fake (?:citations?|references?|sources?))\b',
 'VER':r'\b(?:verif\w*|fact[- ]check\w*|double[- ]check\w*|cross[- ]check\w*|check(?:ing)? (?:the|its|their|my|your) (?:answer|output|facts?|sources?|references?|citations?|information)|human[- ]in[- ]the[- ]loop|oversight)\b',
 'AUT':r'\b(?:authentic\w*|genuine|disclos\w*|transparen\w*|ai[- ]generated|ai[- ]written|human[- ]written|detect(?:or|ion))\b',
 'SRC':r'\b(?:citations?|references?|sources?|evidence|peer[- ]review\w*|scholar(?:ly)?|attribution)\b',
 'BIA':r'\b(?:bias(?:ed)?|misinformation|disinformation|misleading|decepti\w*)\b'
}
for k,p in patterns.items():S[k]=S.text.str.contains(p,flags=re.I,regex=True)
# Transparent heuristic stance, not human-coded: rules can misread sarcasm, quotation, negation.
distrust=r'\b(?:don.t trust|do not trust|can.t trust|cannot trust|shouldn.t trust|not reliable|unreliable|inaccurate|hallucinat\w*|fabricat\w*|made[- ]up|wrong|incorrect|errors?|lies?|fake (?:citation|source|reference)|not accurate|misleading)\b'
conditional=r'\b(?:double[- ]check|fact[- ]check|verif\w*|cross[- ]check|check (?:the|its|their|your|my) (?:work|answer|output|sources?|information)|human[- ]in[- ]the[- ]loop|oversight|use (?:it|ai|chatgpt) (?:as|for)|helpful|useful|can help|with caution|be careful|but|however|as long as|only if|depending on)\b'
positive=r'\b(?:trust (?:it|ai|chatgpt|the output)|reliable|accurate|works well|great tool|very helpful|useful|good at)\b'
def stance(t):
 d=bool(re.search(distrust,t,re.I));c=bool(re.search(conditional,t,re.I));p=bool(re.search(positive,t,re.I))
 if d and (c or p):return 'C'
 if d:return 'D'
 if c:return 'C'
 if p:return 'T'
 return 'U'
S['trust_stance_auto']=S.text.map(stance)
S['theme_codes_auto']=S.apply(lambda r:';'.join(k for k in patterns if r[k]) or 'OTH',axis=1)
S['review_status']='RULE-BASED PROVISIONAL — manual full-text adjudication required'
S['selection_basis']='AI + credibility within adjacent sentences; strong credibility expression; previous preview screen exclusions retained'
# Private review file; public-safe aggregates only
cols=['sample_id','id','post_id','stakeholder_group','specific_subreddit','text','prior_review','near','strongnear','trust_stance_auto','theme_codes_auto','review_status','selection_basis']+list(patterns)
S[cols].to_csv(D/'stage2_120_provisional_coding_PRIVATE.csv',index=False)
# public-safe aggregates
counts=pd.crosstab(S.stakeholder_group,S.trust_stance_auto).reindex(index=['educators','students'],columns=['T','D','C','U'],fill_value=0)
themes=S.groupby('stakeholder_group')[list(patterns)].sum().reindex(['educators','students'])
counts.to_csv(D/'stage2_stance_counts.csv');themes.to_csv(D/'stage2_theme_counts.csv')
summary={'total_records':len(src),'comments':len(com),'auto_candidates':com.groupby('stakeholder_group').eligible_auto.sum().astype(int).to_dict(),'selected':S.groupby('stakeholder_group').size().to_dict(),'previous_selected_retained':int(S.id.isin(old_ids).sum()),'stance':counts.to_dict(orient='index'),'themes':themes.astype(int).to_dict(orient='index'),'distinct_parent_posts':S.groupby('stakeholder_group').post_id.nunique().to_dict()}
(D/'stage2_summary.json').write_text(json.dumps(summary,indent=2))
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':11})
fig,ax=plt.subplots(figsize=(9,4.7));x=np.arange(2);bottom=np.zeros(2)
for cat,label in [('T','Trust'),('D','Distrust'),('C','Conditional/mixed'),('U','Unclear')]:
 vals=counts[cat].to_numpy();ax.bar(x,vals,bottom=bottom,label=label);bottom+=vals
ax.set_xticks(x,['Educator-oriented','Student-oriented']);ax.set_ylabel('Number of comments');ax.set_title('Provisional rule-based trust stance (n=120)');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.12),ncol=4,frameon=False);fig.tight_layout();fig.savefig(D/'stage2_stance_chart.png',dpi=220,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.8));y=np.arange(len(patterns));h=.36
ax.barh(y-h/2,themes.loc['educators'].values,height=h,label='Educator-oriented');ax.barh(y+h/2,themes.loc['students'].values,height=h,label='Student-oriented');ax.set_yticks(y,['Accuracy','Hallucination','Verification','Authenticity','Sources','Bias/misinformation']);ax.invert_yaxis();ax.set_xlabel('Comments with keyword match (overlapping categories)');ax.set_title('Provisional keyword themes (n=120)');ax.legend();fig.tight_layout();fig.savefig(D/'stage2_themes_chart.png',dpi=220,bbox_inches='tight');plt.close(fig)
print(json.dumps(summary,indent=2))
