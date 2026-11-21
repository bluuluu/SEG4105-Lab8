"""Task validation and domain rules."""
MEMBERS = ('Ali, Almis', 'Al-Khawaldeh, Yusuf', 'Du, Jack', 'Luu, Bryan', 'Yatera, Mohamed')
class TaskService:
    def __init__(self, store):self.store = store
    def create(self, title, assignee):
        if not isinstance(title, str) or not title.strip() or len(title.strip()) > 120:
            raise ValueError('Enter a title between 1 and 120 characters.')
        if assignee not in MEMBERS:raise ValueError('Choose a group member.')
        return self.store.add(title.strip(), assignee)
    def complete(self, task_id):
        if not self.store.complete(task_id):raise LookupError('Task not found.')
