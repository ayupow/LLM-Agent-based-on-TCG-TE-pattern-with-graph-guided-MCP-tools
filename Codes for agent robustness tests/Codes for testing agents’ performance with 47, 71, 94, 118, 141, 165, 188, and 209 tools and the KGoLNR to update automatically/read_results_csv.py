# -*- coding: utf-8 -*-
"""Read RMS simulation results CSV."""
import json, os
from _helpers_pf import _default_cfg_path

def read_results_csv(csv_path: str = "", max_rows: int = 2000, as_path: bool = False,
                     max_bytes: int = 900_000) -> str:
    """Read RMS simulation results CSV. Auto-discovers latest file if no path given.
    Input: csv_path (str, optional) -- specific CSV path. Auto-discovers latest *_RMS.csv.
           max_rows (int=2000) -- max data rows. as_path (bool=False) -- return path only.
           max_bytes (int=900000) -- truncation limit in bytes.
    Output: CSV text with metadata footer."""
    if csv_path:
        target = csv_path
    else:
        with open(_default_cfg_path(), "r", encoding="utf-8") as fh:
            cfg_data = json.load(fh)
        base_dir = cfg_data.get("output_dir", "")
        candidates = []
        for root, _, files in os.walk(base_dir):
            for fname in files:
                if fname.endswith("_RMS.csv"):
                    candidates.append((os.path.getmtime(os.path.join(root, fname)),
                                       os.path.join(root, fname)))
        if not candidates:
            return json.dumps({"error": f"No *_RMS.csv files under {base_dir}"})
        candidates.sort(reverse=True)
        target = candidates[0][1]
    if not os.path.exists(target):
        return json.dumps({"error": f"File not found: {target}"})
    if as_path:
        return json.dumps({"file_path": target})
    with open(target, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    # Find header line (first line with ; or ,)
    header_idx = 0
    for i, line in enumerate(lines):
        if ";" in line or "," in line:
            header_idx = i; break
    header_line = lines[header_idx] if lines else ""
    data_lines = lines[header_idx + 1:]
    total_rows = len(data_lines)
    data_lines = data_lines[:max_rows]
    rows_returned = len(data_lines)
    truncated = total_rows > rows_returned
    csv_text = header_line + "".join(data_lines)
    meta = (f"\n# file: {target}\n# total_data_rows: {total_rows}\n"
            f"# rows_returned: {rows_returned}\n# truncated: {truncated}\n")
    return csv_text + meta
