from collections import defaultdict

class UsageAnalytics:
    def __init__(self):
        self.request_counts = defaultdict(int)

    def record_request(self, model_name: str, endpoint: str):
        key = f"{endpoint}:{model_name}"
        self.request_counts[key] += 1

    def get_usage(self):
        return dict(self.request_counts)

usage_analytics = UsageAnalytics()
