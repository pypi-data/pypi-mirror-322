from datetime import timedelta

from django.db import models
from django.shortcuts import reverse

from .Reservierung import Reservierung


def dateiname_anleitung_skill(instance, filename):
    fn = f"{instance.nummer}_Anleitung.pdf"
    return f"ausleihe/skills/{instance.nummer}/{fn}"


class Skill(models.Model):
    nummer = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=200, unique=True)
    anzahl_plaetze = models.PositiveSmallIntegerField(
        verbose_name="Anzahl benötigter Plätze",
        help_text="Wie viele Plätze werden von den vorhandenen Plätzen eines Raumes benötigt?"
    )
    min_personen = models.PositiveSmallIntegerField(
        verbose_name="Mind. Personen",
        help_text="Wie viele Personen werden mindestens für die Durchführung benötigt?"
    )
    max_personen = models.PositiveSmallIntegerField(
        verbose_name="Max. Personen",
        help_text="Wie viele Personen können maximal an der Durchführung beteilgt sein?"
    )
    dauer = models.PositiveSmallIntegerField(
        help_text="Zeitraum (min)"
    )
    beschreibung = models.TextField(blank=True)
    raeume = models.ManyToManyField(
        "ausleihe.Raum",
        related_name="skills",
        verbose_name="Räume",
        help_text="In welchen Räumen kann dieser Skill durchgeführt werden?",
        blank=True,
    )
    anleitung = models.FileField(
        upload_to=dateiname_anleitung_skill,
        help_text="PDF-Datei mit der Anleitung für die Studierenden.",
        blank=True,
    )
    ist_sichtbar = models.BooleanField(
        verbose_name="ist sichtbar",
        default=True,
        help_text="Wenn aktiviert, dann ist der Skill zur Ausleihe freigegeben.",
    )

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ("nummer",)

    def __str__(self):
        return f"Skill Nr. {self.nummer}: {self.name}"

    @property
    def td_dauer(self):
        return timedelta(minutes=self.dauer)

    def get_absolute_url(self):
        return reverse("ausleihe:skill-detail", kwargs={"skill_id": self.id})

    def cap_name(self):
        return "".join(c for c in self.name if c.isupper())

    def available_skillsets(self, dt):
        possible_skillsets = self.skillsets.prefetch_related("medium__reservierungen")
        skillsets = []
        von, bis = dt, dt + self.td_dauer

        for skillset in possible_skillsets:
            rs = skillset.medium.reservierungen.filter(
                Reservierung._Q_ueberschneidungen(von, bis)
            )
            if not rs.exists():
                skillsets.append(skillset)

        return skillsets
