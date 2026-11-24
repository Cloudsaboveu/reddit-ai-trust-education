import pandas as pd,re,numpy as np
D='/mnt/data/'
df=pd.read_csv(D+'Data 2.csv',sep=';',encoding='utf-8-sig',dtype=str).fillna('')
df['stakeholder_group']=df.stakeholder_group.replace({'educator':'educators'})
comments=df[(df.type=='comment') & df.stakeholder_group.isin(['students','educators'])].copy()
# Targeted terms to identify credibility evaluations, not simply any mention of AI.
patterns={
 'trust':r'\b(?:trust|trustworthy|distrust|untrustworthy|believab\w*|credib\w*)\b',
 'accuracy':r'\b(?:accurac\w*|inaccurac\w*|accurate|inaccurate|correct|incorrect|wrong|mistak\w*|error\w*|reliab\w*|unreliab\w*)\b',
 'hallucination':r'\b(?:hallucinat\w*|fabricat\w*|made.up|mak(?:e|es|ing) (?:things|stuff|facts) up|invent(?:ed|s|ing)? (?:facts|sources|citations|references))\b',
 'verification':r'\b(?:verify|verif\w*|fact.check\w*|double.check\w*|check (?:the|its|their|my) (?:facts|sources|answers|output|information)|cross.check\w*)\b',
 'authenticity':r'\b(?:authentic\w*|genuine|fake|deepfake\w*|real vs fake|human.written|AI.generated|AI.written)\b',
 'bias':r'\b(?:bias|biased|misinformation|disinformation|misleading|decepti\w*|transparen\w*|disclos\w*)\b'
}
for k,p in patterns.items(): comments[k]=comments.text.str.contains(p,flags=re.I,regex=True)
comments['keyword_count']=comments[list(patterns)].sum(axis=1)
comments['candidate']=comments.keyword_count.gt(0)
print('groups',comments.groupby('stakeholder_group').size().to_dict())
print('candidates',comments[comments.candidate].groupby('stakeholder_group').size().to_dict())
print('categories',comments[list(patterns)].sum().to_dict())
# Strong signal candidates require explicit trust/hallucination/verification OR two different signal groups
comments['high_signal']=comments[['trust','hallucination','verification']].any(axis=1) | comments.keyword_count.ge(2)
print('high_signal',comments[comments.high_signal].groupby('stakeholder_group').size().to_dict())
# sample with seeded random, but first one comment per parent post to avoid thread dominance; if fewer, sample further.
rng=np.random.default_rng(20261123)
selected=[]
for group in ['students','educators']:
    pool=comments[(comments.stakeholder_group==group)&comments.high_signal].copy()
    pool['rand']=rng.random(len(pool));pool=pool.sort_values('rand')
    first=pool.drop_duplicates('post_id').head(60)
    if len(first)<60: first=pd.concat([first,pool[~pool.id.isin(first.id)].head(60-len(first))])
    selected.append(first)
S=pd.concat(selected).sort_values(['stakeholder_group','rand']).copy()
S['sample_id']=['C%03d'%i for i in range(1,len(S)+1)]
S['relevance_review']='pending_manual_review'
S['trust_stance']='uncoded'
S['credibility_themes']='uncoded'
S[['sample_id','id','post_id','stakeholder_group','specific_subreddit','created_utc','text','keyword_count',*patterns.keys(),'relevance_review','trust_stance','credibility_themes']].to_csv(D+'stage2_selected_120_review.csv',index=False)
# review previews, with full text in csv
with open(D+'stage2_review_previews.txt','w') as f:
 for _,r in S.iterrows():
  f.write(f"{r.sample_id} {r.stakeholder_group} {r.id} {','.join(k for k in patterns if r[k])}: {re.sub(r'\s+',' ',r.text)[:500]}\n")
print('selected',S.groupby('stakeholder_group').size().to_dict(),'distinct posts',S.groupby('stakeholder_group').post_id.nunique().to_dict())
