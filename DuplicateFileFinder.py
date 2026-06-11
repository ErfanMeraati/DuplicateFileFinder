import os
import hashlib
import sys
from collections import defaultdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_file_hash(filepath, chunk_size=8192):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, OSError):
        return None

def scan_directory(directory):
    """Recursively collect all file paths."""
    file_paths = []
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def find_duplicates(directory):
    """Find duplicate files using SHA256 hashing."""
    print(f"\n📂 Scanning: {directory}")
    print("   Collecting files...", end='\r')

    all_files = scan_directory(directory)
    total = len(all_files)
    print(f"   Found {total} files. Hashing...        ")

    size_groups = defaultdict(list)
    for fp in all_files:
        try:
            size = os.path.getsize(fp)
            if size > 0:  
                size_groups[size].append(fp)
        except OSError:
            continue


    candidates = [fp for group in size_groups.values() if len(group) > 1 for fp in group]
    print(f"   {len(candidates)} candidate files to hash (same size groups)...")

    hash_map = defaultdict(list)
    done = 0

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {executor.submit(get_file_hash, fp): fp for fp in candidates}
        for future in as_completed(future_to_file):
            fp = future_to_file[future]
            file_hash = future.result()
            if file_hash:
                hash_map[file_hash].append(fp)
            done += 1
            print(f"   Hashing: {done}/{len(candidates)}", end='\r')

    print()
    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
    return duplicates

def format_size(size_bytes):
    """Human-readable file size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def display_results(duplicates):
    """Display duplicate groups."""
    if not duplicates:
        print("\n✅ No duplicates found!")
        return

    total_groups = len(duplicates)
    total_wasted = 0

    print(f"\n{'='*60}")
    print(f"  🔍 Found {total_groups} duplicate group(s)")
    print(f"{'='*60}")

    for i, (file_hash, paths) in enumerate(duplicates.items(), 1):
        file_size = os.path.getsize(paths[0])
        wasted = file_size * (len(paths) - 1)
        total_wasted += wasted

        print(f"\n[Group {i}] — {len(paths)} copies | "
              f"Size: {format_size(file_size)} each | "
              f"Wasted: {format_size(wasted)}")
        print(f"  Hash: {file_hash[:16]}...")
        for j, path in enumerate(paths):
            marker = "  📄" if j == 0 else "  🔁"
            print(f"{marker} {path}")

    print(f"\n{'='*60}")
    print(f"  💾 Total wasted space: {format_size(total_wasted)}")
    print(f"{'='*60}")

    return total_wasted

def save_results(duplicates, directory):
    """Save results to a timestamped text file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"duplicates_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Duplicate File Finder — Results\n")
        f.write(f"Scanned: {directory}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        if not duplicates:
            f.write("No duplicates found.\n")
        else:
            total_wasted = 0
            for i, (file_hash, paths) in enumerate(duplicates.items(), 1):
                file_size = os.path.getsize(paths[0])
                wasted = file_size * (len(paths) - 1)
                total_wasted += wasted
                f.write(f"[Group {i}] {len(paths)} copies | "
                        f"Size: {format_size(file_size)} | "
                        f"Wasted: {format_size(wasted)}\n")
                f.write(f"Hash: {file_hash}\n")
                for path in paths:
                    f.write(f"  {path}\n")
                f.write("\n")
            f.write("=" * 60 + "\n")
            f.write(f"Total wasted space: {format_size(total_wasted)}\n")

    print(f"\n💾 Results saved to: {filename}")

def main():
    print("=" * 60)
    print("       🔍 Duplicate File Finder")
    print("=" * 60)


    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = input("\nEnter folder path to scan: ").strip().strip('"')

    if not os.path.isdir(directory):
        print(f"\n❌ Not a valid directory: {directory}")
        input("\nPress Enter to exit...")
        sys.exit(1)

    duplicates = find_duplicates(directory)
    display_results(duplicates)

    if duplicates:
        save = input("\nSave results to file? (y/n): ").strip().lower()
        if save == 'y':
            save_results(duplicates, directory)

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
