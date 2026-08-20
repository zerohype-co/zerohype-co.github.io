# Tartarus — Set-up Stripe (FLUX COMPLET)

> Document INTERN. NU se commit-eaza in repo-ul public (altfel fisierul devine public pe zerohypelab.com).
> Brand: ZeroHype Lab (anonim). Contact: zerohype@proton.me.
> Data: 2026-08-15.

---

## 1. Ce vindem (detaliile reale din pagina tartarus/index.html + index.md)

### Produs A — „Tartarus: Full Diagnostic Report"
| Camp | Valoare |
|---|---|
| Nume in Stripe | `Tartarus — Full Diagnostic Report` |
| Tip | one-time (nu abonament) |
| Pret | **$49.00 USD** |
| Camp de email client | colectat in Checkout (ON) |
| Descriere (pe checkout) | Written, structure-by-structure analysis: annotated code structure map, dependency graph with problem nodes, documentation gap analysis with priorities, AI-agent readiness checklist, written recommendations. |
| Ce primeste dupa plata | Raportul complet livrat pe email (clientul a dat deja email-ul in form). |
| Delivery SLA | 48-72h, ca restul diagnosticelor ZeroHype (vezi lansarea limbajului din restul site-ului). |

### Produs B — „Tartarus: Custom Integration" (from $2,500)
- **Nu e platit prin Payment Link.** E cotatie (quote) + consult; pagina foloseste `mailto:zerohype@proton.me?subject=Tartarus custom integration`.
- Recomand: NU crea Payment Link fix aici. Pastreaza fluxul „contacteaza-ne", apoi, la nevoie, facturezi manual din Stripe (Invoice / Custom amount) per client.

### Gratis
- Scan-ul heuristic / Context Readiness Score ramane GRATUIT (nu trebuie Stripe).

---

## 2. Pasii in Dashboard Stripe (contul brandului, NU personal)

1. **Mode: Test** (butonul toggle din colt): Test mode ON.
2. **Products → + Add product**:
   - Name: `Tartarus — Full Diagnostic Report`
   - Description (paseaza textul din tabelul Produs A, col. „Descriere").
   - Image: optional (logo/screenshot al paginii, fara identitate reala).
   - **Pricing model: Standard pricing / One-time → $49.00** (USD). Salveaza. Se genereaza un `Price ID` (ex. `price_1...`) — noteaza-l.
3. Din pagina produsului (sau from price): **... → Create a payment link**.
4. In setarile Payment Link, setezi:

### 2.1 After-payment action (CRITIC)
> Pagina nu are backend, deci **NU folosi webhook API** pentru livrare automata. Raspunsul corect: **redirect + livrare pe email** (procesul existent al brandului: email la client).

- **On successful payment → Redirect to a URL**
- URL: **`https://zerohypelab.com/tartarus/thanks`**
- Actualizez eu aceasta pagina (o creez ca pagina statica `tartarus/thanks`) — ea ii spune clientului: „Plata OK. Raportul ti se trimite pe email in maximum 48-72h. Contact: zerohype@proton.me".
- (Alternativa fara redirect: lași pagina implicita de succes Stripe. Dar redirectul catre un page de brand e mai curat si mai on-brand.)

### 2.2 Alte setari Payment Link
- **Collect email**: ON (Checkout o colecteaza implicit).
- **Billing address**: optional.
- **Payment methods**: lasa defaultul Stripe (cards; in functie de tara, adaugi altele optional).
- **Expire link**: optional. Nu-ti trebuie pentru un link permanent.
- **Invoice**: ON (clientul primeste chitanta pe email — util pentru B2B).

5. Copiaza **link-ul Payment Link** (`https://buy.stripe.com/...` — asa-numitul „payment link", la 4 bucati de sub-domeniu). Se pare la fel cu celelalte: `buy.stripe.com/<segmentA>/<segmentB>`. **Nu folosi altceva decat acest link in site.**

---

## 3. Test in Test mode

1. Deschide Payment Link-ul din Test mode (arata preview Checkout Stripe).
2. Plateste cu card test Stripe: `4242 4242 4242 4242`, orice CVV, any data viitoare.
3. Verifica: redirect dupa plata ajunge la `zerohypelab.com/tartarus/thanks`, email colectat corect.
4. Verifica in Stripe: Payment e in `TEST` batch, invoice emis.

---

## 4. Activa Live + pune link-ul in site

1. **Test mode OFF** → creezi (sau Activezi) Payment Link-ul **Live** (acelasi produs/price). Noteaza link-ul live `https://buy.stripe.com/...live...`.
2. Imi dai mie link-ul live. Eu inlocuiesc cele **3 referinte** de placeholder:
   - `tartarus/index.html` → href-ul „Unlock – $49" (linia ~837): `https://buy.stripe.com/placeholder_tartarus` → link live.
   - `tartarus/index.md` → 2x `buy.stripe.com/placeholder_tartarus` (sectiuni „Full report (paid)" + „Custom integration") → link live.
3. Creez pagina `tartarus/thanks` (destinatia redirectului) + o adaug in sitemap (optional).
4. Commit + push sub identitatea `Zero Hype <zerohype@proton.me>`, prin `gh auth switch --user zerohype-co`, doar la `zerohype-co/*`.
5. Verific live: plata → redirect → thanks page, si ca placeholder-ul a disparut din tot repo-ul.

---

## 5. Dupa-primii-bani (verificare rapida)

- Confirmi in Stripe ca `Payment Link`-ul e Live si are cateva plata.
- Comportamentul livrarii raportului = livrare manuala pe email (procesul ZeroHype existent, 48-72h). Daca peste 2-3 luni vrei automatizare, migram pe Stripe **Checkout Session + webhook** cu un backend cu tot (cand ai backend pentru tartarus).

---

## Snapshot: valori exacte de folosit la crearea in Stripe
- Product name (A): `Tartarus — Full Diagnostic Report`
- Price (A): **$49.00** one-time, USD
- After payment: redirect la `https://zerohypelab.com/tartarus/thanks`
- Product (B): `Tartarus — Custom Integration`, from $2,500 — QUOTE/contact, nu Payment Link
- Email contact: `zerohype@proton.me`
- Brand (public)= ZeroHype Lab (ANONIM). Nicio referinta la identitate reala in nume produs, descriere, imagini sau invoice.

## Ce NU trebuie sa uiti
- Test mode intai, Live dupa.
- Link-ul Live il dai MIE (nu il pui tu direct daca nu vrei) — il integrez + testez eu.
- Custom ($2,500) ramane pe consult + invoice manual, nu Payment Link.
