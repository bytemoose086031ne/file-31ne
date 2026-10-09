"""File deduplication utility: finds duplicate files in a directory."""
import argparse, os, hashlib
from collections import defaultdict

def file_hash(path, blocksize=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            h.update(block)
    return h.hexdigest()

def find_dupes(root):
    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                h = file_hash(path)
                hashes[h].append(path)
            except (OSError, PermissionError):
                pass
    return [paths for paths in hashes.values() if len(paths) > 1]

def main():
    parser = argparse.ArgumentParser(description="Find duplicate files")
    parser.add_argument("directory", help="Directory to scan")
    args = parser.parse_args()
    dup_groups = find_dupes(args.directory)
    if not dup_groups:
        print("No duplicates found.")
        return
    for group in dup_groups:
        print("\nDuplicate group:")
        for p in group:
            print(f"  {p}")

if __name__ == "__main__":
    main()