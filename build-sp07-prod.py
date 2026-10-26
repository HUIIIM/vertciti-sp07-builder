#!/usr/bin/env python3
"""Build the SP-07 production index.html from the D111-safe base.
Applies: v1.1 logo syntax normalization + 6 SP-07 edits. Fails loudly if any
anchor is not found exactly once.
"""
import argparse
import re, sys

ap = argparse.ArgumentParser(description="Build SP-07 production index.html from the D111-safe base.")
ap.add_argument("--src", default="/tmp/prod_vc.html", help="input base HTML (default: /tmp/prod_vc.html)")
ap.add_argument("--dst-dir", required=True,
                help="output directory for index.html (required)")
args = ap.parse_args()

SRC = args.src
DST_DIR = args.dst_dir
DST = DST_DIR + "/index.html"

with open(SRC, encoding="utf-8") as f:
    html = f.read()
orig_len = len(html)

def rep(old, new, label):
    global html
    n = html.count(old)
    if n != 1:
        sys.exit(f"ASSERT FAIL [{label}]: anchor found {n}x (expected 1)")
    html = html.replace(old, new)
    print(f"ok [{label}]")

# ---- 1. logo v1.1 syntax normalization (zero visual change) ----
rep('<path d="M20 10 28 30"/>', '<path d="M20,10 L28,30"/>', "logo-p1")
rep('<path d="M44 10 36 30"/>', '<path d="M44,10 L36,30"/>', "logo-p2")
rep('<path d="M26 35.5 32 45 38 35.5"/>', '<path d="M26,35.5 L32,45 L38,35.5"/>', "logo-p3")

# ---- 2. CHECKOUT_CONFIG.paymentLinks += SP-07 ----
rep(
    "'SP-06':'https://buy.stripe.com/14A8wI4rI7DGcxo8r7ffy05'\n  }),",
    "'SP-06':'https://buy.stripe.com/14A8wI4rI7DGcxo8r7ffy05',\n"
    "    'SP-07':'https://buy.stripe.com/fZu6oA3nEbTW7d49vbffy06'\n  }),",
    "paymentLinks",
)

# ---- 3. fee map += SP-07 ----
rep(
    "'SP-06':{fee:29,zh:'首单体验包',en:'First-Order Trial Pack'}};}",
    "'SP-06':{fee:29,zh:'首单体验包',en:'First-Order Trial Pack'},"
    "'SP-07':{fee:249,zh:'AI 电话接待员首单试行包',en:'AI Receptionist Trial Pack'}};}",
    "fee-map",
)

# ---- 4. delivery map += SP-07 (refundable deposit terms) ----
rep(
    "'SP-06':{zh:'加急交付（优先排期，约 1–2 个工作日）、交付后 7 天内 1 次追问',"
    "en:'Rush delivery (priority queue, about 1–2 business days) + 1 follow-up within 7 days after delivery'}};",
    "'SP-06':{zh:'加急交付（优先排期，约 1–2 个工作日）、交付后 7 天内 1 次追问',"
    "en:'Rush delivery (priority queue, about 1–2 business days) + 1 follow-up within 7 days after delivery'},"
    "'SP-07':{zh:'可全额退款的验证申请金；书面确认服务范围后才执行，确认前随时可全额退款',"
    "en:'Fully refundable validation deposit; execution only after written scope confirmation, "
    "full refund available anytime before confirmation'}};",
    "delivery-map",
)

# ---- 5. phone card: deposit terms in description, badge UNCHANGED (D111), trial link ----
rep(
    "d:zh?'来电自动接听、智能预约、转人工；首批面向美国本地服务企业验证中。':"
    "'Automatic call answering, smart scheduling, and human handoff; "
    "first batch verifying with US home-service businesses.',",
    "d:zh?'来电自动接听、智能预约、转人工；首批面向美国本地服务企业验证中。"
    "首单试行申请金 $249（可全额退款）：书面确认服务范围后才执行，确认前随时可全额退款。':"
    "'Automatic call answering, smart scheduling, and human handoff; "
    "first batch verifying with US home-service businesses. "
    "First-trial application deposit $249 (fully refundable): execution only after written scope confirmation, "
    "full refund available anytime before confirmation.',",
    "phone-card-desc",
)
rep(
    "'🟡 First batch · Working on it')+'</span>',first:true,cta:true},",
    "'🟡 First batch · Working on it')+'</span>',first:true,cta:true,"
    "trial:CHECKOUT_CONFIG.paymentLinks['SP-07']},",
    "phone-card-trial",
)

# ---- 6. card template: trial CTA; suppress notify when trial exists ----
# NOTE: this region uses PLAIN quotes (no backslash escapes) - verified by hex
_old6 = """'+(c.cta?'<button type="button" class="btn small" data-cfg="open">'+(zh?'进入配置器':'Open configurator')+'</button>':'')+'<button type="button" class="btn small alt" data-cfg="notify">'+(zh?'到货通知我':'Notify me')+'</button></div>"""
_new6 = """'+(c.trial?'<a class="btn small" target="_blank" rel="noopener" href="'+c.trial+'">'+(zh?'申请首批验证 · $249':'Apply for pilot · $249')+'</a>':'')+(c.cta?'<button type="button" class="btn small" data-cfg="open">'+(zh?'进入配置器':'Open configurator')+'</button>':'')+(!c.trial?'<button type="button" class="btn small alt" data-cfg="notify">'+(zh?'到货通知我':'Notify me')+'</button>':'')+'</div>"""
n = html.count(_old6)
if n != 1:
    sys.exit(f"ASSERT FAIL [card-template]: anchor found {n}x (expected 1)")
html = html.replace(_old6, _new6)
print("ok [card-template]")

# ---- 7. blueprint intro: honest pilot-application clause ----
rep(
    "zh?'蓝图一次看全，验证一个、开放一个。状态标不是上架：没经过实测的品类不接受下单、不承诺日期。'",
    "zh?'蓝图一次看全，验证一个、开放一个。状态标不是上架：没经过实测的品类不接受下单、不承诺日期。"
    "首批验证开放申请：申请金可全额退款，书面确认服务范围后才执行。'",
    "intro-zh",
)
rep(
    "A status badge is not a listing — unverified categories take no orders and promise no dates.')",
    "A status badge is not a listing — unverified categories take no orders and promise no dates. "
    "First-batch validation is open for applications: the deposit is fully refundable, "
    "execution only after written scope confirmation.')",
    "intro-en",
)

import os
os.makedirs(DST_DIR, exist_ok=True)
with open(DST, "w", encoding="utf-8") as f:
    f.write(html)
print(f"wrote {DST} ({orig_len} -> {len(html)} bytes)")

# ---- JS syntax check: extract inline <script> blocks and node --check ----
# only real JS: skip type=application/json, application/ld+json, etc.
scripts = []
for m in re.finditer(r"<script([^>]*)>(.*?)</script>", html, re.S):
    attrs, code = m.group(1), m.group(2)
    if re.search(r"\bsrc\s*=", attrs):
        continue
    tm = re.search(r"type\s*=\s*[\"']([^\"']+)[\"']", attrs)
    if tm and "javascript" not in tm.group(1).lower():
        continue  # application/json, ld+json, etc.
    scripts.append(code)
print(f"found {len(scripts)} inline JS blocks")
import subprocess, tempfile
for i, code in enumerate(scripts):
    if not code.strip():
        continue
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tf:
        tf.write(code)
        tf.flush()
        r = subprocess.run(["node", "--check", tf.name], capture_output=True, text=True)
    os.unlink(tf.name)
    if r.returncode != 0:
        sys.exit(f"JS SYNTAX FAIL block {i}:\n{r.stderr[:2000]}")
    print(f"js ok block {i} ({len(code)} chars)")
print("ALL CHECKS PASSED")
