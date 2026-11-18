import csv, math
from pathlib import Path
p=Path(r'C:\Users\48891\Desktop\10.3\rsef-supplementary-materials-final')

def rows(name):
    with (p/name).open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def write_svg(name, body, title, desc):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="520" viewBox="0 0 900 520">
<title>{esc(title)}</title><desc>{esc(desc)}</desc>
<rect width="100%" height="100%" fill="white"/>
<style>text{{font-family:Arial,Helvetica,sans-serif;fill:#111}} .axis{{stroke:#222;stroke-width:1.5}} .grid{{stroke:#ddd;stroke-width:1}} .small{{font-size:13px}} .label{{font-size:15px}} .title{{font-size:21px;font-weight:600}} .legend{{font-size:13px}}</style>
{body}</svg>'''
    (p/name).write_text(svg, encoding='utf-8')

# Figure S1: stochastic dropout spectrum, aggregate MAE +/- sample SD.
data=rows('Table_S2_dropout_spectrum.csv')
W,H=900,520; left,right,top,bottom=100,40,70,85; pw=W-left-right; ph=H-top-bottom
xmin,xmax=0,1; ymin,ymax=30,50
x=lambda v:left+(float(v)-xmin)/(xmax-xmin)*pw
y=lambda v:top+(ymax-float(v))/(ymax-ymin)*ph
parts=['<text x="450" y="35" text-anchor="middle" class="title">Stochastic channel-dropout sensitivity</text>']
for val in range(30,51,5):
    yy=y(val); parts.append(f'<line class="grid" x1="{left}" y1="{yy:.1f}" x2="{W-right}" y2="{yy:.1f}"/>')
    parts.append(f'<text x="{left-14}" y="{yy+5:.1f}" text-anchor="end" class="small">{val}</text>')
parts += [f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{H-bottom}"/>',f'<line class="axis" x1="{left}" y1="{H-bottom}" x2="{W-right}" y2="{H-bottom}"/>']
for val in [0,.2,.4,.6,.8,1]:
    xx=x(val); parts.append(f'<line class="axis" x1="{xx:.1f}" y1="{H-bottom}" x2="{xx:.1f}" y2="{H-bottom+5}"/>'); parts.append(f'<text x="{xx:.1f}" y="{H-bottom+24}" text-anchor="middle" class="small">{val:.1f}</text>')
parts += [f'<text x="{left+pw/2}" y="{H-28}" text-anchor="middle" class="label">Dropped-channel ratio</text>',f'<text transform="translate(28 {top+ph/2}) rotate(-90)" text-anchor="middle" class="label">Test MAE (Wh)</text>']
series=[('RSEF','indoor','#1f77b4'),('RSEF','outdoor','#2ca02c'),('without_residual_huber','indoor','#d62728'),('without_residual_huber','outdoor','#9467bd')]
for method,scope,color in series:
    subset=sorted([r for r in data if r['method']==method and r['dropout_scope']==scope],key=lambda r:float(r['dropout_ratio']))
    coords=[]
    for r in subset:
        xx=x(r['dropout_ratio']); m=float(r['mae_mean_wh']); sd=float(r['mae_sample_sd_wh']); yy=y(m); y1=y(m-sd); y2=y(m+sd)
        parts.append(f'<line stroke="{color}" stroke-width="1.4" x1="{xx:.1f}" y1="{y1:.1f}" x2="{xx:.1f}" y2="{y2:.1f}"/><line stroke="{color}" x1="{xx-4:.1f}" y1="{y1:.1f}" x2="{xx+4:.1f}" y2="{y1:.1f}"/><line stroke="{color}" x1="{xx-4:.1f}" y1="{y2:.1f}" x2="{xx+4:.1f}" y2="{y2:.1f}"/>')
        coords.append(f'{xx:.1f},{yy:.1f}')
    parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.5" points="{" ".join(coords)}"/>')
    for r in subset:
        xx=x(r['dropout_ratio']); yy=y(r['mae_mean_wh']); parts.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="4" fill="{color}"/>')
legend=[('RSEF, indoor', '#1f77b4'),('RSEF, outdoor','#2ca02c'),('No residual-Huber, indoor','#d62728'),('No residual-Huber, outdoor','#9467bd')]
for i,(label,color) in enumerate(legend):
    lx=left+(i%2)*340; ly=top+ph+48+(i//2)*19
    parts.append(f'<line x1="{lx}" y1="{ly-4}" x2="{lx+24}" y2="{ly-4}" stroke="{color}" stroke-width="3"/><text x="{lx+30}" y="{ly}" class="legend">{esc(label)}</text>')
write_svg('Fig_S1_dropout_spectrum.svg','\n'.join(parts),'Figure S1. Stochastic channel-dropout sensitivity','Mean test MAE with sample standard deviation across nine fold-seed runs. Intermediate dropout rates use ten randomized evaluation repetitions per run; zero and one are deterministic endpoints.')

# Figure S2: empirical interval coverage before/after validation-only scaling.
data=rows('Table_S3_interval_calibration.csv')
coverage=[r for r in data if r['quantity'] in ('uncalibrated_coverage','calibrated_coverage')]
W,H=900,500; left,right,top,bottom=110,40,70,95; pw=W-left-right; ph=H-top-bottom; ymin,ymax=40,100
y=lambda v:top+(ymax-float(v))/(ymax-ymin)*ph
parts=['<text x="450" y="35" text-anchor="middle" class="title">Empirical test coverage of nominal 95% intervals</text>']
for val in [40,50,60,70,80,90,95,100]:
    yy=y(val); style='#9b2226' if val==95 else '#ddd'; dash=' stroke-dasharray="6,5"' if val==95 else ''
    parts.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{W-right}" y2="{yy:.1f}" stroke="{style}" stroke-width="{2 if val==95 else 1}"{dash}/><text x="{left-12}" y="{yy+5:.1f}" text-anchor="end" class="small">{val}</text>')
parts += [f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{H-bottom}"/>',f'<line class="axis" x1="{left}" y1="{H-bottom}" x2="{W-right}" y2="{H-bottom}"/>',f'<text x="{left+pw/2}" y="{H-30}" text-anchor="middle" class="label">Model</text>',f'<text transform="translate(30 {top+ph/2}) rotate(-90)" text-anchor="middle" class="label">Empirical test coverage (%)</text>']
groups=['RSEF','without_residual_huber']; colors={'uncalibrated_coverage':'#f4a261','calibrated_coverage':'#2a9d8f'}; labels={'uncalibrated_coverage':'Uncalibrated','calibrated_coverage':'Calibrated'}
centers=[left+pw*.30,left+pw*.72]; bw=70
for gi,g in enumerate(groups):
    for j,q in enumerate(('uncalibrated_coverage','calibrated_coverage')):
        r=next(z for z in coverage if z['method']==g and z['quantity']==q)
        val=float(r['mean']); sd=float(r['sample_sd']); xx=centers[gi]+(j-.5)*(bw+10); yy=y(val); base=y(ymin); color=colors[q]
        parts.append(f'<rect x="{xx-bw/2:.1f}" y="{yy:.1f}" width="{bw}" height="{base-yy:.1f}" fill="{color}"/>')
        y1,y2=y(val-sd),y(val+sd)
        parts.append(f'<line x1="{xx:.1f}" y1="{y1:.1f}" x2="{xx:.1f}" y2="{y2:.1f}" stroke="#222" stroke-width="1.5"/><line x1="{xx-8:.1f}" y1="{y1:.1f}" x2="{xx+8:.1f}" y2="{y1:.1f}" stroke="#222"/><line x1="{xx-8:.1f}" y1="{y2:.1f}" x2="{xx+8:.1f}" y2="{y2:.1f}" stroke="#222"/>')
        parts.append(f'<text x="{xx:.1f}" y="{yy-9:.1f}" text-anchor="middle" class="small">{val:.1f} ± {sd:.1f}</text>')
    parts.append(f'<text x="{centers[gi]}" y="{H-bottom+26}" text-anchor="middle" class="label">{"RSEF" if g=="RSEF" else "Without residual-Huber"}</text>')
for i,(lab,col) in enumerate((('Uncalibrated','#f4a261'),('Calibrated','#2a9d8f'))):
    xx=left+100+i*190; yy=H-bottom+60; parts.append(f'<rect x="{xx}" y="{yy-13}" width="16" height="16" fill="{col}"/><text x="{xx+24}" y="{yy}" class="legend">{lab}</text>')
parts.append(f'<text x="{W-right-3}" y="{y(95)-8:.1f}" text-anchor="end" class="small" fill="#9b2226">Nominal 95%</text>')
write_svg('Fig_S2_interval_coverage.svg','\n'.join(parts),'Figure S2. Empirical interval coverage','Mean test coverage and sample standard deviation across nine fold-seed runs before and after validation-only scaling. The dashed red line marks the nominal 95% level.')
