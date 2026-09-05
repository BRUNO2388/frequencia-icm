from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

old = """  .filter-chip.active { background:var(--primary); border-color:var(--primary); color:#fff; }
  .status-badge-btn.ausente { background:var(--danger-bg); color:var(--danger-text); border-color:var(--danger-border); }"""

new = """  .filter-chip.active { background:var(--primary); border-color:var(--primary); color:#fff; }

  @media (max-width: 600px) {
    .filter-chips {
      flex-wrap: wrap;
      overflow-x: visible;
      align-items: center;
    }
    .filter-chip {
      flex: 0 0 auto;
    }
  }

  .status-badge-btn.ausente { background:var(--danger-bg); color:var(--danger-text); border-color:var(--danger-border); }"""

if s.count(old) != 1:
    raise SystemExit(f"Bloco de filtros não encontrado de forma única: {s.count(old)}")

s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")
