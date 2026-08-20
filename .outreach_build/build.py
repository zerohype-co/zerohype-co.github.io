#!/usr/bin/env python3
"""
Build script for the 10 outreach-scripts pages.
Content lives below; CSS, nav, CTA, footer, and skip-link are byte-identical to the
reference page (guides/outreach-scripts-cto-austria/index.html from git history),
minus the Cloudflare beacon and email-obfuscation artifacts.
"""
import os, json

CSS = open('/tmp/ref_css.css').read()

NAV = """
    <nav>
      <a href="https://zerohypelab.com" class="nav-wordmark">Zero Hype</a>
      <ul class="nav-links">
        <li><a href="https://zerohypelab.com/manifesto/">Manifesto</a></li>
        <li><a href="https://zerohypelab.com/guides/" class="active">Guides</a></li>
        <li><a href="https://zerohypelab.substack.com">Substack Newsletter</a></li>
        <li><a href="https://x.com/zerohype_co">X</a></li>
        <li><a href="https://zerohypelab.com/about/">About</a></li>
      </ul>
    </nav>
"""

CTA = """
    <div class="cta-block">
      <h3>Get Your Outreach Sequence Audited</h3>
      <p>Send ZeroHype your outreach sequence. Get a detailed autopsy: what is wrong, why it is wrong, and exactly how to fix it. Delivered in 48 to 72 hours.</p>
      <a href="https://buy.stripe.com/3cI5kF87C6fu3MNbPEaR200" class="btn-yellow">Order an Outreach Autopsy &mdash; $99 &rarr;</a>
    </div>
"""

FOOT = """
  <footer>
    <div class="footer-inner">
      <span class="footer-wordmark">Zero Hype</span>
      <ul class="footer-links">
        <li><a href="https://zerohypelab.com/manifesto/">Manifesto</a></li>
        <li><a href="https://zerohypelab.com/guides/">Guides</a></li>
        <li><a href="https://zerohypelab.substack.com">Substack Newsletter</a></li>
        <li><a href="https://x.com/zerohype_co">X &mdash; @zerohype_co</a></li>
        <li><a href="https://www.youtube.com/@zerohype_co" target="_blank" rel="noopener">YouTube</a></li>
        <li><a href="https://www.producthunt.com/products/campaign-failure-predictor" target="_blank" rel="noopener">Product Hunt</a></li>
        <li><a href="https://zerohypelab.com/monthly-autopsy/">Monthly Autopsy &mdash; $300/mo</a></li>
        <li>Contact: <a href="mailto:zerohype@proton.me">zerohype@proton.me</a></li>
      </ul>
      <p class="footer-tagline">No fluff. No hype. Just what works. &middot; <time datetime="2026-07-22">Updated July 2026</time></p>
      <p class="footer-tagline">Published by <a href="https://zerohypelab.com/about/" style="color:var(--muted);">Zero Hype</a> &mdash; Contact: <a href="mailto:zerohype@proton.me">zerohype@proton.me</a></p>
    </div>
  </footer>
"""

SKIP = '  <a href="#main" class="skip-link">Skip to main content</a>'
GOAT = '\n  <script data-goatcounter="https://zerohype.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n</body>\n</html>'
NOTE = '\n<p style="font-size:13px;color:#999;font-style:italic;margin-top:24px">Fakten mit Bezug zu Schwellenwerten (Betriebsrat, BVG, BVergG, NISG, FFG/aws), Verordnungen (VSo), oder Branchen-Konventionen (GAV, Kollektivvertrag): die Existenz der Regelung ist verifizierbar, exakte Schwellen und Saetze sind hier als plauzibel gekennzeichnet und ohne Quelle nicht weiter spezifiziert. Vor einer kundenwirksamen Aussage mit Quelle gegenpruefen.</p>'

def split(s):
    if '. ' in s: return s.split('. ', 1)
    if s.endswith('.'): return s[:-1], ''
    return s, ''

def render(p):
    slug, title, desc, h1 = p["slug"], p["title"], p["description"], p["h1"]
    country = p["country"]
    url = f"https://zerohypelab.com/guides/{slug}/"
    intro = "".join(f"<p>{x}</p>" for x in p["intro"])
    b1 = "".join(f"<li><strong>{a}.</strong>{(' ' + b) if b else ''}</li>"
                for s in p["bullets_1"] for a, b in [split(s)])
    b2 = "".join(f"<li><strong>{a}.</strong>{(' ' + b) if b else ''}</li>"
                for s in p["bullets_2"] for a, b in [split(s)])
    rel = '<h3>Related ' + country + ' outreach-script material</h3>\n' \
          '<p style="font-size:15px;color:#888;margin-bottom:24px">Continuing the cluster: ' \
          + " &middot; ".join(f'<a href="https://zerohypelab.com/guides/{r[0]}/">{r[1]}</a>' for r in p["related"]) \
          + '</p>'
    jl = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": h1,
        "description": desc,
        "url": url,
        "publisher": {"@type": "Organization", "name": "ZeroHype", "url": "https://zerohypelab.com"}
    }, separators=(",", ":"), ensure_ascii=False)

    body = f"""<body>{SKIP}

  <div class="yellow-zone">
{NAV}
    <div class="page-hero">
      <div class="breadcrumb">
        <a href="https://zerohypelab.com">Home</a>
        <span class="sep">/</span>
        <a href="https://zerohypelab.com/guides/">Guides</a>
        <span class="sep">/</span>
        Outreach Scripts by Role
      </div>
      <span class="page-cluster">Outreach Scripts by Role</span>
      <h1 class="page-title">{h1}</h1>
    </div>
  </div>

  <main id="main">
    <p class="meta-bar">Zero Hype &middot; DACH B2B Sales &amp; Outreach</p>
    <div class="content">
{intro}
<h2>{p["h2_1"]}</h2>
<ul>{b1}</ul>
<h2>{p["h2_2"]}</h2>
<ul>{b2}</ul>
{rel}
{NOTE}
    </div>

{CTA}
  </main>

{FOOT}
{GOAT}"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="ZeroHype">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://zerohypelab.com/og-image.png">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://zerohypelab.com/og-image.png">
  <meta name="author" content="Zero Hype">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" href="/favicon.svg" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">
  <link rel="preload" as="font" href="/fonts/BebasNeue-400-normal.woff2" type="font/woff2" crossorigin>
  <link rel="preload" as="font" href="/fonts/Inter-400-normal.woff2" type="font/woff2" crossorigin>
  <script type="application/ld+json">{jl}</script>
  <style>{CSS}</style>
</head>
{body}"""

PAGES = [
{
"slug": "outreach-scripts-cfo-austria",
"title": "Outreach Scripts for Austrian CFOs | ZeroHype",
"description": "Austrian CFOs at KMU and Mittelstand companies evaluate vendors through Bilanz, Foerderungen, and the Greissler margin squeeze. What lands in the first email to an Austrian CFO.",
"h1": "Outreach Scripts for CFOs in Austria: Foerderungen, Bilanz, and the Greissler Margin",
"country": "Austrian",
"intro": [
"Austrian CFOs sit between two markets that rarely take advice from the same playbook. There is the Vienna-based corporate and scale-up finance function, where English-first outreach is acceptable, EBITDA is the primary lens, and capital allocation decisions move at quarterly cadence. There is the Provinz KMU and Mittelstand market, German-only, conservative, and structurally tighter on margins than a German counterpart of the same revenue band. The first conversation you have with an Austrian CFO runs differently depending on which room you walked into.",
"The baseline for both is the same. Austrian finance leadership is more measured than German finance leadership. Approval cycles run longer. The CFO is more often the final approver than a procurement committee. Anything that looks rushed, hype-driven, or English-only will be quietly dropped before the second touch.",
"Austrian finance has its own vocabulary, and using it correctly signals you have done your homework. Bilanz and GuV are the standard reporting references, not Balance Sheet and P&L. EBITDA is used, but operating cash flow matters more in the Provinz conversation. UGB (Unternehmensgesetzbuch) governs statutory accounting for most non-listed Austrian companies; IFRS applies to listed and large entities. Knowing which one your contact reports under changes how you frame savings and ROI.",
"The two conversations that move Austrian CFOs to a reply are Foerderungen and Greissler margin pressure. Austrian CFOs care deeply about FFG (Forschungsfoerderungsgesellschaft) and aws (Austria Wirtschaftsservice) grants because they affect cash flow and CapEx approval. They also care about the structural margin squeeze caused by Greissler-era supplier concentration, small, dated supplier bases that limit negotiating room. If your sequence connects to either of these, the open rate is materially higher."
],
"h2_1": "Key Differences When Targeting Austrian CFOs",
"bullets_1": [
"Vienna corporate CFOs vs KMU and Provinz CFOs. Vienna-based CFOs at scale-ups and corporate HQs work in English and read your email within an hour of landing. KMU and Mittelstand CFOs in provinces like Oberoesterreich, Steiermark, and Tirol expect German, allow two business days for a reply, and need at least one warm reference before the second email.",
"Titles matter and you should not abbreviate them. Use Mag. (Magister) and Dr. as prefixes when they appear on the contact's signature or LinkedIn. An opening line that gets the prefix wrong is not forgiven in this market.",
"Foerderungen are a decision factor, not a footnote. Austrian CFOs at KMU and Mittelstand companies actively track FFG R&D grants, aws Investitionspraemien, and WKO Exportfoerderung. A vendor message that maps its service to a Foerderung cash flow advantage is read twice and forwarded.",
"Greissler margin pressure is structural. Many Austrian CFOs operate in sectors (gastro, retail trade, hospitality, regional manufacturing) where supply chains still run through small, long-standing Greissler-style suppliers. Your outreach is more useful to them when you acknowledge this constraint rather than implying they can switch suppliers overnight.",
"Tax and reporting lens is UGB by default. Most Austrian KMU report under UGB, not IFRS or German HGB. Frame savings in Bilanz and GuV terms, not in IFRS-segment language. The CFO will not translate your numbers for you."
],
"h2_2": "What Gets a Reply from Austrian CFOs",
"bullets_2": [
"A specific reference to their last published Bilanz or annual report. Austrian CFOs are almost always personally involved in producing the annual report and will read an email that cites a specific line item from it.",
"Concrete Foerderungen framing. A line that links your offering to FFG, aws, or WKO support is a reply trigger. Do not invent subsidy categories, only reference the ones that genuinely apply to the buyer's industry.",
"Lead time signals, not urgency signals. Phrases like 'erstes Gespraech im naechsten Quartal' (first call next quarter) work better than 'only 3 spots left this month'. Austrian CFOs reward patience, not pressure.",
"A local Austrian case study in the first paragraph, not a global logo. An Austrian KMU reference from the same Bundesland is worth more than any Fortune 500 customer mention. The CFO will check it within ten minutes.",
"Forwarded to the right internal stakeholder. Sequence copy that names which role will review the proposal before the CFO closes the loop, controlling, IT, or operations, reads as legitimate and gets routed correctly."
],
"related": [
["outreach-scripts-hr-director-austria","Austrian HR Director outreach"],
["outreach-scripts-it-director-austria","Austrian IT Director outreach"],
["outreach-scripts-procurement-austria","Austrian Procurement outreach"],
["outreach-scripts-vp-sales-austria","Austrian VP Sales outreach"]
]
},
{
"slug": "outreach-scripts-hr-director-austria",
"title": "Outreach Scripts for Austrian HR Directors | ZeroHype",
"description": "Austrian HR directors navigate Betriebsrat thresholds, Kollektivvertrag impact on payroll, and Abfertigung Neu obligation. Cultural and legal specifics that get an Austrian HR reply.",
"h1": "Outreach Scripts for HR Directors in Austria: Betriebsrat, Kollektivvertrag, and Bildungskarenz",
"country": "Austrian",
"intro": [
"Austrian HR is a separate profession from German HR in two ways that matter to a sales conversation. First, the Betriebsrat (works council) is legally anchored at a different threshold than in Germany and has a different scope of co-determination rights. Second, the Kollektivvertrag (collective agreement) is mandatory in most sectors and caps what an HR director can do unilaterally on compensation, working time, and benefits. A pitch that ignores these is a pitch that lands at the wrong desk.",
"Beyond the structural floor, Austrian HR directors are more conservative on tooling than their German or Swiss counterparts. They are early to audit, late to deploy, and structurally cautious about anything that touches employee data, performance, or working time tracking. SaaS that works in Berlin or Zurich is treated as a six-month evaluation in Vienna.",
"The two levers that move Austrian HR conversations are compliance and subsidies. Austrian HR directors care about clean Betriebsrat pathways, audit-ready records for Betriebsinspektorat or Arbeitsinspektorat, and Foerderungen the company might be leaving on the table. Bildungskarenz, WKO Lehrlingsfoerderung, and aws personnel-related subsidies are real cash flows that HR directors actively track.",
"What does not move Austrian HR is English-only positioning. Inside Wien there is a thin layer of international HR functions that read in English, but the majority of Austrian HR directors expect German and reward persistence without pressure. The first email is rarely the email that gets the meeting."
],
"h2_1": "Key Differences When Targeting Austrian HR Directors",
"bullets_1": [
"Betriebsrat thresholds and scope. Austrian Betriebsrat law (Arbeitsverfassungsgesetz) sets different thresholds than German Betriebsverfassungsgesetz. The Austrian threshold and the specific co-determination rights depend on company size and sector. A pitch to a 30-employee Austrian company that assumes German-style works council rights will confuse the HR director.",
"Kollektivvertrag impact on payroll decisions. Austrian HR cannot set compensation unilaterally in companies bound by a Kollektivvertrag. The minimum wages, salary scales, and benefits are already fixed. Your sequence must position around what the HR director can change (process, tooling, training) rather than what they cannot (headcount cost structure).",
"Abfertigung Neu vs Alt distinction. The Abfertigung system changed in 2003. Neue Arbeitsverhaeltnisse (started after 2003) follow the Abfertigung Neu framework; older contracts follow Abfertigung Alt. HR directors often run both populations in parallel. Anything HR analytics related must handle this dual-track correctly.",
"Bildungskarenz and AMS subsidies. Austrian HR directors have access to subsidized educational leave via Bildungskarenz and AMS support. Tools that enable educational tracking or upskilling paths are more valuable when framed against this subsidy.",
"Austrian data protection default. The Austrian DSG (Datenschutzgesetz) implementation of GDPR applies locally and the DSB (Datenschutzbehoerde) is engaged frequently on employee data issues. HR tooling that hand-waves past Austrian DSB practice reads as foreign and gets bounced."
],
"h2_2": "What Gets a Reply from Austrian HR Directors",
"bullets_2": [
"A reference to a specific Kollektivvertrag or Betriebsrat clause. Austrian HR directors are impressed by outreach that cites a specific clause they work with daily. Use the correct KV name (Handel, Gewerbe, Industrie, or Informationstechnologie for IT-adjacent roles).",
"A clean Betriebsrat pathway. A vendor offering that names the Betriebsrat introduction process explicitly, in writing, gets engagement. Austrian HR directors do not want to figure out your product's compliance workflow themselves.",
"Bildungskarenz or WKO Lehrlingsfoerderung framing. Tools that map to a specific Foerderung are read twice. Avoid invented subsidy categories; use only the ones the HR director can actually claim.",
"Reference to a local Austrian employer of similar size and sector. Austrian HR directors trust Austrian case studies above German ones. A Mittelstand reference from Steiermark is worth more than a DAX-40 reference.",
"Bilingual (German plus English) UI commitment. Austrian HR directors want German as default but expect English as fallback for international subsidiaries. A pitch that commits to both languages in writing wins."
],
"related": [
["outreach-scripts-cfo-austria","Austrian CFO outreach"],
["outreach-scripts-it-director-austria","Austrian IT Director outreach"],
["outreach-scripts-procurement-austria","Austrian Procurement outreach"],
["outreach-scripts-vp-sales-austria","Austrian VP Sales outreach"]
]
},
{
"slug": "outreach-scripts-it-director-austria",
"title": "Outreach Scripts for Austrian IT Directors | ZeroHype",
"description": "Austrian IT directors balance NISG 2024 obligations, EU data residency, and the Vienna startup vs Provinz Mittelstand split. How to land an Austrian IT outreach.",
"h1": "Outreach Scripts for IT Directors in Austria: NISG, Datensouveraenitaet, and the Vienna-Provinz Split",
"country": "Austrian",
"intro": [
"Austrian IT directors sit between two stacks and two regulatory realities. The Vienna startup and scale-up IT function has cloud-native defaults, an English-first vendor stack, and quick evaluation cycles. The Provinz Mittelstand and KMU IT function is on-prem heavy, German-speaking, audit-driven, and structurally tied to the same NISG 2024 and upcoming NIS-2 implementation as every other EU IT leader. Knowing which seat your contact sits in changes the outreach radically.",
"Beyond the market split, Austrian IT directors have inherited a compliance load that German IT directors in the same revenue band do not carry. NISG 2024 expanded the scope of operators of essential services; NIS-2, transposed across the EU over 2024 to 2026, layers additional obligations. Austrian IT directors in regulated sectors (energy, finance, healthcare, pharma) carry GAMP 5 or similar validation expectations that are absent in pure-SaaS markets.",
"Austrian IT has a specific vantage point on data sovereignty that does not exist in Germany. Austrian regulators are cautious about US-only data residency; Austrian hosting providers (A1, T-Systems Austria, World4You, Atos Austria) carry weight in this market. Cloud architecture decisions are typically accompanied by an explicit EU or Austria residency assertion.",
"What does not move Austrian IT is hype. The Austrian Mittelstand IT director is deaf to 'AI-powered', 'revolutionary', '10x'. They are listening for evidence of auditability, vendor stability, and an Austrian or EU reference customer."
],
"h2_1": "Key Differences When Targeting Austrian IT Directors",
"bullets_1": [
"Vienna startup IT vs Provinz Mittelstand IT. Vienna startup IT reads in English, evaluates in days, and prefers API-first cloud-native vendors. Provinz Mittelstand IT reads in German, evaluates in months, and needs on-prem or hybrid deployment options to clear internal review.",
"NISG 2024 and NIS-2 awareness. Austrian IT directors in essential services (energy, water, transport, finance, healthcare) carry direct NISG obligations; many others fall under NIS-2 transposition timelines. Your sequence is more useful when it acknowledges which framework applies to the buyer.",
"Datensouveraenitaet and hosting locality. Austrian IT directors are more cautious about US-only cloud than German IT directors. EU or Austria-resident hosting is a differentiator; AWS Frankfurt or Azure West Europe alone is no longer a default.",
"GAMP 5 and validation in regulated sectors. Austrian IT directors serving pharma or medical device customers carry validation expectations (IQ/OQ/PQ, audit trails, change control). Your offering is differentiated when it acknowledges and supports these, and disqualified when it does not.",
"Betriebsrat involvement in employee monitoring tooling. Austrian IT directors consult the Betriebsrat on any tool that touches employee productivity, screen, or communication data. Tools that arrive without a pre-built Betriebsrat pathway create project risk."
],
"h2_2": "What Gets a Reply from Austrian IT Directors",
"bullets_2": [
"A reference to a specific Austrian or EU reference customer in the same regulatory category. Austrian IT directors reject global logos as primary evidence; a comparable Austrian entity is the signal they trust.",
"Explicit NISG or NIS-2 mapping. A one-page note on which NISG clauses your product addresses gets forwarded. Vendors that hand-wave past compliance are filtered out early.",
"Local hosting option documented in writing. EU or Austria hosting, even as one option, reads as serious; nothing reads as more serious than an Austrian DC reference.",
"Operability with Austrian KMS, identity, and audit stack. Austrian IT directors prefer solutions that work with Austrian-managed A-Trust certificates, Austrian password vaulting, and Austrian-resident logging.",
"Pre-built Betriebsrat communication template. Austrian IT directors will reject any tooling that requires them to negotiate the Betriebsrat introduction from scratch. A pre-written sequence of committee-ready materials wins."
],
"related": [
["outreach-scripts-cfo-austria","Austrian CFO outreach"],
["outreach-scripts-hr-director-austria","Austrian HR Director outreach"],
["outreach-scripts-procurement-austria","Austrian Procurement outreach"],
["outreach-scripts-vp-sales-austria","Austrian VP Sales outreach"]
]
},
{
"slug": "outreach-scripts-procurement-austria",
"title": "Outreach Scripts for Austrian Procurement Leads | ZeroHype",
"description": "Austrian procurement runs on Bundesvergabegesetz thresholds, GATT/WTO GPA, and a Greissler-heavy supplier base. How a vendor lands the first conversation with Austrian Einkauf.",
"h1": "Outreach Scripts for Procurement Leads in Austria: BVergG, ESG-Sorgfalt, and the Greissler-Lieferant",
"country": "Austrian",
"intro": [
"Austrian procurement is a smaller, more tightly scoped profession than German procurement. The Bundesvergabegesetz (BVergG) governs public tenders; GATT/WTO GPA governs cross-border tender rules; private procurement at KMU and Mittelstand companies is governed by internal policy more than by law. Knowing which frame applies to your contact changes both the entry angle and the objection set.",
"Austrian procurement leads also operate in a supply landscape that is structurally different from Germany. The Mittelstand supplier base in many Austrian sectors is built on long-standing Greissler relationships, small, sometimes family-run, often decades-old. Breaking into this means acknowledging that the incumbent relationship is real and showing a credible migration path.",
"The two regulatory frames that have changed Austrian procurement in the last three years are ESG due diligence and data localization in tenders. The Austrian Lieferkettensorgfaltspflichtengesetz (similar in spirit to the German LkSG) requires companies above thresholds to audit their supply chains. Procurement is now the function responsible for carrying that audit. Public procurement increasingly requires local residency or EU residency as a hard criterion.",
"What does not move Austrian procurement is generic ROI. Austrian Einkauf reads ROI as a given; they need proof of category insight, structural fit, and an Austrian or DACH reference customer."
],
"h2_1": "Key Differences When Targeting Austrian Procurement Leads",
"bullets_1": [
"BVergG thresholds and public tender discipline. Austrian public procurement thresholds under BVergG 2018 (and its amendments) differ from those in other EU jurisdictions. Vendors selling to Austrian public bodies must understand these thresholds for both EU-wide and Austria-only tenders; the same logic applies to GATT/WTO GPA when crossing borders.",
"Greissler and Mittelstand incumbent supplier base. Austrian Einkauf often inherits supplier relationships that are person-bound and decades-long. Your outreach that maps the migration path (not just the cost cut) reads as legitimate; outreach that pitches raw displacement reads as naive.",
"Lieferkettensorgfaltspflichtengesetz obligations. Austrian companies in scope are expected to document supplier ESG performance. Vendors that offer ESG-aligned audit, traceability, or documentation support are read seriously; vendors that ignore this frame lose on TCO even when price is competitive.",
"Heimische Lieferantenpraeferenz where legally allowed. Austrian procurement teams face internal pressure to favor Austrian and EU suppliers where the rules permit. Not a hard rule, but worth mapping to your positioning.",
"Logistics and regional distribution logic. Austrian geography (Alpen, Ost-Tirol, Vorarlberg, Weinviertel) creates a delivery-cost dynamic that German procurement does not face. Vendors that can credibly commit on lead times win."
],
"h2_2": "What Gets a Reply from Austrian Procurement Leads",
"bullets_2": [
"A reference to a specific Austrian public tender or procurement framework. Procurement leads are impressed when you cite a BVergG-adjacent example or a publicly named reference customer.",
"ESG due diligence documentation ready. Not a marketing claim; actual certificates, audit reports, and supplier code of conduct materials that can be filed into their internal documentation system.",
"Migration path from incumbent supplier. Austrian Einkauf wants the change story, not just the price cut. A two-quarter migration plan that preserves incumbent relationship data and validates handover risk is the language they trust.",
"Austrian or DACH logistics footprint. Vendors with an Austrian warehouse, a regional carrier partner, or a reliable Oesterreich-lieferbar commitment in writing close faster than vendors without one.",
"Invoice and procurement-system integration. Austrian companies run on SAP, BMD, or in smaller setups on RZL and Dynamics. Pre-built connectors and known implementation partners shorten the procurement cycle."
],
"related": [
["outreach-scripts-cfo-austria","Austrian CFO outreach"],
["outreach-scripts-hr-director-austria","Austrian HR Director outreach"],
["outreach-scripts-it-director-austria","Austrian IT Director outreach"],
["outreach-scripts-vp-sales-austria","Austrian VP Sales outreach"]
]
},
{
"slug": "outreach-scripts-vp-sales-austria",
"title": "Outreach Scripts for Austrian VP Sales | ZeroHype",
"description": "Austrian VP Sales navigate two markets (Vienna startup speed vs Provinz Mittelstand rhythm), distinct Verkaufsleiter vs Vertriebsleiter terminology, and a Schmaeh-toned buyer. Cultural fit for Austrian sales outreach.",
"h1": "Outreach Scripts for VP Sales in Austria: Schmaeh, KAM, and the Wien-Provinz Rhythm",
"country": "Austrian",
"intro": [
"Austrian sales is two jobs wearing one title. The VP Sales at a Vienna scale-up is on a quarterly cadence, evaluates tooling in days, and treats sales enablement like a Berlin peer would. The Vertriebsleiter or Verkaufsleiter at an Austrian Mittelstand company in Steiermark, Oberoesterreich, or Vorarlberg is on a multi-quarter cadence, evaluates tooling against a long-standing internal process, and is structurally more conservative on vendor churn. A pitch that fits the first will land at the wrong company for the second.",
"Austrian sales has a vocabulary that signals cultural fit or its absence. Schmaeh is the wry, understated humor that runs through Austrian business conversation; it is not something to manufacture, but something to recognize. Greissler-style channel relationships still operate in many sectors; ignoring them is a missed signal. The Wien-Provinz dynamic is genuine and present in every sales conversation. A vendor who reads this and reflects it back gets traction; a vendor who treats Austria as a homogenous German market stalls.",
"KAM (Key Account Management) in Austrian Mittelstand is structurally tighter than in German Mittelstand. Account portfolios are smaller; relationships are denser; cross-selling and up-selling require a personal touch that global sales plays do not tolerate. Tools that help Austrian sales teams map account context, multi-stakeholder access, and relationship history earn their budget; tools that try to replace these relationships do not.",
"What does not move Austrian VP Sales is urgency. Austrian VP Sales is structurally allergic to countdown timers, scarcity messaging, and aggressive multi-channel cadences. Patience and specificity beat pressure."
],
"h2_1": "Key Differences When Targeting Austrian VP Sales",
"bullets_1": [
"Wien vs Provinz cadence. Vienna VP Sales wants speed and a tight evaluation loop. Provinz VP Sales treats the first two emails as orientation and the third as the trigger. Same person, different company, different cadence.",
"Verkaufsleiter vs Vertriebsleiter titles. Both translate as 'Head of Sales' but signal different scopes. Verkaufsleiter is usually narrower (outbound, often consumer or retail); Vertriebsleiter tends to cover broader distribution. Use the title the contact uses.",
"KAM portfolio density. Austrian VP Sales typically manages smaller but denser account portfolios than a German counterpart of same company size. Outreach that acknowledges '5-10 named accounts' rather than '500-1000' lands better.",
"Multi-channel cadence tolerance. Austrian VP Sales prefers email plus a single phone call or a face-to-face meeting, not LinkedIn plus email plus phone plus retargeting plus ads. Sequences built for Berlin density are too aggressive for Vienna moderation.",
"Reference customer weight. Austrian VP Sales reads Austrian logos in the same sector and same revenue band as more meaningful than global logos. A local Austrian Mittelstand reference will close deals that a global logo cannot."
],
"h2_2": "What Gets a Reply from Austrian VP Sales",
"bullets_2": [
"A reference to one of their named accounts. Austrian VP Sales is impressed by outreach that names a specific Austrian key account (not always a customer). Skip generic personalization; show you read the press release.",
"Quartalsbezug framing, not urgency. Phrases like 'fuer Q1 naechstes Jahr vorzumerken' (file for next year Q1) work. Urgency cues ('this week', 'only 3 spots') are filtered.",
"Austrian Mittelstand reference as primary evidence. A Steiermark-based Mittelstand reference with same revenue band closes. A Siemens or BMW reference does not.",
"Tools that map to KAM realities. Account context, multi-stakeholder mapping, and deal history score higher than AI-driven outbound automation in this market.",
"Personal contact and a single follow-up channel. VP Sales in Austria responds to a personal email with a known sender name; cold sequences from managed accounts do not perform."
],
"related": [
["outreach-scripts-cfo-austria","Austrian CFO outreach"],
["outreach-scripts-hr-director-austria","Austrian HR Director outreach"],
["outreach-scripts-it-director-austria","Austrian IT Director outreach"],
["outreach-scripts-procurement-austria","Austrian Procurement outreach"]
]
},
{
"slug": "outreach-scripts-cfo-switzerland",
"title": "Outreach Scripts for Swiss CFOs | ZeroHype",
"description": "Swiss CFOs balance Swiss GAAP FER, FINMA-aware reporting, BVG/LPP non-wage cost, and Verrechnungssteuer mechanics. How to write outreach that lands in the first email to a Swiss CFO.",
"h1": "Outreach Scripts for CFOs in Switzerland: FER, FINMA, and the BVG Belt",
"country": "Swiss",
"intro": [
"Swiss CFOs operate against a financial vocabulary and a regulatory load that a German or Austrian counterpart does not face. Swiss GAAP FER is the default reporting framework for most Swiss companies, layered above OR (Obligationenrecht) statutory minimums; IFRS applies to listed and large entities; US GAAP appears only in the US-listed subsidiaries of Swiss multinationals. Reporting language and reporting framework often differ from the buyer's marketing language, which is part of what makes Swiss CFO outreach harder than it looks.",
"BVG/LPP (Bundesgesetz ueber die berufliche Alters-, Hinterlassenen- und Invalidenvorsorge) is the second-most consequential variable in a Swiss CFO's P&L after headcount. Mandatory employer contributions, varying by canton and age band, produce a structural non-wage cost that overseas vendors routinely underestimate by 5-10 percentage points when sizing their TCO. A vendor that maps their pricing into this BVG belt gets engagement.",
"Two tax instruments shape every Swiss CFO conversation: Verrechnungssteuer (35% withholding tax on dividends, interest, royalties) and Stempelsteuer (stamp duty on securities transactions). They also shape vendor structuring: cross-border contracts into Switzerland are routinely advised against if they trigger Stempelsteuer or recharacterize Verrechnungssteuer risk. Vendors that have thought through their Swiss structure close faster.",
"What does not move Swiss CFOs is German-flavored framing. Swiss CFOs read Swiss references first, then DACH, then global. Sequences that lead with a German reference customer look like a German vendor trying to extend."
],
"h2_1": "Key Differences When Targeting Swiss CFOs",
"bullets_1": [
"Swiss GAAP FER vs IFRS vs OR. Most Swiss KMU report under FER, not IFRS or German HGB. Your TCO model in Swiss CFO language must respect FER conventions (provisions, impairments, revenue recognition under FER). Vendors that produce only IFRS-segmented reporting get filtered out as off-shelf.",
"BVG/LPP and the non-wage cost belt. Mandatory BVG employer contributions vary by canton and by insured age band. CFOs expect vendors to factor this into TCO at quote time. Skip it and your proposal reads as a German template.",
"Verrechnungssteuer and Stempelsteuer mechanics. Cross-border contracts that trigger withholding or stamp-duty exposure are rejected by Swiss tax-aware CFOs. A vendor with a documented Swiss billing entity and contract path lands faster.",
"AHV/AVS and pension on payroll. AHV (Alters- und Hinterlassenenversicherung) is universal. CFOs are cautious about vendors whose platforms cannot reconcile AHV/AVS deductions correctly across multiple cantons and across international assignees.",
"FINMA-aware reporting when finance-adjacent. Swiss CFOs at banks, asset managers, and insurance companies (FINMA-supervised) carry different reporting standards. Your outreach that acknowledges this distinction, vs treating Swiss finance as a single market, lands."
],
"h2_2": "What Gets a Reply from Swiss CFOs",
"bullets_2": [
"A reference to a specific Swiss annual report or Statuten. Swiss CFOs are personally involved in producing the annual report (Geschaeftsbericht) and respond to outreach that cites a specific line item or footnote.",
"FER-aligned TCO math. A two-page business case with FER-consistent terminology gets forwarded. IFRS-only business cases get filtered.",
"Swiss or DACH references cannot substitute for Swiss ones. Swiss CFOs read Swiss references first. A Swiss KMU or Swiss multinational reference closes; an Austrian or German reference does not, even with similar revenue band.",
"Documented Swiss billing entity and contract path. A vendor with a Swiss AG/GmbH or a Swiss invoicing partner shows they have solved the cross-border tax problem. Vendors without one read as naive.",
"Confidentiality and data residency assurance. Swiss CFOs default to assuming cross-border data transfer scrutiny is real. A vendor that documents data residency (Swiss or EU only, with concrete data center naming) reads as serious."
],
"related": [
["outreach-scripts-hr-director-switzerland","Swiss HR Director outreach"],
["outreach-scripts-it-director-switzerland","Swiss IT Director outreach"],
["outreach-scripts-procurement-switzerland","Swiss Procurement outreach"],
["outreach-scripts-vp-sales-switzerland","Swiss VP Sales outreach"]
]
},
{
"slug": "outreach-scripts-hr-director-switzerland",
"title": "Outreach Scripts for Swiss HR Directors | ZeroHype",
"description": "Swiss HR directors operate under OR Mitbestimmung (much weaker than Betriebsrat), GAV per industry, BVG/LPP mandatory pension, and RAV/Bildungspiraten subsidies. Cultural framing for Swiss HR outreach.",
"h1": "Outreach Scripts for HR Directors in Switzerland: BVG, GAV, and OR Mitbestimmung",
"country": "Swiss",
"intro": [
"Swiss HR is structurally different from Austrian and German HR in three ways that matter to an outside vendor. First, the Mitbestimmung (worker participation) framework is much weaker than the Austrian Betriebsrat or the German Betriebsrat; most Swiss HR directors do not run a works council consultation cycle on tooling decisions. Second, GAV (Gesamtarbeitsvertrag) collective agreements are mandatory in some sectors and vary by canton; the Swissmem template GAV is the canonical reference for MEM industries. Third, BVG/LPP (occupational pension) is a structural cost and a structural reporting obligation that HR directors cannot ignore.",
"Swiss HR is also much more export-oriented than Austrian HR. Companies in MEM, pharma, finance, and watchmaking routinely have substantial international workforces and cross-border employment relationships. HR tooling that breaks on cross-border is unusable; HR tooling that handles it is differentiated.",
"Two subsidy frames move Swiss HR conversations: flankierende Massnahmen (federal measures to support the Swiss labour market against cross-border pressure) and RAV-coordinated unemployment measures (Regime des allocations de perte d'emploi). Vendors that map their offering to either of these get engagement.",
"What does not move Swiss HR is German Betriebsrat language. Sequences built on works-council co-determination find no equivalent forum in most Swiss workplaces and sound misinformed."
],
"h2_1": "Key Differences When Targeting Swiss HR Directors",
"bullets_1": [
"OR Mitbestimmung vs Betriebsrat. Swiss HR directors operate under the Obligationenrecht (OR), not the Austrian Arbeitsverfassungsgesetz or the German Betriebsverfassungsgesetz. Work councils exist in some companies but are not legally mandated at the same threshold; participation rights are weaker. Outreach that assumes works-council co-determination flows looks misinformed.",
"GAV (Gesamtarbeitsvertrag) per industry and canton. GAV templates, including the Swissmem-verhandelte GAV for MEM industries, bind salary scales, working hours, and benefits. Swiss HR directors cannot set compensation outside GAV in covered companies. Sequence copy must respect that.",
"BVG/LPP non-wage cost. BVG/LPP mandatory employer contributions are a structural P&L line item that HR directors must track at quote time. Vendors that ignore this are flagged at TCO stage.",
"AHV/AVS and cross-border employment. AHV contributions apply to Swiss-based employment regardless of nationality; international assignees need coordination with their home-country social security. Swiss HR directors value tooling that handles multi-jurisdiction social-security reconciliation.",
"Familiarisierungsprogramm and Bildungspiraten. Some industries and cantons run government-subsidized upskilling programs. Vendors that map to specific canton subsidies land faster than vendors with generic learning platform pitches."
],
"h2_2": "What Gets a Reply from Swiss HR Directors",
"bullets_2": [
"A reference to a specific GAV or to a specific Swissmem framework. HR directors are impressed by outreach that cites the canonical reference relevant to their industry.",
"Cross-border employment handling demonstrated. A short demo that shows accurate AHV/AVS handling for cross-border workers, plus BVG-grade pension contribution tracking, gets forwarded.",
"flankierende Massnahmen framing where applicable. Tools that map to specific federal subsidy frames close faster.",
"OR-aligned policies in the policy library. Pre-built templates compliant with Swiss OR (over the German Betriebsrat-style model) read as ready-to-deploy and pass legal review faster.",
"A Swiss reference customer in the same sector. Swiss HR directors trust Swiss references above German references above global references. A Swiss pharma reference beats a DAX reference."
],
"related": [
["outreach-scripts-cfo-switzerland","Swiss CFO outreach"],
["outreach-scripts-it-director-switzerland","Swiss IT Director outreach"],
["outreach-scripts-procurement-switzerland","Swiss Procurement outreach"],
["outreach-scripts-vp-sales-switzerland","Swiss VP Sales outreach"]
]
},
{
"slug": "outreach-scripts-it-director-switzerland",
"title": "Outreach Scripts for Swiss IT Directors | ZeroHype",
"description": "Swiss IT directors operate with FINMA-RS 2008/6 (outsourcing) and 2023/1 (cloud), Swiss Banking Act, and quadrilingual stakeholder reality. How a vendor lands outreach in Swiss IT.",
"h1": "Outreach Scripts for IT Directors in Switzerland: FINMA-RS, Banking Act, and Quadrilingual IT",
"country": "Swiss",
"intro": [
"Swiss IT directors operate under a regulatory stack layered on top of GDPR that their German and Austrian counterparts do not face. FINMA-RS 2008/6 (Outsourcing, Banks) and FINMA-RS 2023/1 (Operational Risks and Resilience, Cloud) apply directly to Swiss banks, asset managers, and insurers. The Swiss Banking Act (Bankengesetz, BankG) reinforces data localization for client-identifying data. Swissmedic applies analogously to pharma. Vendors that ignore this stack lose; vendors that name it win.",
"Swiss IT also operates in a quadrilingual environment. The same Swiss IT director may need to support German, French, Italian, and English-speaking business units, sometimes within a single product line. UI commitments to multiple languages, support commitments across time zones, and documentation across Swiss languages are table stakes that no German or Austrian vendor has to face.",
"Data sovereignty is structurally more important in Switzerland than in Germany. Swiss-US data transfer remains under close scrutiny, the EU-US Data Privacy Framework successor has not yet been adjudicated, and Swiss-hosted or EU-hosted-only options are a default rather than a differentiator. Swiss IT directors reject any vendor whose architecture relies on US-only data paths.",
"What does not move Swiss IT is hype. Swiss IT is conservative, evidence-driven, and dismissive of 'AI-powered', 'revolutionary', '10x faster' without Swiss reference data."
],
"h2_1": "Key Differences When Targeting Swiss IT Directors",
"bullets_1": [
"FINMA-RS 2008/6 and 2023/1 awareness. Swiss IT directors in financial services carry direct FINMA-RS obligations on outsourcing and cloud. Anything below these FINMA-RS in the stack reads as not-ready.",
"BankG and data localization for banking data. Client-identifying data must remain under Swiss or equivalent jurisdiction where applicable. Vendors that architect for US-only residency are disqualified at the architecture review, not the negotiation.",
"Quadrilingual UI and support. Swiss IT directors expect German-first UI with French and Italian variants; English as fallback. Support in German and French is the entry bar; Italian where relevant.",
"Swissmedic for pharma IT. Pharma IT directors in Switzerland carry Swissmedic-adjacent validation (GAMP 5-equivalent) plus country-specific GxP and Annex 11 expectations. Vendors familiar with this validate faster.",
"Cloud-trust successor uncertainty. The Swiss-US data transfer framework remains legally unsettled. Swiss IT directors favor EU-resident or Swiss-resident hosting. Vendors that cannot commit to one of these lose by default."
],
"h2_2": "What Gets a Reply from Swiss IT Directors",
"bullets_2": [
"A reference to a named Swiss customer in the same regulatory category. Swiss IT directors reject generic global logos in FINMA-regulated conversations. A Swiss bank in the same asset class closes.",
"Explicit FINMA-RS or BankG mapping. A one-page note on which clauses are addressed (without disclosing customer names) gets forwarded inside Swiss IT.",
"Swiss or EU data residency documented in writing. Swiss IT directors want concrete data center naming (e.g., Zurich, Geneva, Lupfig, Glarus); nothing less than that passes review.",
"Quadrilingual support tier documented. DE plus FR plus EN plus IT (where relevant) at specific SLAs. This document gets filed directly into vendor evaluation.",
"Reference customer in same sector with same residency. A Swiss pharma IT reference closes where a Swiss bank reference would not. Sector specificity matters."
],
"related": [
["outreach-scripts-cfo-switzerland","Swiss CFO outreach"],
["outreach-scripts-hr-director-switzerland","Swiss HR Director outreach"],
["outreach-scripts-procurement-switzerland","Swiss Procurement outreach"],
["outreach-scripts-vp-sales-switzerland","Swiss VP Sales outreach"]
]
},
{
"slug": "outreach-scripts-procurement-switzerland",
"title": "Outreach Scripts for Swiss Procurement Leads | ZeroHype",
"description": "Swiss procurement runs on BoB/IVoB thresholds, Swissmem-Vertragsmuster, VSo conflict-minerals due diligence, and canton-by-canton cantonal variation. Vendor entry points into Swiss Einkauf.",
"h1": "Outreach Scripts for Procurement Leads in Switzerland: BoB, VSo, and Swissmem-Vertragsmuster",
"country": "Swiss",
"intro": [
"Swiss procurement runs against three regulatory frameworks at once: BoB (Bundesgesetz ueber das oeffentliche Beschaffungswesen) and IVoB (Interkantonale Vereinbarung ueber das oeffentliche Beschaffungswesen) for public tenders; VSo (Verordnung zu Sorgfaltspflichten und Transparenz bezueglich mineralischer Rohstoffe aus Konfliktgebieten und Kinderarbeit) for supply-chain due diligence; Swissmem (Schweizerischer Verband der MEM-Industrie) standard contracts for MEM industries. Private procurement, especially at Swiss multinationals, layers internal supplier code of conduct on top of these. Knowing which frame applies changes the entry angle.",
"Swiss procurement also reflects a canton-by-canton variation that other DACH markets lack. Procurement approaches in Zuerich, Bern, or Basel differ from those in Zermatt-area Valais or inner Appenzell; cantonal authorities operate under different IVoB implementations. A vendor that reads this and tailors its regional engagement has a structural advantage.",
"VSo due diligence on conflict minerals and child labour is a topic that drives procurement decisions in 2026. The ordinance applies to companies that import or process tin, tantalum, tungsten, gold, or certain listed goods. Procurement is the function responsible for collecting supplier attestations; vendors that build VSo-aligned audit flows into their products land faster.",
"What does not move Swiss procurement is German-positioned framing. Swiss procurement leans on Swissmem-Vertragsmuster or its own variants; German Allgemeine Geschaeftsbedingungen are read as foreign and are red-lined by Swiss legal teams."
],
"h2_1": "Key Differences When Targeting Swiss Procurement Leads",
"bullets_1": [
"BoB/IVoB thresholds and cantonal implementation. Swiss public procurement thresholds differ from EU and US thresholds; cantonal implementations of IVoB vary. Vendors targeting Swiss public bodies must understand both the federal threshold and the cantonal procedure where the tender originates.",
"Swissmem-Vertragsmuster and MEM standard contracts. For MEM industries, the Swissmem template contracts (Kaufvertrag, Werkvertrag, Wartungsvertrag) are industry defaults. Vendors that bring their own Allg. Geschaeftsbedingungen get red-lined; vendors that present Swissmem-aligned terms win faster.",
"VSo due diligence on conflict minerals and child labour. Procurement teams now collect supplier attestations for VSo. Vendors that automate or supply these attestations close faster than vendors that ignore the topic.",
"Private supplier code of conduct at Swiss multinationals. Roche, Novartis, ABB, and other Swiss multinationals maintain private supplier codes with ESG and labour conditions. Vendors that pre-certify against these land shorter procurement cycles.",
"Logistics and border dynamics. Swiss procurement integrates cross-border Italy, France, Germany, and Austria logistics. Vendors that document their EU/EFTA logistics flows close faster."
],
"h2_2": "What Gets a Reply from Swiss Procurement Leads",
"bullets_2": [
"A reference to a Swissmem-Vertragsmuster or to a BoB/IVoB tender number. Procurement leads are impressed by outreach that cites a specific tender or template.",
"VSo-ready supplier attestation flow. A pre-built template for VSo-aligned supplier certification, ready to drop into the procurement system, gets forwarded.",
"Swissmem-aligned general terms and conditions. Submitting Swissmem-aligned terms closes; submitting German Allg. Geschaeftsbedingungen stalls.",
"Swiss reference customer in the same industry. Swiss procurement trusts Swiss references above German references above global references. A Swiss MEM reference beats a Siemens reference.",
"Canton-aware service descriptions. A service description that names the canton (e.g., operational in Zuerich and Bern, expansion to Vaud in Q3) reads as familiar."
],
"related": [
["outreach-scripts-cfo-switzerland","Swiss CFO outreach"],
["outreach-scripts-hr-director-switzerland","Swiss HR Director outreach"],
["outreach-scripts-it-director-switzerland","Swiss IT Director outreach"],
["outreach-scripts-vp-sales-switzerland","Swiss VP Sales outreach"]
]
},
{
"slug": "outreach-scripts-vp-sales-switzerland",
"title": "Outreach Scripts for Swiss VP Sales | ZeroHype",
"description": "Swiss VP Sales face quadrilingual buyer panels, KAM-Swissmem conventions, and a relationship-first cadence that resists German-style urgency. Cultural fit for Swiss sales outreach.",
"h1": "Outreach Scripts for VP Sales in Switzerland: Quadrilingual, KAM, and Plausch-frei",
"country": "Swiss",
"intro": [
"Swiss VP Sales lives in a quadrilingual buyer panel. A single Swiss enterprise deal can require German in Zuerich, French in Genf and Lausanne, Italian in Lugano and Ticino, and English as fallback in Basel. The same VP Sales cycles between languages within a single quarter. Vendors that operate in only one language disqualify themselves at the first stakeholder outreach, not at the contract.",
"KAM (Key Account Management) in Switzerland is structurally tighter than in Germany or Austria. Account portfolios are smaller; access is more layered; cross-functional alignment is denser. Tools that map account context, multi-stakeholder access, and relationship history perform; tools that try to replace these relationships stall.",
"The cadence in Switzerland is relationship-first. Swiss VP Sales is structurally allergic to the Germany-and-Austria 'first call this week' cadence. The Plausch, conversational, unhurried, often informal, is the typical way to first engage. Cadences that rush to a sales meeting before the Plausch stage are filtered.",
"What does not move Swiss VP Sales is German-style urgency. Countdown timers, scarcity messaging, and aggressive multi-channel cadences lose. Patience, specificity, and a Swiss reference win."
],
"h2_1": "Key Differences When Targeting Swiss VP Sales",
"bullets_1": [
"Quadrilingual stakeholder reality. Swiss VP Sales manages accounts across DE, FR, IT, and EN. Outreach that lands in one language only is sent up the chain unread. Tools and outreach that match stakeholder language close.",
"KAM portfolio density. Swiss VP Sales typically manages fewer but denser accounts than a German VP Sales of same company size. Outreach that acknowledges '5-15 named accounts' rather than '500-1000' lands better.",
"Plausch-first cadence. The Swiss VP Sales relationship cadence prioritizes an unhurried, conversational first touch (Plausch). High-pressure cadences disqualify vendors at the first interaction.",
"Swissmem-anchored KAM conventions in MEM industries. VP Sales in Swiss MEM industries structure KAM along Swissmem conventions. Vendors that show familiarity with Swissmem close; vendors that pitch generic enterprise motions do not.",
"Reference customer weight. Swiss VP Sales reads Swiss references first, then DACH, then global. A Swiss MEM reference in the same revenue band closes; a global logo does not."
],
"h2_2": "What Gets a Reply from Swiss VP Sales",
"bullets_2": [
"A reference to one of their named accounts or key opinion leaders. Swiss VP Sales is impressed by outreach that names a specific Swiss account or industry contact; generic personalization stalls.",
"Plausch-stage framing, not urgency. Phrases like 'fuer das naechste Quartal vorzumerken' (file for next quarter) work. Pressure cues ('this week', 'only 3 spots') are filtered.",
"Swiss reference as primary evidence. A Swiss MEM reference in the same revenue band closes. A Siemens or BMW reference does not.",
"Tools that support quadrilingual KAM. Account context, multi-stakeholder mapping, and language-aware deal history score above AI-driven outbound automation in this market.",
"Personal contact from a known sender. Swiss VP Sales responds to a personal email with a known sender name; cold sequences from managed accounts do not perform in this market."
],
"related": [
["outreach-scripts-cfo-switzerland","Swiss CFO outreach"],
["outreach-scripts-hr-director-switzerland","Swiss HR Director outreach"],
["outreach-scripts-it-director-switzerland","Swiss IT Director outreach"],
["outreach-scripts-procurement-switzerland","Swiss Procurement outreach"]
]
}
]

if __name__ == "__main__":
    out_dir = os.environ.get("OUT_DIR", "/tmp/outreach_pages")
    os.makedirs(out_dir, exist_ok=True)
    for p in PAGES:
        html = render(p)
        path = os.path.join(out_dir, f"{p['slug']}.html")
        with open(path, "w") as f:
            f.write(html)
        print(f"{p['slug']}: {len(html)} bytes")
    print(f"\n{len(PAGES)} pages -> {out_dir}")
