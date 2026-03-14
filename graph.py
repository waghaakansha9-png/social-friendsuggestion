from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}

    # Add user
    def add_user(self, user):
        if user not in self.graph:
            self.graph[user] = []

    # Add friendship
    def add_friend(self, u, v):
        if u in self.graph and v in self.graph:
            if v not in self.graph[u]:
                self.graph[u].append(v)
            if u not in self.graph[v]:
                self.graph[v].append(u)

    # Get all friends
    def get_friends(self, user):
        return set(self.graph.get(user, []))

    # Suggest friends (friends of friends)
    def suggest_friends(self, user):
        suggestions = {}
        user_friends = set(self.graph.get(user, []))
        for friend in user_friends:
            for mutual in self.graph.get(friend, []):
                if mutual != user and mutual not in user_friends:
                    suggestions[mutual] = suggestions.get(mutual, 0) + 1
        return suggestions

    # Rank suggestions
    def ranked_suggestions(self, user):
        suggestions = self.suggest_friends(user)
        return sorted(suggestions.items(), key=lambda x: x[1], reverse=True)

    # BFS (optional for graph visualization)
    def bfs(self, start):
        visited = set()
        queue = deque([start])
        order = []
        while queue:
            user = queue.popleft()
            if user not in visited:
                visited.add(user)
                order.append(user)
                queue.extend(self.graph.get(user, []))
        return order