"""HTML presentation with escaped user input."""
from html import escape
from .service import MEMBERS

def page(tasks):
    options = ''.join(f'<option>{escape(name)}</option>' for name in MEMBERS)
    cards = ''
    for task in tasks:
        status = 'Completed' if task['done'] else 'Open'
        action = '' if task['done'] else f'<form method="post" action="/tasks/{task["id"]}/complete"><button>Mark complete</button></form>'
        cards += f'<article><div><span class="badge">{status}</span><h2>{escape(task["title"])}</h2><p>{escape(task["assignee"])}</p></div>{action}</article>'
    if not cards:cards = '<p>No tasks yet. Add the first task for your group.</p>'
    done = sum(bool(t['done']) for t in tasks)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Group Task Board - Lab 8</title><style>
*{{box-sizing:border-box}}body{{font:16px system-ui,sans-serif;margin:0;background:#f5f5f4;color:#202020}}main{{max-width:960px;margin:48px auto;padding:0 24px}}header{{border-bottom:2px solid #222;padding-bottom:24px;margin-bottom:24px}}h1{{font-size:36px;margin:8px 0}}h2{{font-size:20px;margin:12px 0 6px}}p{{line-height:1.6}}.panel,article{{background:white;border:1px solid #ccc;border-radius:8px;padding:24px;margin:18px 0}}label{{display:block;font-weight:600;margin:14px 0 6px}}input,select{{width:100%;padding:12px;border:1px solid #888;border-radius:4px;font:inherit}}button{{background:#222;color:white;border:0;border-radius:4px;padding:12px 18px;font:inherit;cursor:pointer;margin-top:16px}}article{{display:flex;justify-content:space-between;gap:20px;align-items:center}}.badge{{border:1px solid #777;padding:3px 8px;font-size:12px;border-radius:4px}}footer{{border-top:1px solid #aaa;margin-top:32px;padding-top:16px;font-size:13px;color:#555}}@media(max-width:600px){{main{{margin-top:24px}}article{{display:block}}}}
</style></head><body><main><header><div>SEG4105 · LAB 8</div><h1>Group Task Board</h1><p>Assign work, track progress, and keep the group organized.</p></header><section class="panel"><h2>Add a task</h2><form method="post" action="/tasks"><label for="title">Task title</label><input id="title" name="title" required maxlength="120" placeholder="What needs to be done?"><label for="assignee">Assigned to</label><select id="assignee" name="assignee">{options}</select><button>Add task</button></form></section><h2>Tasks</h2><p>{len(tasks)-done} open · {done} completed</p>{cards}<footer>Independent group lab application · Python + SQLite</footer></main></body></html>'''
