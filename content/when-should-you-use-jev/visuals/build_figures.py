"""Original explanatory figures. All numerical examples are hypothetical.

Optional authoring dependency: Matplotlib. Runtime examples need no packages.
"""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'code'))
from economics import mean_cost, all_steps_correct

INK = '#101d33'
CREAM = '#f7f4ec'
MUTED = '#536075'
LIME = '#dce978'
LAVENDER = '#c6c8ee'
RED = '#b44547'
EDGE = '#d8dce0'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14,
                     'svg.fonttype': 'none', 'axes.titleweight': 'bold'})


def canvas(title, subtitle):
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=CREAM)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set(xlim=(0, 16), ylim=(0, 9)); ax.axis('off')
    ax.text(.65, 8.35, title, fontsize=26, fontweight='bold', color=INK, va='top')
    ax.text(.65, 7.75, subtitle, fontsize=15, color=MUTED, va='top')
    return fig, ax


def box(ax, x, y, w, h, title, text='', fill='white', title_size=18):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.04,rounding_size=0.14',
                              facecolor=fill,edgecolor=EDGE,linewidth=1.3))
    if text:
        ax.text(x+.25,y+h-.34,title,va='top',fontsize=title_size,fontweight='bold',color=INK)
        ax.text(x+.25,y+h-.97,text,va='top',fontsize=14,color=INK,linespacing=1.65)
    else:
        ax.text(x+w/2,y+h/2,title,ha='center',va='center',fontsize=title_size,fontweight='bold',color=INK)


def arrow(ax, a, b, color=MUTED, connection='arc3,rad=0'):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=18,
                               color=color,linewidth=2,connectionstyle=connection))


def save(fig, name):
    dest=ROOT/'assets';dest.mkdir(exist_ok=True)
    fig.savefig(dest/(name+'.png'),dpi=160,facecolor=fig.get_facecolor())
    fig.savefig(dest/(name+'.svg'),facecolor=fig.get_facecolor())
    plt.close(fig)


fig,ax=canvas('Give the decision to the right component',
              'Start with the output you need and the evidence already available.')
cards=[(.65,'An exact rule','Ordinary code','Parse a test result\nCheck a permission\nValidate a required field','white'),
       (5.65,'A bounded judgment','Evaluate Jev','Choose a supplied label\nRoute to a collection\nJudge a candidate passage',LIME),
       (10.65,'Something to create','Generator or planner','Write an explanation\nProduce a code patch\nDevelop an evolving plan',LAVENDER)]
for x,kicker,title,body,fill in cards:
    ax.text(x,6.65,kicker.upper(),fontsize=12,fontweight='bold',color=MUTED)
    box(ax,x,3.25,4.65,2.98,title,body,fill)
    arrow(ax,(x+2.32,3.1),(x+2.32,2.35))
box(ax,.65,1.28,14.65,1.05,'Application policy  ·  Permissions  ·  Validation  ·  Recovery',fill=INK)
ax.texts[-1].set_color(CREAM)
ax.text(.65,.58,'A model recommendation does not grant permission to act.',fontsize=15,color=MUTED)
save(fig,'decision-map')

fig,ax=canvas('Check the state before the next step',
              'A wrong decision can become the evidence for a later wrong decision.')
xs=[.65,4.45,8.25,12.05];w=3.2
ax.text(.65,6.95,'UNCHECKED PATH',fontsize=12,fontweight='bold',color=RED)
for x,title in zip(xs,['Wrong\nassumption','Wrong tool\nselected','Result\nmisinterpreted','Next action\noff course']):
    box(ax,x,5.12,w,1.42,title,fill='#f4dfd9',title_size=16)
for a,b in zip(xs,xs[1:]):arrow(ax,(a+w+.05,5.83),(b-.07,5.83),RED)
ax.text(.65,4.54,'PATH WITH A CHECKPOINT',fontsize=12,fontweight='bold',color=MUTED)
for x,title,fill in zip(xs,['Propose a\nbounded action','Execute within\npermissions','Observe and\nvalidate result','Continue if\nchecks pass'],['white','white',LIME,'white']):
    box(ax,x,2.66,w,1.40,title,fill=fill,title_size=16)
for a,b in zip(xs,xs[1:]):arrow(ax,(a+w+.05,3.36),(b-.07,3.36))
box(ax,6.95,.83,7.10,1.03,'On failure: gather evidence, review or stop',fill=LAVENDER,title_size=15)
arrow(ax,(9.85,2.60),(9.85,1.93))
ax.text(.65,.4,'Checks can miss errors. Recovery adds work. Evaluate complete runs.',fontsize=14,color=MUTED)
save(fig,'agent-checkpoints')

fig=plt.figure(figsize=(16,9),facecolor=CREAM)
fig.text(.055,.925,'One-step accuracy does not describe a whole run',fontsize=25,fontweight='bold',color=INK)
fig.text(.055,.867,'Hypothetical arithmetic, not a Jev benchmark or an agent forecast.',fontsize=15,color=MUTED)
ax=fig.add_axes([.09,.18,.58,.58],facecolor=CREAM)
steps=list(range(1,41));values=[100*all_steps_correct(.99,n) for n in steps]
ax.plot(steps,values,color=INK,lw=3)
ax.fill_between(steps,values,color=LIME,alpha=.4)
ax.set(xlim=(1,40),ylim=(0,100),xlabel='Number of required decisions',ylabel='Probability every decision is correct (%)')
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2)
ax.scatter([20],[values[19]],s=140,color=INK,zorder=3)
ax.annotate('20 steps\n81.8% all correct',xy=(20,values[19]),xytext=(21,54),fontsize=17,
            color=INK,arrowprops={'arrowstyle':'-','color':INK},fontweight='bold')
fig.text(.725,.71,'ASSUMPTIONS',fontsize=12,color=MUTED,fontweight='bold')
fig.text(.725,.65,'99% correct per step\nIndependent decisions\nEvery error is fatal\nNo recovery',fontsize=17,color=INK,linespacing=1.8,va='top')
fig.text(.725,.29,'Real workflows need\nmeasured task success,\nnot this shortcut.',fontsize=16,color=MUTED,linespacing=1.5)
fig.text(.055,.065,'P(all correct) = pⁿ only under the stated assumptions. Task completion can behave differently.',fontsize=13,color=MUTED)
save(fig,'error-horizon')

fig=plt.figure(figsize=(16,9),facecolor=CREAM)
fig.text(.055,.925,'A cheap first call can still produce an expensive system',fontsize=24,fontweight='bold',color=INK)
fig.text(.055,.867,'Fictional prices per 1,000 incoming requests. No quality or savings forecast.',fontsize=15,color=MUTED)
ax=fig.add_axes([.09,.2,.84,.56],facecolor=CREAM)
fractions=[i/100 for i in range(101)]
costs=[mean_cost(.08,f,6) for f in fractions];x=list(range(101))
ax.plot(x,costs,color=INK,lw=3,label=r'Cascade: \$0.08 + fallback fraction × \$6')
ax.axhline(4,color=RED,lw=2,ls='--',label='Baseline: $4.00')
ax.fill_between(x,costs,4,where=[c<=4 for c in costs],color=LIME,alpha=.4)
ax.fill_between(x,costs,4,where=[c>4 for c in costs],color='#efb7b1',alpha=.4)
cross=(4-.08)/6*100
ax.axvline(cross,color=MUTED,lw=1,ls=':')
ax.text(cross-2,6.2,'65.3% cost break-even',ha='right',fontsize=14,color=MUTED)
for xx,yy,label,xytext in [(20,1.28,'20% fallback\n$1.28 total',(29,.65)),(70,4.28,'70% fallback\n$4.28 total',(78,6.15))]:
    ax.scatter([xx],[yy],s=90,color=INK,zorder=4)
    ax.annotate(label,xy=(xx,yy),xytext=xytext,color=INK,fontsize=15,fontweight='bold',
                arrowprops={'arrowstyle':'-','color':INK})
ax.set(xlim=(0,100),ylim=(0,7),xlabel='Requests escalated to the fallback model (%)',ylabel='Cost per 1,000 incoming requests ($)')
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18)
ax.legend(loc='upper left',frameon=False,fontsize=13)
fig.text(.055,.065,'Fallback price is the average on the escalated subset. Verification, recovery and operating costs are excluded.',fontsize=13,color=MUTED)
save(fig,'cascade-economics')
print('Wrote four original figures as PNG and editable SVG. All plotted values are synthetic.')
