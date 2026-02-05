from fastapi import APIRouter
from app.schemas import MeetingRequest
from app.llm import extract_action_items, parse_llm_response
from app.services.assignment import resolve_assignee
from app.services.post_process import deduplicate_tasks
from app.services.firestore import save_action_items
from app.services.parse_date import parse_due_text
from app.services.due_date_formatter import format_due_date

router = APIRouter()


@router.post("/process_meeting")
def process_meeting(data: MeetingRequest):
    raw_items = extract_action_items(data.transcript)
    action_items = parse_llm_response(raw_items)
    
    resolved_items = []

    for item in action_items:
        assigned_user_id = resolve_assignee(
            org_id=data.org_id,
            assigned_to_name=item.get("assigned_to_name")
        )
        due_date = parse_due_text(item.get("due_text"))
        resolved_items.append({
            "task": item.get("task"),
            "assigned_to_name": item.get("assigned_to_name"),
            "assigned_to_user_id": assigned_user_id,
            "due_text": item.get("due_text"),
            "display_due_date": format_due_date(due_date, item.get("due_text")),
            "due_date": due_date,   # optional: agar raw date chahiye future me
            "confidence_score": item.get("confidence_score"),
            "needs_manager_review": assigned_user_id is None
        })
    
    resolved_items=deduplicate_tasks(resolved_items)
    save_action_items(
        resolved_items,
        org_id=data.org_id,
        meeting_id=data.meeting_id    
    )    

    return {
        "message": "Meeting received",
        "meeting_id": data.meeting_id,
        "action_items": resolved_items
    }
    # return {
    #     "message": "Meeting received",
    #     "meeting_id": data.meeting_id,
    #     "action_items": action_items
    # }
    
