from django.db import models


class Partner(models.Model):
    first_name = models.CharField(max_length=300, verbose_name="Имя")
    second_name = models.CharField(max_length=300, verbose_name="Фамилия")
    phone = models.CharField(max_length=300, verbose_name="Телефон")

    def __str__(self):
        return self.first_name + ' ' + self.second_name


class Site(models.Model):
    name = models.CharField(max_length=300, verbose_name='Имя')
    url = models.CharField(verbose_name='Url сайта', max_length=300)

    def __str__(self):
        return self.name


class LogSite(models.Model):
    partner = models.ForeignKey("Partner")
    site = models.ForeignKey("Site")
    name = models.CharField(verbose_name='Имя заказчика', max_length=300)
    phone = models.CharField(verbose_name='Телефон', max_length=300)
    massages = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(verbose_name='Дата отправки сообщения', auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class PartnerSite(models.Model):
    partner = models.ForeignKey("Partner")
    site = models.ForeignKey("Site")

    def __str__(self):
        return self.partner.first_name + ' ' + self.partner.second_name + ' ' + self.site.name


class PartnerSiteTelegram(models.Model):
    partner_site = models.ForeignKey("PartnerSite")
    chat_id = models.CharField(max_length=500, verbose_name="Телеграм пользователь")
