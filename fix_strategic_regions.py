
import os
import re
import shutil
import sys
from pathlib import Path


STRAT_DIR   = Path(r"C:\Users\dev-cop\Documents\Paradox Interactive\Hearts of Iron IV\mod\ZHM-Local-DEV\map\strategicregions")
LOCALE_FILE = Path(r"C:\Users\dev-cop\Documents\Paradox Interactive\Hearts of Iron IV\mod\ZHM-Local-DEV\localisation\english\strategic_region_names_l_english.yml")

REMOVE_IDS  = {15, 189, 253}   



def backup(path: Path):
    """Copy directory or file next to itself with a .bak suffix."""
    dest = Path(str(path) + ".bak")
    if dest.exists():
        print(f"  [SKIP] Backup already exists: {dest}")
        return
    if path.is_dir():
        shutil.copytree(path, dest)
    else:
        shutil.copy2(path, dest)
    print(f"  [OK]   Backed up → {dest}")


def parse_id_from_filename(fname: str):
    """
    Extract the leading integer from filenames like:
        15-Asia.txt  →  15
        189-Burma.txt → 189
        NAMIBIA-Something.txt → None  (non-numeric, handled separately)
    """
    m = re.match(r'^(\d+)', fname)
    return int(m.group(1)) if m else None


def extract_name_part(fname: str) -> str:
    """'15-Asia.txt' → 'Asia'   '189-Burma.txt' → 'Burma'"""
    # strip leading digits and dash
    no_ext = Path(fname).stem          # e.g. '15-Asia'
    parts = no_ext.split('-', 1)
    return parts[1] if len(parts) == 2 else no_ext


def main():
    
    if not STRAT_DIR.is_dir():
        sys.exit(f"ERROR: strategicregions directory not found:\n  {STRAT_DIR}")
    if not LOCALE_FILE.is_file():
        sys.exit(f"ERROR: localisation file not found:\n  {LOCALE_FILE}")


    print("\n=== STEP 1: Backing up files ===")
    backup(STRAT_DIR)
    backup(LOCALE_FILE)


    print("\n=== STEP 2: Reading strategic region files ===")
    all_files = sorted(STRAT_DIR.glob("*.txt"))

    numeric   = []   # (old_id, path)  – files with a leading integer
    non_numeric = [] # paths that have no numeric prefix (e.g. NAMIBIA)

    for f in all_files:
        oid = parse_id_from_filename(f.name)
        if oid is not None:
            numeric.append((oid, f))
        else:
            non_numeric.append(f)
            print(f"  [INFO] Non-numeric file (will not be renumbered): {f.name}")

    
    numeric.sort(key=lambda x: x[0])
    print(f"  Found {len(numeric)} numeric region files, {len(non_numeric)} non-numeric.")

    
    print(f"\n=== STEP 3: Building renumber map (removing IDs {sorted(REMOVE_IDS)}) ===")
    old_to_new = {}
    new_id = 1
    for old_id, fpath in numeric:
        if old_id in REMOVE_IDS:
            print(f"  [DELETE] {fpath.name}  (old id {old_id})")
        else:
            old_to_new[old_id] = new_id
            new_id += 1

    print(f"  Total regions after removal: {new_id - 1}")

    #Read localisation BEFORE touching files
    print("\n=== STEP 4: Reading localisation file ===")
    locale_raw = LOCALE_FILE.read_text(encoding="utf-8-sig")  # handles BOM

    # Parse existing locale entries into a dict  { "STRATEGICREGION_15": "Name", ... }
    locale_map: dict[str, str] = {}
    for line in locale_raw.splitlines():
        m = re.match(r'^\s*(STRATEGICREGION_\w+)\s*:\s*(?:\d+\s*)?"([^"]*)"', line)
        if m:
            locale_map[m.group(1)] = m.group(2)

    print(f"  Parsed {len(locale_map)} localisation entries.")

    print("\n=== STEP 5: Deleting empty region files ===")
    for old_id, fpath in numeric:
        if old_id in REMOVE_IDS:
            fpath.unlink()
            print(f"  [DELETED] {fpath.name}")

    print("\n=== STEP 6: Renaming and patching files ===")

    # We must rename carefully to avoid collisions (e.g. 16→15 could clash with
    # an existing 15 if it weren't deleted). Use a two-pass approach:
    # Pass A: rename everything to a temp name.
    # Pass B: rename from temp to final name.

    remaining = [(old_id, fpath) for old_id, fpath in numeric if old_id not in REMOVE_IDS]

    # Pass A – rename to .tmp files
    temp_files = []
    for old_id, fpath in remaining:
        tmp = fpath.with_suffix(".tmp")
        fpath.rename(tmp)
        temp_files.append((old_id, tmp))

    # Pass B – rename to new names + patch interior id
    for old_id, tmp_path in temp_files:
        new_id_val = old_to_new[old_id]
        name_part  = extract_name_part(tmp_path.stem)   # stem is still old name minus .tmp
        # tmp_path.stem looks like "15-Asia" (the original stem before .tmp was added)
        new_fname  = f"{new_id_val}-{name_part}.txt"
        new_path   = STRAT_DIR / new_fname

        # Read content
        content = tmp_path.read_text(encoding="utf-8")

        # Patch  `strategic_region_id = <old>` → `strategic_region_id = <new>`
        patched, n = re.subn(
            r'(strategic_region_id\s*=\s*)' + str(old_id) + r'\b',
            r'\g<1>' + str(new_id_val),
            content
        )
        if n == 0:
            # Some files use just the bare id at the top – try broader match
            patched, n = re.subn(
                r'\b' + str(old_id) + r'\b',
                str(new_id_val),
                content,
                count=1   # only the very first occurrence (the id line)
            )

        new_path.write_text(patched, encoding="utf-8")
        tmp_path.unlink()

        if old_id != new_id_val:
            print(f"  [RENAMED] {old_id:>4} → {new_id_val:>4}   ({name_part})")

    
    print("\n=== STEP 7: Rebuilding localisation file ===")

    # Build new locale map from old
    new_locale_map: dict[str, str] = {}

    for old_id, _ in numeric:
        if old_id in REMOVE_IDS:
            continue
        new_id_val = old_to_new[old_id]
        old_key = f"STRATEGICREGION_{old_id}"
        new_key = f"STRATEGICREGION_{new_id_val}"
        name = locale_map.get(old_key, f"Strategic Region {new_id_val}")
        new_locale_map[new_key] = name

    # Keep non-numeric locale entries (e.g. STRATEGICREGION_NAMIBIA)
    for key, val in locale_map.items():
        if not re.match(r'^STRATEGICREGION_\d+$', key):
            new_locale_map[key] = val

    # Write out
    lines = ["l_english:"]
    # Numeric entries first, sorted by integer value
    numeric_keys = sorted(
        [k for k in new_locale_map if re.match(r'^STRATEGICREGION_\d+$', k)],
        key=lambda k: int(k.split('_')[-1])
    )
    for k in numeric_keys:
        lines.append(f' {k}: "{new_locale_map[k]}"')
    # Then non-numeric
    for k in sorted(new_locale_map):
        if not re.match(r'^STRATEGICREGION_\d+$', k):
            lines.append(f' {k}: "{new_locale_map[k]}"')

    LOCALE_FILE.write_text('\n'.join(lines) + '\n', encoding="utf-8-sig")
    print(f"  [OK] Wrote {len(new_locale_map)} entries to localisation file.")

   
    print("\n=== DONE ===")
    print(f"  Deleted  : {sorted(REMOVE_IDS)}")
    print(f"  Remaining: {len(old_to_new)} regions (now numbered 1–{max(old_to_new.values())})")
    print(f"  Backups  : {STRAT_DIR}.bak  and  {LOCALE_FILE}.bak")
    print("\nYou can now launch the game. If anything looks wrong, restore from the .bak copies.")


if __name__ == "__main__":
    main()
