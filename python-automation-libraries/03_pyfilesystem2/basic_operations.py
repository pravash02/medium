"""
03_pyfilesystem2/basic_operations.py
---------------------------------------
Core PyFilesystem2 operations: read, write, list, walk, copy, move.
Uses the local OS filesystem (osfs://) — no extra backends required.
"""

import os
from fs import open_fs
from fs.copy import copy_fs, copy_file
from fs.walk import Walker


#  Setup: create a temp working directory 

WORK_DIR = "./fs_demo_workspace"
os.makedirs(WORK_DIR, exist_ok=True)


def demo_basic_operations():
    print("=" * 55)
    print("PYFILESYSTEM2 — Basic Operations")
    print("=" * 55)

    with open_fs(f"osfs://{WORK_DIR}", create=True) as filesystem:

        #  Write files ─
        print("\n Writing files \n")

        filesystem.makedirs("reports/2026", recreate=True)
        filesystem.makedirs("staging", recreate=True)

        filesystem.writetext("reports/2026/q1_summary.txt", "Q1 Revenue: $1.2M\nGrowth: +18%")
        filesystem.writetext("reports/2026/q2_summary.txt", "Q2 Revenue: $1.5M\nGrowth: +25%")
        filesystem.writetext("staging/pending_upload.csv",  "id,name,value\n1,Widget,9.99\n2,Gadget,19.99")

        print("  ✓ Created reports/2026/q1_summary.txt")
        print("  ✓ Created reports/2026/q2_summary.txt")
        print("  ✓ Created staging/pending_upload.csv")

        #  Read files 
        print("\n Reading files \n")

        content = filesystem.readtext("reports/2026/q1_summary.txt")
        print(f"  q1_summary.txt:\n    {content.replace(chr(10), chr(10) + '    ')}")

        #  List directory 
        print("\n Directory listing \n")

        for item in filesystem.listdir("reports/2026"):
            info = filesystem.getinfo(f"reports/2026/{item}", namespaces=["details"])
            size = info.size or 0
            print(f"  {item:35s} {size:>6} bytes")

        #  Walk entire tree 
        print("\n Walking full tree \n")

        for path in filesystem.walk.files():
            print(f"  {path}")

        #  File existence check 
        print("\n Existence checks \n")
        print(f"  reports/2026/ exists? {filesystem.isdir('reports/2026')}")
        print(f"  reports/2025/ exists? {filesystem.isdir('reports/2025')}")
        print(f"  q1_summary.txt exists? {filesystem.isfile('reports/2026/q1_summary.txt')}")

        #  Copy and Move ─
        print("\n Copy and move \n")

        filesystem.copy("staging/pending_upload.csv", "reports/2026/upload.csv")
        print("  ✓ Copied staging/pending_upload.csv → reports/2026/upload.csv")

        filesystem.move("staging/pending_upload.csv", "staging/processed_upload.csv")
        print("  ✓ Moved to staging/processed_upload.csv")

    print(f"\n Workspace at: {os.path.abspath(WORK_DIR)}")


#  Cleanup helper 

def cleanup():
    import shutil
    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
        print(f"\n Cleaned up {WORK_DIR}")


if __name__ == "__main__":
    demo_basic_operations()
    cleanup()
