import os
import json
import re

MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "memory.json"
)


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r",encoding = "utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w",encoding = "utf-8") as f:
        json.dump(memory, f, indent=4)

def add_memory(ticket_text,result):
    memory = load_memory()

    codes = {
        "accounts payable": "AP",
        "accounts receivable": "AR",
        "inventory": "INV",
        "purchasing": "PUR",
        "order management": "OM",
    }

    Module = result.Module
    code = codes.get(
        Module.lower(), "".join(word[0] for word in Module.split()).upper() or "ERP"
    )
    numbers = [int(re.search(r"\d+$",item["id"]).group()) for item in memory]
    next_number = max(numbers, default=0) + 1
    ticket_id = f"{code}{next_number}"

    memory.append({
        "id": ticket_id,
        "ticket": ticket_text,
        "Module": result.Module,
        "Category": result.Category,
        "Complexity": result.Complexity,
        "Root Cause":result.Root_Cause,
        "Steps": result.Steps
    })

    save_memory(memory)
    print("Saved to:", MEMORY_FILE)
    return ticket_id

def get_ticket(ticket_id:str) -> dict:
     
    """Retrieve one saved ERP ticket by its ID.

    Args:
        ticket_id: The ID of the ticket to retrieve.
    """
    ticket_id = ticket_id.lower().strip()

    for ticket in load_memory():
        if ticket["id"].lower() == ticket_id.lower():
            return ticket
    return {"error":"ticket cant be retrieved"}

def search_tickets(keyword:str) -> list[dict]:
    """Searches the tickets which are stored in the memory
       Args:
       A word or a phrase to search for
    """
    # print(f"TOOL EXECUTED: search_tickets({keyword!r})")
    keyword_lower = keyword.lower().strip()
    if not keyword_lower:
        return []
    results = []
    for ticket in load_memory():
       ticket_text = ticket.get("ticket","").lower()
       module = ticket.get("Module","").lower()
       steps = ticket.get("Steps",[]) 
       if( 
            keyword_lower in ticket_text or
            keyword_lower in module or
            any(keyword_lower in str(step).lower() for step in steps)
       
        ):
            results.append(ticket)
    return results[:5]

# print(search_tickets("invoice"))