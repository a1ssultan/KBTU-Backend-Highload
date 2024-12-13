class ShardRouter:
    def db_for_read(self, model, **hints):
        """
        Route read queries to the appropriate shard based on a key (for example user ID).
        """
        if "user_id" in hints:
            user_id = hints["user_id"]
            if user_id % 2 == 0:
                return "shard_1"
            return "shard_2"
        return "default"

    def db_for_write(self, model, **hints):
        """
        Route write queries to the primary shard.
        """
        return "default"
