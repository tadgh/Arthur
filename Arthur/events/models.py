from django.db import models

# Create your models here.
class Team(models.Model):
    team_id = models.CharField(null=False, max_length=20)
    team_name = models.CharField(null=True, max_length=100)

    def __str__(self):
        return f"{self.team_id}:{self.team_name}"

class HotWord(models.Model):
    BUZZWORD = "BZ"
    ACRONYM = "AC"
    OBFUSCATED_WORD_CHOICES = (
        (BUZZWORD, "Buzzword"),
        (ACRONYM, "Acronym")
    )
    text = models.CharField(null=False, max_length=200, unique=True)
    meaning = models.CharField(null=False, max_length=1000)
    type = models.CharField(
        max_length=2,
        choices=OBFUSCATED_WORD_CHOICES,
        default=BUZZWORD
    )

    @staticmethod
    def classify(text):
        if text.isupper():
            return HotWord.ACRONYM
        else:
            return HotWord.BUZZWORD

    def explain(self):
        return f"*{self.text}*: {self.meaning}"

    def __str__(self):
        return f"{(self.id)} - {self.explain()}"

class SlackMessage(models.Model):
    utterer = models.CharField(max_length=15, null=False)
    message = models.CharField(max_length=5000, null=False)
    channel = models.CharField(max_length=30, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.channel}]({self.utterer}): {self.message}"

class Utterance(models.Model):
    hot_word = models.ForeignKey(HotWord, null=False, on_delete=models.CASCADE)
    utterer = models.CharField(max_length=15, null=False)
    original_context = models.ForeignKey(SlackMessage, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.utterer}): {self.hot_word.text}"
