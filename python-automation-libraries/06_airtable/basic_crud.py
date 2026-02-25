"""
06_airtable/basic_crud.py  +  sync_workflow.py  +  content_calendar.py
-------------------------------------------------------------------------
pyairtable: CRUD operations, CRM sync, and content calendar automation.
Runs in MOCK MODE if no credentials are set — shows expected behavior.
"""

import os
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "")
MOCK_MODE        = not (AIRTABLE_API_KEY and AIRTABLE_BASE_ID)


# =======================================================
# MOCK CLIENT (for demo without real credentials)
# =======================================================

class MockTable:
    """Simulates pyairtable Table for demo purposes."""
    _store: list[dict] = []
    _id_counter: int = 1

    def __init__(self, name: str):
        self.name = name
        self._store = []
        self._id_counter = 1

    def all(self, formula: str = "") -> list[dict]:
        return [r for r in self._store if self._matches(r, formula)]

    def create(self, fields: dict) -> dict:
        record = {"id": f"rec{self._id_counter:05d}", "fields": fields}
        self._id_counter += 1
        self._store.append(record)
        return record

    def update(self, record_id: str, fields: dict) -> dict:
        for r in self._store:
            if r["id"] == record_id:
                r["fields"].update(fields)
                return r
        raise ValueError(f"Record {record_id} not found")

    def delete(self, record_id: str) -> dict:
        for i, r in enumerate(self._store):
            if r["id"] == record_id:
                return self._store.pop(i)
        raise ValueError(f"Record {record_id} not found")

    def _matches(self, record: dict, formula: str) -> bool:
        if not formula:
            return True
        # Simple field=value matching for mock
        for key, val in record["fields"].items():
            if str(val) in formula and key.lower().replace(" ", "_") in formula.lower().replace(" ", "_"):
                return True
        return not formula  # default: return all if formula not parsed


def get_table(table_name: str):
    """Returns real or mock table based on credentials."""
    if MOCK_MODE:
        print(f"  [MOCK MODE] Using simulated Airtable table: '{table_name}'")
        return MockTable(table_name)
    from pyairtable import Api
    api = Api(AIRTABLE_API_KEY)
    return api.table(AIRTABLE_BASE_ID, table_name)


# =======================================================
# PART 1: Basic CRUD
# =======================================================

def demo_basic_crud():
    print("=" * 55)
    print("PYAIRTABLE — Basic CRUD Operations")
    print("=" * 55)

    table = get_table("Tasks")

    # CREATE
    print("\n- CREATE -\n")
    tasks_to_add = [
        {"Name": "Setup CI/CD pipeline",  "Status": "In Progress", "Priority": "High",   "Assignee": "Alice"},
        {"Name": "Write API docs",         "Status": "Pending",     "Priority": "Medium", "Assignee": "Bob"},
        {"Name": "Database migration",     "Status": "Pending",     "Priority": "High",   "Assignee": "Alice"},
        {"Name": "Deploy to staging",      "Status": "Complete",    "Priority": "Low",    "Assignee": "Carlos"},
    ]
    created = []
    for task in tasks_to_add:
        record = table.create(task)
        created.append(record)
        print(f"  ✓ Created [{record['id']}]: {task['Name']}")

    # READ ALL
    print("\n- READ ALL -\n")
    all_records = table.all()
    print(f"  Total records: {len(all_records)}")
    for r in all_records:
        f = r["fields"]
        print(f"  [{r['id']}] {f.get('Name','?'):35s} {f.get('Status','?'):15s} {f.get('Priority','?')}")

    # UPDATE
    print("\n- UPDATE -\n")
    target_id = created[1]["id"]
    updated = table.update(target_id, {"Status": "In Progress", "Notes": "Started 2026-02-25"})
    print(f"  Updated {target_id}: Status → '{updated['fields']['Status']}'")

    # DELETE
    print("\n- DELETE -\n")
    del_id = created[3]["id"]
    table.delete(del_id)
    print(f"  Deleted record {del_id}")
    print(f"  Remaining records: {len(table.all())}")


# =======================================================
# PART 2: CRM Sync Workflow
# =======================================================

def demo_crm_sync():
    """
    Pattern: Pull contacts from Airtable, enrich with API data,
    push updated records back. Common in sales/ops automation.
    """
    print("\n" + "=" * 55)
    print("PYAIRTABLE — CRM Sync Workflow")
    print("=" * 55)

    table = get_table("Contacts")

    # Seed contacts
    contacts_data = [
        {"Name": "Sarah Chen",    "Email": "sarah@techcorp.com",  "Status": "Lead",     "Score": 0},
        {"Name": "Marcus Webb",   "Email": "marcus@startup.io",   "Status": "Lead",     "Score": 0},
        {"Name": "Priya Sharma",  "Email": "priya@enterprise.co", "Status": "Customer", "Score": 0},
    ]
    for c in contacts_data:
        table.create(c)

    print(f"\n  Seeded {len(contacts_data)} contacts\n")

    # Simulate enrichment API (in production: Clearbit, Apollo, etc.)
    def enrich_contact(email: str) -> dict:
        enrichment_db = {
            "sarah@techcorp.com":  {"Score": 87, "Company_Size": "50-100",  "Industry": "SaaS"},
            "marcus@startup.io":   {"Score": 62, "Company_Size": "1-10",    "Industry": "Fintech"},
            "priya@enterprise.co": {"Score": 94, "Company_Size": "500+",    "Industry": "Enterprise"},
        }
        return enrichment_db.get(email, {"Score": 0})

    print("- Enriching leads -\n")
    leads = table.all()
    updated_count = 0

    for record in leads:
        email = record["fields"].get("Email", "")
        enriched = enrich_contact(email)
        if enriched.get("Score", 0) > 0:
            table.update(record["id"], enriched)
            print(f"  ✓ Enriched {record['fields']['Name']:15s} → Score: {enriched['Score']}, Industry: {enriched.get('Industry','?')}")
            updated_count += 1

    print(f"\n  Enriched {updated_count} contacts")


# =======================================================
# PART 3: Content Calendar Automation
# =======================================================

def demo_content_calendar():
    """
    Pattern: Read scheduled posts from Airtable, trigger publishing,
    update status. Runs as a daily cron job.
    """
    print("\n" + "=" * 55)
    print("PYAIRTABLE — Content Calendar Automation")
    print("=" * 55)

    table = get_table("Content Calendar")

    # Seed content items
    posts = [
        {"Title": "8 Python Libraries You Should Know",  "Status": "Scheduled", "Platform": "Medium",   "Scheduled_Date": "2026-02-25"},
        {"Title": "Async Python for Beginners",          "Status": "Draft",     "Platform": "Medium",   "Scheduled_Date": "2026-03-01"},
        {"Title": "Python automation tips thread",       "Status": "Scheduled", "Platform": "Twitter",  "Scheduled_Date": "2026-02-25"},
        {"Title": "Behind the stack: our ETL pipeline",  "Status": "Published", "Platform": "LinkedIn", "Scheduled_Date": "2026-02-20"},
    ]
    created = [table.create(p) for p in posts]
    print(f"\n  Seeded {len(created)} content items\n")

    # Simulate: fetch today's scheduled posts and publish them
    today = "2026-02-25"
    print(f"- Publishing posts scheduled for {today} -\n")

    # In real pyairtable: table.all(formula=f"AND(Status='Scheduled', Scheduled_Date='{today}')")
    scheduled = [r for r in table.all() if
                 r["fields"].get("Status") == "Scheduled" and
                 r["fields"].get("Scheduled_Date") == today]

    for record in scheduled:
        f = record["fields"]
        # Simulate publishing API call
        print(f" Publishing to {f['Platform']:10s}: '{f['Title']}'")
        table.update(record["id"], {"Status": "Published", "Published_At": today})
        print(f"     → Status updated to 'Published'")

    published_total = len([r for r in table.all() if r["fields"].get("Status") == "Published"])
    print(f"\n Total published items: {published_total}")


#  Main

if __name__ == "__main__":
    if MOCK_MODE:
        print("Running in MOCK MODE — set AIRTABLE_API_KEY and AIRTABLE_BASE_ID in .env for live mode.\n")

    demo_basic_crud()
    demo_crm_sync()
    demo_content_calendar()
