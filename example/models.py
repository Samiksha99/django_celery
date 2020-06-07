from django.db import models

# Create your models here.
class ScheduledReport(models.Model):
    """
        Contains email subject and cron expression,to evaluate when the email has to be sent
    """
    subject = models.CharField(max_length=200)
    last_run_at = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    cron_expression = models.CharField(max_length=200)
    def save(self, *args, **kwargs):
        """
        function to evaluate "next_run_at" using the cron expression, so that it is updated once the report is sent.
        """
        self.last_run_at = datetime.now()
        iter = croniter(self.cron_expression, self.last_run_at)
        self.next_run_at = iter.get_next(datetime)
        super(ScheduledReport, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.subject
class ScheduledReportGroup(models.Model):
    """
        Many to many mapping between reports which will be sent out in a
        scheduled report
    """
    report = models.ForeignKey(Report, related_name='report')
    scheduled_report = models.ForeignKey(ScheduledReport,
                               related_name='relatedscheduledreport')
class ReportRecipient(models.Model):
    """
        Stores all the recipients of the given scheduled report
    """
    email = models.EmailField()
    scheduled_report = models.ForeignKey(ScheduledReport, related_name='reportrecep')