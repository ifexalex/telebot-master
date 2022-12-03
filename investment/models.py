from django.db import models


class RIO(models.Model):
    DURATION_CHOICES = (
        ('Daily', 'Daily'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    )
    percentage = models.IntegerField(default=0)
    duration = models.CharField(max_length=100, choices=DURATION_CHOICES)

    def __str__(self):
        return f"{self.percentage}% {self.duration}"

    class Meta:
        verbose_name = "Rio"
        verbose_name_plural = "Rios"



class InvestmentPlan(models.Model):
    name = models.CharField(max_length=100, )
    description = models.TextField(null=True, blank=True, help_text="Description of the investment")
    rio = models.ForeignKey(RIO, on_delete=models.CASCADE, related_name="rio")
    range_amt = models.CharField(max_length=100, null=True, blank=True, help_text="Range of investment amount. eg: 100-500")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)                               

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Investment Plan"
        verbose_name_plural = "Investments Plans"
