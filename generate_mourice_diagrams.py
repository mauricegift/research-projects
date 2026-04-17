"""Generate unique diagrams for Mourice's project documentation.

These diagrams are intentionally distinct from any used by James Ngovi
(same supervisor) to ensure the practical project documentation has its
own visual identity (system architecture, ER, use case, deployment,
sequence — none of which appear in James's research).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import os

OUT_DIR = 'mourice_figures'
os.makedirs(OUT_DIR, exist_ok=True)

PRIMARY = '#1f4e79'
ACCENT = '#2e75b6'
LIGHT = '#deebf7'
DARK = '#0f2c4a'
GREY = '#595959'


def _box(ax, x, y, w, h, text, fc=LIGHT, ec=PRIMARY, fontsize=9, bold=False):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.05",
                         linewidth=1.4, edgecolor=ec, facecolor=fc)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=weight, color=DARK, wrap=True)


def _arrow(ax, x1, y1, x2, y2, label='', style='->', color=GREY, ls='-'):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=14, linewidth=1.2,
                        color=color, linestyle=ls)
    ax.add_patch(a)
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.08, label, ha='center',
                va='bottom', fontsize=7.5, color=color, style='italic')


def fig_architecture():
    """Figure 6.1: 3-tier System Architecture."""
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7)
    ax.axis('off')

    # Tier labels
    for y, lbl in [(5.6, 'PRESENTATION TIER'),
                   (3.2, 'APPLICATION TIER'),
                   (0.8, 'DATA TIER')]:
        ax.text(0.15, y + 0.55, lbl, fontsize=8.5, fontweight='bold',
                color=PRIMARY, rotation=90, va='center')

    # Presentation
    _box(ax, 1.2, 5.4, 2.2, 1.0, 'Web Browser\n(Desktop)', fc='#fff4e6', ec='#bf6b04')
    _box(ax, 4.0, 5.4, 2.2, 1.0, 'Web Browser\n(Mobile)', fc='#fff4e6', ec='#bf6b04')
    _box(ax, 6.8, 5.4, 2.2, 1.0, 'Admin Console', fc='#fff4e6', ec='#bf6b04')

    # SPA layer
    _box(ax, 1.2, 4.1, 7.8, 0.8,
         'React 18 + TypeScript SPA  •  Vite Build  •  Tailwind CSS  •  shadcn/ui',
         fc=LIGHT, ec=ACCENT, bold=True)

    # API Gateway / Backend
    _box(ax, 1.2, 2.8, 7.8, 0.9,
         'FastAPI REST API  •  /api/auth  /api/notes  /api/past-papers  /api/admin',
         fc=LIGHT, ec=PRIMARY, bold=True)

    # Services
    _box(ax, 1.2, 1.6, 1.9, 0.8, 'JWT Auth\nService', fc='#e8f4ea', ec='#2d6a3a')
    _box(ax, 3.3, 1.6, 1.9, 0.8, 'Email/SMS\nOTP Service', fc='#e8f4ea', ec='#2d6a3a')
    _box(ax, 5.4, 1.6, 1.9, 0.8, 'File Storage\n& Validation', fc='#e8f4ea', ec='#2d6a3a')
    _box(ax, 7.5, 1.6, 1.5, 0.8, 'Logging /\nMonitoring', fc='#e8f4ea', ec='#2d6a3a')

    # Data tier
    _box(ax, 1.2, 0.4, 3.6, 0.9, 'MongoDB (Motor async)\nUsers • Notes • PastPapers • Blogs', fc='#fdecec', ec='#a04040', bold=True)
    _box(ax, 5.0, 0.4, 2.0, 0.9, 'Local File\nStorage (PDFs)', fc='#fdecec', ec='#a04040')
    _box(ax, 7.2, 0.4, 1.8, 0.9, 'External SMTP\n& SMS Gateway', fc='#fdecec', ec='#a04040')

    # Arrows between tiers
    for x in [2.3, 5.1, 7.9]:
        _arrow(ax, x, 5.4, x, 4.9)
    _arrow(ax, 5.1, 4.1, 5.1, 3.7, label='HTTPS / JSON')
    _arrow(ax, 5.1, 2.8, 5.1, 2.4)
    _arrow(ax, 3.0, 1.6, 3.0, 1.3)
    _arrow(ax, 6.0, 1.6, 6.0, 1.3)
    _arrow(ax, 8.2, 1.6, 8.2, 1.3)

    ax.set_title('Figure 6.1: BBM Annex Three-Tier System Architecture',
                 fontsize=10, fontweight='bold', color=DARK, pad=8)
    out = os.path.join(OUT_DIR, 'fig_6_1_architecture.png')
    plt.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return out


def fig_er_diagram():
    """Figure 6.2: Entity-Relationship diagram (crow's foot style)."""
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7)
    ax.axis('off')

    def entity(x, y, w, h, name, attrs):
        _box(ax, x, y + h - 0.5, w, 0.5, name, fc=PRIMARY, ec=DARK,
             fontsize=9.5, bold=True)
        # Attribute box
        box = Rectangle((x, y), w, h - 0.5, linewidth=1.2,
                        edgecolor=PRIMARY, facecolor='white')
        ax.add_patch(box)
        for i, a in enumerate(attrs):
            ax.text(x + 0.1, y + h - 0.75 - i*0.22, a,
                    fontsize=7.5, color=DARK, va='center')

    entity(0.2, 4.2, 2.4, 2.4, 'User',
           ['• _id (PK)', '• email', '• phone', '• password_hash',
            '• reg_no', '• specialisation', '• role', '• verified',
            '• created_at'])
    entity(3.6, 4.2, 2.4, 2.4, 'Note',
           ['• _id (PK)', '• title', '• subject_code', '• description',
            '• file_path', '• uploaded_by (FK)', '• status',
            '• downloads', '• created_at'])
    entity(7.0, 4.2, 2.6, 2.4, 'PastPaper',
           ['• _id (PK)', '• title', '• unit_code', '• year', '• semester',
            '• file_path', '• uploaded_by (FK)', '• status', '• downloads'])

    entity(0.2, 0.4, 2.4, 2.4, 'Blog',
           ['• _id (PK)', '• title', '• body', '• author_id (FK)',
            '• thumbnail', '• published', '• created_at'])
    entity(3.6, 0.4, 2.4, 2.4, 'Review',
           ['• _id (PK)', '• target_id (FK)', '• target_type',
            '• user_id (FK)', '• rating (1-5)', '• comment',
            '• created_at'])
    entity(7.0, 0.4, 2.6, 2.4, 'OTPCode',
           ['• _id (PK)', '• user_id (FK)', '• code', '• method',
            '• purpose', '• expires_at', '• used'])

    # Relationships (crow's foot indicated by N / 1 labels)
    _arrow(ax, 2.6, 5.4, 3.6, 5.4, label='1 ── N  uploads', style='-|>',
           color=PRIMARY)
    _arrow(ax, 2.6, 5.0, 7.0, 5.0, label='1 ── N  uploads', style='-|>',
           color=PRIMARY)
    _arrow(ax, 1.4, 4.2, 1.4, 2.8, label='1 ── N  authors', style='-|>',
           color=PRIMARY)
    _arrow(ax, 2.6, 4.4, 3.6, 1.6, label='1 ── N  writes', style='-|>',
           color=PRIMARY)
    _arrow(ax, 2.6, 4.6, 7.0, 1.6, label='1 ── N  requests', style='-|>',
           color=PRIMARY)
    _arrow(ax, 4.8, 4.2, 4.8, 2.8, label='reviews', style='-|>',
           color=ACCENT, ls='--')
    _arrow(ax, 8.2, 4.2, 6.0, 2.8, label='reviews', style='-|>',
           color=ACCENT, ls='--')

    ax.set_title('Figure 6.2: BBM Annex Database Entity-Relationship Diagram',
                 fontsize=10, fontweight='bold', color=DARK, pad=8)
    out = os.path.join(OUT_DIR, 'fig_6_2_er_diagram.png')
    plt.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return out


def fig_use_case():
    """Figure 6.3: Use case diagram with three actors."""
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7)
    ax.axis('off')

    # System boundary
    sys_box = Rectangle((2.4, 0.4), 5.2, 6.2, linewidth=1.5,
                        edgecolor=PRIMARY, facecolor='#f7fafd', linestyle='-')
    ax.add_patch(sys_box)
    ax.text(5.0, 6.4, 'BBM Annex Platform', ha='center', fontsize=10,
            fontweight='bold', color=PRIMARY)

    # Actors (stick-figure circles)
    def actor(x, y, name):
        ax.plot([x], [y + 0.45], marker='o', markersize=14, color=DARK,
                markerfacecolor='white', markeredgewidth=1.5)
        ax.plot([x, x], [y + 0.4, y - 0.05], color=DARK, linewidth=1.5)
        ax.plot([x - 0.25, x + 0.25], [y + 0.2, y + 0.2], color=DARK,
                linewidth=1.5)
        ax.plot([x - 0.2, x, x + 0.2], [y - 0.5, y - 0.05, y - 0.5],
                color=DARK, linewidth=1.5)
        ax.text(x, y - 0.85, name, ha='center', fontsize=9,
                fontweight='bold', color=DARK)

    actor(1.0, 4.5, 'Student')
    actor(1.0, 1.8, 'Guest')
    actor(9.0, 3.2, 'Admin')

    # Use cases (ellipses)
    use_cases = [
        (5.0, 5.6, 1.5, 0.45, 'Register / Verify'),
        (5.0, 4.8, 1.5, 0.45, 'Login (Email/Phone)'),
        (5.0, 4.0, 1.5, 0.45, 'Upload Notes / Papers'),
        (5.0, 3.2, 1.5, 0.45, 'Browse & Download'),
        (5.0, 2.4, 1.5, 0.45, 'Review Content'),
        (5.0, 1.6, 1.5, 0.45, 'Read Blog Posts'),
        (5.0, 0.8, 1.5, 0.45, 'Approve / Reject Uploads'),
    ]
    for (x, y, w, h, name) in use_cases:
        ell = mpatches.Ellipse((x, y), w*1.7, h*1.6, linewidth=1.2,
                               edgecolor=ACCENT, facecolor=LIGHT)
        ax.add_patch(ell)
        ax.text(x, y, name, ha='center', va='center', fontsize=8.2,
                color=DARK)

    # Lines from actors to use cases
    for (_, y, *_), allowed in zip(use_cases,
                                   [True, True, True, True, True, True, False]):
        if allowed:
            _arrow(ax, 1.25, 4.5, 4.0, y, style='-', color=GREY)
    for (_, y, *_), allowed in zip(use_cases,
                                   [True, False, False, True, False, True, False]):
        if allowed:
            _arrow(ax, 1.25, 1.8, 4.0, y, style='-', color=GREY)
    for (_, y, *_), allowed in zip(use_cases,
                                   [False, True, False, True, False, True, True]):
        if allowed:
            _arrow(ax, 8.75, 3.2, 6.0, y, style='-', color=GREY)

    ax.set_title('Figure 6.3: BBM Annex Use Case Diagram',
                 fontsize=10, fontweight='bold', color=DARK, pad=8)
    out = os.path.join(OUT_DIR, 'fig_6_3_use_case.png')
    plt.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return out


def fig_deployment():
    """Figure 6.4: Deployment architecture diagram."""
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.axis('off')

    # Client side
    _box(ax, 0.2, 4.4, 2.2, 1.2, 'End-User Devices\n(Browser / Mobile)',
         fc='#fff4e6', ec='#bf6b04', bold=True)

    # CDN / Domain
    _box(ax, 0.2, 2.4, 2.2, 1.0,
         'Public DNS\nbbm.giftedtech.co.ke\n(HTTPS / TLS)',
         fc=LIGHT, ec=ACCENT, bold=True)

    # Frontend hosting
    _box(ax, 3.0, 4.4, 3.2, 1.2,
         'GitHub Pages /\nStatic Host\n(React SPA build)',
         fc='#e8f4ea', ec='#2d6a3a', bold=True)

    # Reverse proxy
    _box(ax, 3.0, 2.4, 3.2, 1.0,
         'Nginx Reverse Proxy\n(TLS termination, rate limiting)',
         fc=LIGHT, ec=PRIMARY, bold=True)

    # VPS box (group)
    vps = Rectangle((6.6, 0.4), 3.2, 5.2, linewidth=1.5,
                    edgecolor=PRIMARY, facecolor='#f4f8fc', linestyle='--')
    ax.add_patch(vps)
    ax.text(8.2, 5.4, 'Production VPS Server', ha='center', fontsize=9,
            fontweight='bold', color=PRIMARY)

    _box(ax, 6.8, 4.0, 2.8, 0.9, 'Gunicorn + Uvicorn\nWorkers (FastAPI)',
         fc=LIGHT, ec=PRIMARY)
    _box(ax, 6.8, 2.8, 2.8, 0.9, 'MongoDB Service\n(localhost:27017)',
         fc='#fdecec', ec='#a04040')
    _box(ax, 6.8, 1.6, 2.8, 0.9, 'Local File Store\n(/uploads)',
         fc='#fdecec', ec='#a04040')
    _box(ax, 6.8, 0.5, 2.8, 0.9, 'Systemd Service\n+ Log Rotation',
         fc='#e8f4ea', ec='#2d6a3a')

    # External services
    _box(ax, 0.2, 0.5, 2.2, 1.0, 'External SMTP\n(Email OTP)',
         fc='#fdecec', ec='#a04040')
    _box(ax, 3.0, 0.5, 3.2, 1.0, 'SMS Gateway\n(PROCALL Sender ID)',
         fc='#fdecec', ec='#a04040')

    # Arrows
    _arrow(ax, 1.3, 4.4, 1.3, 3.4, label='HTTPS')
    _arrow(ax, 2.4, 2.9, 3.0, 2.9, label='resolves')
    _arrow(ax, 4.6, 4.4, 4.6, 3.4, label='static assets')
    _arrow(ax, 6.2, 2.9, 6.8, 4.4, label='/api/* proxy')
    _arrow(ax, 8.2, 4.0, 8.2, 3.7)
    _arrow(ax, 8.2, 2.8, 8.2, 2.5)
    _arrow(ax, 6.8, 4.4, 2.4, 1.0, ls='--')
    _arrow(ax, 6.8, 4.4, 4.6, 1.0, ls='--')

    ax.set_title('Figure 6.4: BBM Annex Deployment Architecture',
                 fontsize=10, fontweight='bold', color=DARK, pad=8)
    out = os.path.join(OUT_DIR, 'fig_6_4_deployment.png')
    plt.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return out


def fig_sequence():
    """Figure 6.5: Authentication sequence diagram."""
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.axis('off')

    actors = ['User', 'React SPA', 'FastAPI', 'MongoDB', 'Email/SMS']
    xs = [1.0, 3.0, 5.0, 7.0, 9.0]
    for x, a in zip(xs, actors):
        _box(ax, x - 0.6, 7.2, 1.2, 0.5, a, fc=PRIMARY, ec=DARK,
             fontsize=9, bold=True)
        ax.plot([x, x], [0.4, 7.2], color=GREY, linestyle='--', linewidth=0.8)

    # Sequence steps (y descending)
    steps = [
        (0, 1, 6.6, 'Submit credentials'),
        (1, 2, 6.2, 'POST /api/auth/login'),
        (2, 3, 5.8, 'Find user by email/phone'),
        (3, 2, 5.4, 'User document'),
        (2, 2, 5.0, 'Verify password (bcrypt)'),
        (2, 4, 4.6, 'Generate + send OTP'),
        (4, 0, 4.2, 'OTP delivered'),
        (0, 1, 3.6, 'Submit OTP code'),
        (1, 2, 3.2, 'POST /api/auth/verify'),
        (2, 3, 2.8, 'Validate OTP & mark used'),
        (3, 2, 2.4, 'OK'),
        (2, 2, 2.0, 'Issue JWT (5-day exp)'),
        (2, 1, 1.6, '200 OK + access token'),
        (1, 0, 1.2, 'Redirect to Dashboard'),
    ]
    for (s, t, y, label) in steps:
        x1, x2 = xs[s], xs[t]
        if s == t:
            ax.text(x1, y, '⟳ ' + label, fontsize=7.5, color=DARK,
                    ha='left', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', fc=LIGHT,
                              ec=ACCENT, lw=0.8))
        else:
            _arrow(ax, x1, y, x2, y, style='->', color=DARK)
            ax.text((x1 + x2)/2, y + 0.08, label, fontsize=7.5, ha='center',
                    color=DARK)

    ax.set_title('Figure 6.5: BBM Annex Authentication Sequence Flow',
                 fontsize=10, fontweight='bold', color=DARK, pad=8)
    out = os.path.join(OUT_DIR, 'fig_6_5_sequence.png')
    plt.savefig(out, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return out


def generate_all():
    figs = [fig_architecture(), fig_er_diagram(), fig_use_case(),
            fig_deployment(), fig_sequence()]
    for f in figs:
        print('Generated:', f)
    return figs


if __name__ == '__main__':
    generate_all()
