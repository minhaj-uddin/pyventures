import datetime


class IncidentStore:
    def __init__(self):
        self.incidents = {}
        self.counter = 1

    def list_all(self, status=None, severity=None):
        result = list(self.incidents.values())
        if status:
            result = [i for i in result if i["status"] == status]
        if severity:
            result = [i for i in result if i["severity"] == severity]
        return result

    def get(self, incident_id):
        return self.incidents.get(incident_id)

    def create(self, data):
        incident = {
            "id": self.counter,
            "title": data["title"],
            "description": data.get("description", ""),
            "severity": data.get("severity", "low"),
            "status": "open",
            "reported_at": datetime.datetime.utcnow().isoformat() + "Z",
            "responder": None,
            "timeline": []
        }
        self.incidents[self.counter] = incident
        self.counter += 1
        return incident

    def update_status(self, incident_id, new_status):
        incident = self.get(incident_id)
        if incident:
            incident["status"] = new_status
        return incident

    def delete(self, incident_id):
        return self.incidents.pop(incident_id, None)

    def assign_responder(self, incident_id, responder):
        incident = self.get(incident_id)
        if incident:
            incident["responder"] = responder
        return incident

    def add_timeline_event(self, incident_id, message):
        incident = self.get(incident_id)
        if incident:
            event = {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "message": message
            }
            incident["timeline"].append(event)
            return event
        return None
