# Quick Reference: What Changed & How to Use It

## 🎯 The Two Fixes at a Glance

### Fix #1: Autocomplete Dropdown No Longer Hidden
**What was broken:**  
Autocomplete suggestions disappeared behind result cards

**What changed:**  
CSS z-index increased (110 → 1000)

**How it works:**  
Type in search → Dropdown stays visible even with results below → Click suggestion

---

### Fix #2: No More Duplicates + New Filter System  
**What was broken:**  
- Same genome appeared multiple times in results
- Single toggle was confusing ("on/off" unclear)

**What changed:**  
- Replaced toggle with TWO buttons: "Reference Genomes" vs "All Sequences"
- Added color-coded badges (Cyan = Reference, Purple = Sequenced)

**How it works:**  
See the next section!

---

## 🎮 How to Use the New Dual Filter

### Scenario 1: "Show me ONLY the official reference genome"

1. Search "Homo sapiens"
2. Click button: **📋 Reference Genomes** (should be highlighted in cyan)
3. Result: **1 genome** - GRCh38.p14 (the gold-standard human reference)
4. Cards show: Cyan 📋 badge + cyan left border

```
┌─────────────────────────────────────┐
│ Homo sapiens [human]                │
│ 📋 Reference ← cyan badge           │
│ Accession: GCF_000001405.40         │
│ Size: 3.10 Gb                       │
│ 🧬 Download | 🔬 Details            │
│ ← cyan left border                  │
└─────────────────────────────────────┘
```

---

### Scenario 2: "Show me ALL sequenced versions for comparison"

1. Search "Homo sapiens"  
2. Click button: **🔬 All Sequences** (should be highlighted in cyan)
3. Result: **Multiple genomes** including:
   - Reference (GRCh38.p14)
   - Alternative assemblies (GRCh38_alternative)
   - Cancer cell line genomes
4. Cards show mixed badges: Cyan (references) + Purple (sequenced)

```
┌──────────────────────────────┐  ┌──────────────────────────────┐
│ Homo sapiens                 │  │ Homo sapiens [Cancer Line]   │
│ 📋 Reference                 │  │ 🔬 Sequenced ← purple badge  │
│ GCF_000001405.40             │  │ GCA_000001405.29             │
│ Size: 3.10 Gb                │  │ Size: 3.11 Gb                │
│ ← cyan border                │  │ ← purple border              │
└──────────────────────────────┘  └──────────────────────────────┘
```

---

### Scenario 3: Malaria Research - Drug Resistance Study

1. Search "Plasmodium falciparum"
2. Toggle **Reference Genomes** → Result: 1 genome (3D7 reference)
   - Use for: Mapping drug resistance genes to reference coordinates
3. Toggle **All Sequences** → Result: 70+ genomes
   - Dd2 (chloroquine-resistant)
   - W2 (drug-resistant)
   - Clinical isolates from Africa, Asia, Americas
   - Use for: Compare mutations across strains with different resistances

```
Reference Mode:
┌──────────────────────────────────┐
│ Plasmodium falciparum 3D7        │
│ 📋 Reference                     │
│ (Use for coordinate mapping)     │
└──────────────────────────────────┘

All Sequences Mode:
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│ P. falciparum 3D7    │ │ P. falciparum Dd2    │ │ P. falciparum W2     │
│ 📋 Reference         │ │ 🔬 Sequenced         │ │ 🔬 Sequenced         │
│ (Ref genome)         │ │ (Drug-resistant)     │ │ (Drug-resistant)     │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
... 67 more sequenced isolates ...
```

---

## 🎨 Visual Guide: Badge & Border Colors

### Reference Genomes
- **Badge Color**: Cyan 📋
- **Left Border**: Cyan (#06b6d4)
- **Meaning**: Gold-standard, NCBI-curated assembly
- **Database**: RefSeq only

### Sequenced Variants
- **Badge Color**: Purple 🔬
- **Left Border**: Purple (#a855f7)
- **Meaning**: Research-quality, community-submitted assembly
- **Database**: GenBank, clinical isolates, alternative assemblies

---

## ⚡ Quick Tips

### Tip 1: Reactive Filtering
You don't need to re-type the query!
1. Search "Arabidopsis thaliana"
2. Click **Reference Genomes** 
3. See results
4. Click **All Sequences**
5. Results update INSTANTLY without re-typing

### Tip 2: Deduplication
Each genome accession appears **exactly once**, even if it exists in multiple databases.

### Tip 3: Autocomplete Still Works
Ambiguous terms resolve to scientific names:
- Type "hepatitis" → see "Hepatitis B virus" suggestion → click it
- Type "coronavirus" → see "Severe acute respiratory syndrome coronavirus 2" suggestion

### Tip 4: Mobile Responsive
Buttons stack vertically on small screens - still fully functional

---

## 🔍 Detailed View: Filter Button States

### Button: Reference Genomes
```
Inactive (gray):
  [📋 Reference Genomes]
  
Active (cyan with glow):
  [📋 Reference Genomes] ← highlighted, glowing
```

### Button: All Sequences
```
Inactive (gray):
  [🔬 All Sequences]
  
Active (cyan with glow):
  [🔬 All Sequences] ← highlighted, glowing
```

Only ONE button is active at a time. Click to toggle.

---

## 🐛 Testing: How to Verify the Fixes Work

### Test 1: Autocomplete Not Hidden
1. Open http://localhost:3000
2. Type "hepatitis" slowly
3. See dropdown with suggestions
4. **Verify**: Dropdown stays visible even if you scroll or if results cards appear
5. Click a suggestion → search runs

### Test 2: No Duplicates  
1. Search "Homo sapiens"
2. Click "All Sequences"
3. Count the cards
4. **Verify**: Each accession (like GCF_000001405.40) appears only ONCE
5. No card appears twice

### Test 3: Filters Work
1. Search "Plasmodium falciparum"
2. With **Reference Genomes** → 1 card (3D7)
3. With **All Sequences** → 70+ cards (with Dd2, W2, isolates, etc.)
4. **Verify**: Switching buttons updates results instantly

### Test 4: Badge Colors
1. Search any organism
2. In **All Sequences** mode
3. **Verify**: 
   - Cyan 📋 badges = Reference genomes
   - Purple 🔬 badges = Sequenced variants
   - Card left borders match badge colors

---

## 📋 Comparison Table

| Feature | Before | After |
|---------|--------|-------|
| **Autocomplete Visibility** | Hidden behind results | Always visible (z-index: 1000) |
| **Filter Type** | Single checkbox | Two explicit buttons |
| **Filter Clarity** | Unclear (on/off) | Clear (Reference vs All) |
| **Duplicate Results** | Yes, same accession twice | No, deduplicated |
| **Visual Source Distinction** | None | Color-coded badges + borders |
| **Reactivity** | Re-type to change filter | Click button, auto-search |
| **Responsive Design** | Yes | Yes (improved) |

---

## 🚀 Ready to Use!

The app is fully updated. Just:
1. Refresh your browser at http://localhost:3000
2. Start searching
3. Use the new dual filters to find exactly what you need!

---

