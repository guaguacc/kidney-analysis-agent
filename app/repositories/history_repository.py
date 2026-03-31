from typing import Any, Dict, List


class HistoryRepository:
    _storage: Dict[str, List[Dict[str, Any]]] = {}

    def add_record(self, patient_id: str, record: Dict[str, Any]) -> None:
        if patient_id not in self._storage:
            self._storage[patient_id] = []
        self._storage[patient_id].append(record)

    def get_records(self, patient_id: str) -> List[Dict[str, Any]]:
        return self._storage.get(patient_id, [])