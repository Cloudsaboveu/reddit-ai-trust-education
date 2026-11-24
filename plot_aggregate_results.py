"""Regenerate *provisional* charts from aggregate CSVs; no raw Reddit data needed."""
from pathlib import Path
import csv
import matplotlib.pyplot as plt
BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / 'results'
FIGURES = BASE / 'figures'
FIGURES.mkdir(exist_ok=True)

def rows(filename):
    with (RESULTS / filename).open(newline='', encoding='utf-8-sig') as f:
        return {r['group']: r for r in csv.DictReader(f)}

stance = rows('stage2_working_stance_counts.csv')
themes = rows('stage2_working_theme_counts.csv')
groups = ['educators', 'students']
labels = ['Educator-oriented', 'Student-oriented']
fig, ax = plt.subplots(figsize=(10, 5))
bottom = [0, 0]
for key, label in [('T', 'Trust'), ('D', 'Distrust'), ('C', 'Conditional/mixed'), ('U', 'Unclear')]:
    vals = [int(stance[g][key]) for g in groups]
    ax.bar(labels, vals, bottom=bottom, label=label)
    bottom = [a+b for a,b in zip(bottom, vals)]
ax.set_ylabel('Comments')
ax.set_title('PROVISIONAL AI-assisted trust stance (n=60 per group)')
ax.legend(loc='upper center', bbox_to_anchor=(.5, -.12), ncol=4)
fig.tight_layout()
fig.savefig(FIGURES / 'stage2_working_stance_chart.png', dpi=220, bbox_inches='tight')
plt.close(fig)

keys = ['ACC','HAL','VER','AUT','SRC','BIA']
names = ['Accuracy','Hallucinations','Verification','Authenticity','Source credibility','Bias/misinformation']
y = list(range(len(keys)))
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh([v-.19 for v in y], [int(themes['educators'][k]) for k in keys], height=.36, label='Educator-oriented')
ax.barh([v+.19 for v in y], [int(themes['students'][k]) for k in keys], height=.36, label='Student-oriented')
ax.set_yticks(y, names)
ax.invert_yaxis()
ax.set_xlabel('Provisional theme count (overlapping codes)')
ax.set_title('PROVISIONAL AI-assisted credibility themes')
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES / 'stage2_working_themes_chart.png', dpi=220, bbox_inches='tight')
plt.close(fig)
print('Saved provisional figures in', FIGURES)
