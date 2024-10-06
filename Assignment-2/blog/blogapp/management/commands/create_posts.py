import random
from django.core.management.base import BaseCommand

from ...models import Post, Comment, User, Tag


class Command(BaseCommand):
    help = "This command is used to insert 200 posts into the database."

    def handle(self, *args, **options):
        # Clear existing data (optional, for testing purposes)
        Post.objects.all().delete()
        Comment.objects.all().delete()

        # Retrieve or create users
        users = list(User.objects.all())
        if not users:
            users = [User.objects.create_user(username=f"User{i}", password="password") for i in range(1, 11)]

        # Retrieve or create tags
        tag_titles = ['Animal', 'Clothes', 'News', 'Health', 'Beauty', 'Family', 'Work', 'Lifehacks']
        tags = [Tag.objects.get_or_create(title=title)[0] for title in tag_titles]

        # Create 200 posts with random content
        posts = []
        for i in range(200):
            author = random.choice(users)
            post = Post(
                title=f"Post Title {i + 1}",
                content=f"Content for post {i + 1} goes here...",
                author=author,
            )
            post.save()
            # Attach random tags to each post
            post.tags.set(random.sample(tags, k=random.randint(1, 3)))
            posts.append(post)

        # Optional: Create comments for some posts
        for post in random.sample(posts, k=100):  # Add comments to 100 random posts
            for j in range(random.randint(1, 5)):
                Comment.objects.create(
                    post=post,
                    author=random.choice(users),
                    content=f"Comment {j + 1} on post {post.title}",
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully created 200 posts and associated comments!"))
