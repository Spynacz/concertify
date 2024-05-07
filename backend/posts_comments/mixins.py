class VoteMixin:
    def get_vote_count(self, obj):
        return obj.votes.all().count()

    def get_has_voted(self, obj):
        request = self.context.get("request", None)

        if not hasattr(request, "user") or not request.user.is_authenticated:
            return False

        votes = obj.votes.all()
        return votes.filter(user=request.user).exists()
